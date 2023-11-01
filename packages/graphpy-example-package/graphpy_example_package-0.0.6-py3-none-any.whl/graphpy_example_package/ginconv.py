import torch as th 
from torch import nn
from graphpy_example_package import sparse
import torch.nn.functional as F



class ApplyNodeFunc(nn.Module):
    """Update the node feature hv with MLP"""
    def __init__(self, mlp):
        super(ApplyNodeFunc, self).__init__()
        self.mlp = mlp

    def forward(self, h):
        h = self.mlp(h)
        return h



def copy_input(input_):
    return input_, input_

"""
class ApplyNodeFunc(nn.Module):
    def __init__(self, mlp):
        super(ApplyNodeFunc, self).__init__()
        self.mlp = mlp
        print("check", self.mlp.output_dim)
        self.bn = nn.BatchNorm1d(self.mlp.output_dim)

    def forward(self, h):
        h = self.mlp(h)
        h = self.bn(h)
        h = F.relu(h)
        return h


"""



class GINConv(nn.Module):
    def __init__(self,
                 device, 
                 apply_func=None,
                 aggregator_type='sum',
                 init_eps=0,
                 learn_eps=False,
                 activation=None):
        super(GINConv, self).__init__()
        self.apply_func = apply_func
        self._aggregator_type = aggregator_type
        self.activation = activation
        self.device = device
        if aggregator_type not in ('sum', 'max', 'mean'):
            raise KeyError(
                'Aggregator type {} not recognized.'.format(aggregator_type))
        # to specify whether eps is trainable or not.
        if learn_eps:
            self.eps = th.nn.Parameter(th.FloatTensor([init_eps]))
        else:
            self.register_buffer('eps', th.FloatTensor([init_eps]))

    def forward(self, graph, feat):

        feat_src, feat_dst = copy_input(feat)
        dim = feat.size(1)
        # aggregate first then mult W
        norm = 0 
        feat_dst = sparse.run_gspmm(graph, feat_dst, norm, graph.get_vcount(), dim, self.device)
        rst = (1 + self.eps) * feat_src + feat_dst
        if self.apply_func is not None:
            rst = self.apply_func(rst)
        # activation
        if self.activation is not None:
            rst = self.activation(rst)
        return rst

class GIN(nn.Module):
    """GIN model"""
    def __init__(self, graph, input_dim, hidden_dim, output_dim, device, num_layers=5):
        """model parameters setting
        Paramters
        ---------
        input_dim: int
            The dimensionality of input features
        hidden_dim: int
            The dimensionality of hidden units at ALL layers
        output_dim: int
            The number of classes for prediction
        """
        super(GIN, self).__init__()
        self.g = graph
        self.num_layers = num_layers
        self.ginlayers = th.nn.ModuleList()
        self.device = device
        
        for layer in range(self.num_layers):
            if layer == 0:
                mlp = nn.Linear(input_dim, hidden_dim)
            elif layer < self.num_layers - 1:
                mlp = nn.Linear(hidden_dim, hidden_dim) 
            else:
                mlp = nn.Linear(hidden_dim, output_dim) 

            self.ginlayers.append(GINConv(self.device, ApplyNodeFunc(mlp), "sum", init_eps=0, learn_eps=False))

    def forward(self, h):
        for i in range(self.num_layers):
            h = self.ginlayers[i](self.g, h)
        return h
