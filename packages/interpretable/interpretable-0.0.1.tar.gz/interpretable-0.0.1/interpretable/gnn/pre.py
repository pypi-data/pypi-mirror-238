import numpy as np
import torch

def insert_y_edge(data):
    """
    Add target for the edges (y_edge) which is belonging of nodes to the same group (y) or not
    """
    # Access the node labels from data.y
    node_labels = data.y
    # Initialize an empty list to store the edge attributes
    edge_y = []
    # Iterate through the edges
    for edge in data.edge_index.T:
        source_node_label = node_labels[edge[0]].item()
        target_node_label = node_labels[edge[1]].item()
        # Create the edge attribute as True if the nodes have the same label, False otherwise
        edge_y.append(source_node_label == target_node_label)

    # Convert the list of edge attributes to a PyTorch tensor
    # Add the edge attribute to the dataset
    data.y_edge = torch.tensor(edge_y, dtype=torch.float)
    assert data.validate()
    return data

def split_train_edges(data,train_fraction=0.8,test=False):
    """
    
    TODOs: 
        Use pyg's train_test_split_edges function.
    """
    import numpy as np
    def random_true_vector(m, f):
        num_true_values = int(m * f)
        vector = np.zeros(m, dtype=bool)
        indices = np.random.choice(m, num_true_values, replace=False)
        vector[indices] = True
        return vector
    data.train_mask_edge = torch.tensor(random_true_vector(m=data.edge_index.shape[1], f=train_fraction))
    if test: print(data)

    #### Edge indices based on the mask

    train_edge_index=[]
    test_edge_index=[]
    for t in zip(data.train_mask_edge.numpy(),data.edge_index.T.numpy()):
        if t[0]:
            train_edge_index.append(t[1].tolist())
        else:
            test_edge_index.append(t[1].tolist())

    data.train_edge_index=torch.tensor(np.array(train_edge_index).T)
    data.test_edge_index=torch.tensor(np.array(test_edge_index).T)
    return data