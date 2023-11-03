import numpy as np

def get_channels(start, end, scale, kind):
    if start==end:
        logging.warning(f"start==end ({start})")
        return [start]
    if kind.lower().startswith('enc'):
        start,end=sorted([start,end])[::-1]
        if not scale is None:
            # Forward order
            l=[int(start / scale**i) for i in range(100) if int(start / scale**i) > end]+[end]
        else:
            l=[start,end]
    elif kind.lower().startswith('dec'):
        start,end=sorted([start,end])
        if not scale is None:
            # Reverse order
            l=([int(end / scale**i) for i in range(100) if int(end / scale**i) > start]+[start])[::-1]
        else:
            l=[start,end]
    assert l[0]==start, l
    assert l[-1]==end, l
    assert len(l) == len(set(l)), l # unique
    return l[1:]


def get_layers(
    model_name,
    num_node_features,
    hidden_channels,
    kind,
    scale,
    **kws_model,
    ):
    """
    Get the layers for encoding or decoding.
    """
    from torch_geometric import nn
    layers=[]
    for i in get_channels(num_node_features,hidden_channels,kind=kind,scale=scale):
        layers.append(
            getattr(nn,model_name)(in_channels=num_node_features if kind.lower().startswith('enc') else hidden_channels,
                      out_channels=i,
                      **kws_model,
                     )
            )
    return layers

def get_coder(
    # self,
    model_name,
    num_node_features,
    hidden_channels,
    kind,
    scale,
    **kws_model
    ):
    """
    Get a stack of layers for encoding or decoding 
    """
    import torch.nn as nn
    return nn.ModuleList(get_layers(model_name,num_node_features,hidden_channels, kind=kind,scale=scale,**kws_model))