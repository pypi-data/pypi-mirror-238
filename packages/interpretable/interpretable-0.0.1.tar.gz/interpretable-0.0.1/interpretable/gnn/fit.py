import logging

import numpy as np
import torch
import torch.nn as nn # create model
from torch_geometric.utils import train_test_split_edges
from sklearn.metrics import roc_auc_score, mean_squared_error

def encode(
    data_loader,
    model,
    lr,
    epochs,
    criteria,
    test=False,
    **kws_wandb,
    ):
    if not test:
        import wandb
        assert wandb.login()

    if not test:
        run = wandb.init(
            # Set the project where this run will be logged
            notes=str(model),
            # Track hyperparameters and run metadata
            **kws_wandb,
        )

    # Specify optimizer and loss function
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()

    # Training loop
    from sklearn.metrics import roc_auc_score, mean_squared_error
    def get_metrics(x1,x2):
        metrics={}
        metrics['MSE']=mean_squared_error(x1,x2)
        if all(np.unique(x1)==np.array([0,1])):
            metrics['ROC AUC']=roc_auc_score(x1==1, x2)
        else:
            metrics['r_p']=pearsonr(x1,x2)[0]
            metrics['r_s']=spearmanr(x1,x2)[0]
        return metrics

    def train(
        model,
        data_loader: list,
        optimizer,
        # kind, 
        criteria=None, # both nodes and edges
        test=False,
        ):
        model.train()
        total_loss = 0
        total_loss_node = 0
        total_loss_edge = 0
        for data in data_loader:     
            metrics={}        
            optimizer.zero_grad()

            if criteria.lower().startswith('node'):
                # Forward pass, get decoded data
                x_dec = model(data)
                # if test: print(f"x_dec={x_dec.shape}")
                # Compute the loss
                loss_node = criterion(data.x, x_dec)
                total_loss_node += loss_node.item()
                metrics['train x loss total']=total_loss_node / len(data_loader), 

            if criteria.lower().startswith('edge'):
                z = model.encode(data)#.x, data.train_edge_index)
                edge_dec_train = (z[data.train_edge_index[0]] * z[data.train_edge_index[1]]).sum(dim=1)
                loss_edge = criterion(edge_dec_train, data.y_edge[data.train_mask_edge])
                total_loss_edge += loss_edge.item()
                metrics['train y_edge loss total']=total_loss_edge / len(data_loader)

            ## finish training
            if criteria is None:
                total_loss=loss_node+loss_edge
                metrics['train loss']=total_loss/ len(data_loader)
                total_loss.backward()
            elif criteria.lower().startswith('node'):
                loss_node.backward()
            elif criteria.lower().startswith('edge'):
                loss_edge.backward()
            else:
                raise ValueError(criteria)

            optimizer.step()
            model.eval()
            # Evaluate feature reconstructions
            ## compare x_dec with x
            if data.x is None:
                for k_,mask in [('train x_dec',data.train_mask),('test x_dec',data.test_mask)]:
                    m=get_metrics(
                        x1=data.x[mask].detach().numpy().flatten(),
                        x2=x_dec[mask].detach().numpy().flatten(),
                    )
                    metrics={**metrics,**{f'{k_} {k}':v for k,v in m.items()}}

            ## TODOs: compare edge_attr_dec with edge_attr

            # Compare with the targets (if available)
            ## TODOs: compare node targets
            if not data.y_edge is None:
                ## train
                m=get_metrics(
                    x1=data.y_edge[data.train_mask_edge], 
                    x2=edge_dec_train.detach().numpy(),
                )
                metrics={**metrics,**{f'train edge_y {k}':v for k,v in m.items()}}
                
                ## test
                edge_dec_test = (z[data.test_edge_index[0]] * z[data.test_edge_index[1]]).sum(dim=1)
                m=get_metrics(
                    x1=data.y_edge[~data.train_mask_edge], 
                    x2=edge_dec_test.detach().numpy(),
                )
                metrics={**metrics,**{f'test edge_y {k}':v for k,v in m.items()}}

        return metrics

    # Number of training epochs
    # Training loop
    metrics=[]
    for epoch in range(epochs):
        d_ = train(model, 
                   data_loader=data_loader,
                   optimizer=optimizer,
                   criteria=criteria,
                  )
        d_['epoch']=epoch
        logging.info(f"Epoch {(d_['epoch'] + 1):>3}/{epochs}: "+('; '.join([f"{k}={v:.3f}" for k,v in d_.items()])))
        metrics.append(d_)
        if not test:
            wandb.log(d_)
        else:
            break
    if not test:
        wandb.finish() 
    return metrics