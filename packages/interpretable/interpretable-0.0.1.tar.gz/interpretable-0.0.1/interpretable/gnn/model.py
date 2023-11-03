import torch.nn as nn # create model
import torch.nn.functional as F # relu

from interpretable.gnn.layers import get_coder

class Encoder(nn.Module):
    """
    Define the GAE model
    """
    def __init__(self, 
         model_name,
         num_node_features,
         hidden_channels,
         # num_edge_features=None,
         scale_channels_enc: int,
         # scale_channels_dec: int,
         test: bool=False,
         **kws_model,                 
    ):
        super(Encoder, self).__init__()
        self.encoder=get_coder(
            model_name=model_name,
            num_node_features=num_node_features,
            hidden_channels=hidden_channels,
            kind='encoder',
            scale=scale_channels_enc,
            **kws_model,                 
        )

    def forward(self,data):#x, edge_index):
        x, edge_index, edge_attr = data.x, data.edge_index, data.edge_attr
        for layer in self.encoder:
            x_enc = F.elu(layer(x, edge_index, edge_attr))
        # if test: print(f"x_enc.shape={x_enc.shape}")
        return x_enc