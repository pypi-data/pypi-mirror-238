from collections import OrderedDict
from pypaq.mpython.mpdecor import proc_wait
import torch
from typing import Optional

from torchness.types import TNS, DTNS



class TorchnessException(Exception):
    pass

# weights initializer from BERT, the only difference is that in torch values are CLAMPED not SAMPLED till in <a,b>
def bert_initializer(*args, std=0.02, **kwargs):
    return torch.nn.init.trunc_normal_(*args, **kwargs, std=std, a=-2*std, b=2*std)


def my_initializer(*args, std=0.02, **kwargs):
    # different layers use different initialization functions:
    # torch Linear % Conv1D uses kaiming_uniform_(weights) & xavier_uniform_(bias)
    # my TF uses trunc_normal_(weights, std=0.02, a==b==2*std) & 0(bias) <- from BERT
    # - kaiming_uniform_ is uniform_ with bound from 2015 paper, (for relu)
    # - xavier_uniform_ is uniform_ whit bound from 2010 paper (for linear / sigmoid)
    # - trunc_normal_ is normal with mean 0 and given std, all values SAMPLED till in <a,b>
    return bert_initializer(*args, **kwargs, std=std)

@proc_wait
def mrg_ckpts(
        ckptA: str,                     # checkpoint A (file name)
        ckptB: Optional[str],           # checkpoint B (file name), for None takes 100% ckptA
        ckptM: str,                     # checkpoint merged (file name)
        ratio: float=           0.5,    # ratio of merge
        noise: float=           0.0     # noise factor, amount of noise added to new value <0.0;1.0>
):
    """
    weighted merge of two checkpoints
    does NOT check for compatibility of two checkpoints, but will crash if those are not compatible
    enclosed with subprocess for better separation of torch objects
    """
    checkpoint_A = torch.load(ckptA)
    checkpoint_B = torch.load(ckptB) if ckptB else checkpoint_A

    cmsd_A = checkpoint_A['model_state_dict']
    cmsd_B = checkpoint_B['model_state_dict']
    cmsd_M = OrderedDict()

    for k in cmsd_A:
        if cmsd_A[k].is_floating_point():
            std_dev = float(torch.std(cmsd_A[k]))
            noise_tensor = torch.zeros_like(cmsd_A[k])
            if std_dev != 0.0: # bias variable case
                my_initializer(noise_tensor, std=std_dev)
            cmsd_M[k] = ratio * cmsd_A[k] + (1 - ratio) * cmsd_B[k] + noise * noise_tensor
        else:
            cmsd_M[k] = cmsd_A[k]

    checkpoint_M = {}
    checkpoint_M.update(checkpoint_A)
    checkpoint_M['model_state_dict'] = cmsd_M

    torch.save(checkpoint_M, ckptM)

# returns base checkpoint information, if given two - checks if B is equal A
def ckpt_nfo(
        ckptA: str,                     # checkpoint A (file name)
        ckptB: Optional[str]=   None,   # checkpoint B (file name)
):
    checkpoint_A = torch.load(ckptA)
    checkpoint_B = torch.load(ckptB) if ckptB else None
    are_equal = True

    cmsd_A = checkpoint_A['model_state_dict']
    cmsd_B = checkpoint_B['model_state_dict'] if checkpoint_B else None

    print(f'Checkpoint has {len(cmsd_A)} tensors, #floats: {sum([cmsd_A[k].numel() for k in cmsd_A])}')
    for k in cmsd_A:
        tns = cmsd_A[k]
        print(f'{k:100} shape: {str(list(tns.shape)):15} {tns.dtype}')
        if cmsd_B:
            if k in cmsd_B:
                if not torch.equal(cmsd_A[k], cmsd_B[k]):
                    print(f' ---> is not equal in second checkpoint')
                    are_equal = False
            else:
                print(f' ---> is not present in second checkpoint')
                are_equal = False
    if checkpoint_B:
        print(f'Checkpoints {"are equal" if are_equal else "are NOT equal"}')


def scaled_cross_entropy(
        labels: TNS,
        scale: TNS,
        logits: Optional[torch.Tensor]= None,
        probs: Optional[torch.Tensor]=  None) -> DTNS:

    if logits is None and probs is None:
        raise TorchnessException('logits OR probs must be given!')

    if probs is None:
        probs = torch.nn.functional.softmax(input=logits, dim=-1)

    prob_label = probs[range(len(labels)), labels] # probability of class from label

    # merge loss for positive and negative scale
    ce = torch.where(
        condition=  scale > 0,
        input=      -torch.log(prob_label),
        other=      -torch.log(1-prob_label))

    return {
        'scaled_cross_entropy': ce * torch.abs(scale),
        'cross_entropy':        ce}

def select_with_indices(
        source: TNS,
        indices: TNS,
) -> TNS:
    """selects from the (multidimensional dim) source values from the last axis
    given with indices (dim-1) tensor (int)
    """
    indices = torch.unsqueeze(indices, dim=-1)
    source_selected = torch.gather(source, dim=-1, index=indices)
    return torch.squeeze(source_selected, dim=-1)
