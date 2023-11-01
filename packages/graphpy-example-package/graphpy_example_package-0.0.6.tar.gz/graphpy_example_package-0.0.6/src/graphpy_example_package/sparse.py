from graphpy_example_package import pygraph as gone
import torch as th
from graphpy_example_package import gp_apis
import gc
import enum



class GSpmm(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, X, norm, num_vcount, dim, device):
        res = gp_apis.gp_gspmm(graph, X, num_vcount, dim, 0, norm, device)  # do not specify the reduce operation
        ctx.backward_cache = graph, norm, num_vcount, dim, device
        return res

    @staticmethod
    def backward(ctx, dZ):
        graph, norm, num_vcount, dim, device = ctx.backward_cache
        ctx.backward_cache = None
        res = gp_apis.gp_gspmm(graph, dZ, num_vcount, dim, 1, norm, device)  # do not specify the reduce operation
        return None, res, None, None, None, None

class GSpmm_max(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, X, norm, num_vcount, dim, device):
        res = gp_apis.gp_gspmm_max(graph, X, num_vcount, dim, 0, norm, device)  # do not specify the reduce operation
        ctx.backward_cache = graph, norm, num_vcount, dim, device
        return res

    @staticmethod
    def backward(ctx, dZ):
        graph, norm, num_vcount, dim, device = ctx.backward_cache
        ctx.backward_cache = None
        res = gp_apis.gp_gspmm_max(graph, dZ, num_vcount, dim, 1, norm, device)  # do not specify the reduce operation
        return None, res, None, None, None, None

class GApplyEdges(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, X, Y, device):
        dim = X.size(1)
        num_ecount = graph.get_edge_count()
        #print("apply_Edge dims are", num_ecount, dim)

        res = gp_apis.gp_gsddmme(graph,X, Y, num_ecount, dim, gone.enumOP.eSUM, 0, device)
        #print("apply edge forward size", res.size())
        #print("ApplyEdge is any nan", res.isnan().any())
        ctx.backward_cache = graph, dim, device
        return res

    @staticmethod
    def backward(ctx, dZ):
        #print("apply_edge_backward")
        graph, dim, device = ctx.backward_cache
        ctx.backward_cache = None
        num_vcount = graph.get_vcount();
       
        resX = gp_apis.gp_gspmmw(graph, dZ, num_vcount, dim, gone.enumOP.eSUM, 1, device)
        #print("apply edge backward", resX.size())
        #print("is any nan", resX.isnan().any())
        resY = gp_apis.gp_gspmmw(graph, dZ, num_vcount, dim, gone.enumOP.eSUM, 0, device)
        #print("apply edge backward", resY.size())
        #print("is any nan", resY.isnan().any())

        return None, resX, resY, None


class GApplyEdge_heads(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, X, Y, device):
        num_ecount = graph.get_edge_count()
        heads = X.size(1)
        #print("apply_Edge_heads dims are", X.size(), Y.size(), num_ecount, heads)
        
        #dim is always 1 here (only)
        res = gp_apis.gp_gsddmme2d(graph, X, Y, num_ecount, heads, gone.enumOP.eSUM, 0, device)

        #print("sddmme SUM", res)
        ctx.backward_cache = graph, heads, device
        #print("res_forward", res)
        #print("apply_edge_done")
        return res

    @staticmethod
    def backward(ctx, dZ):
        #print("GApplyEdge_heads_backward")
        graph, heads, device = ctx.backward_cache
        ctx.backward_cache = None
        num_vcount = graph.get_vcount();
        #print("vcount?", num_vcount) 
        resX = gp_apis.gp_gspmmw2d(graph, dZ, num_vcount, heads, gone.enumOP.eSUM, 1, device)
        resY = gp_apis.gp_gspmmw2d(graph, dZ, num_vcount, heads, gone.enumOP.eSUM, 0, device)
        #print("apply_edge_heads backward ends") 
        return None, resX, resY, None


class EdgeSoftmax(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, efficient_score, dim, device):
        num_vcount = graph.get_vcount()
        num_ecount = graph.get_edge_count();
        
        #print("edge_softmax dim is:", num_vcount, num_ecount, dim)
        
        # for score_max
        score_max = gp_apis.gp_gspmmw(graph, efficient_score, num_vcount, dim, gone.enumOP.eMAX, 0, device)
        
        #print("max", score_max.size())
        #print("MAX is any nan", score_max.isnan().any())
        #print("MAX is any inf", th.sum(th.isinf(score_max)))
        """
        score_flat = th.flatten(score_max).tolist()
        for i in range(len(score_flat)):
            if score_flat[i] <= -999:
                print(" score_max it has 0-")
                break
        """
        
        # sub from score_max
        score = gp_apis.gp_gsddmm(graph, score_max, efficient_score, num_ecount, dim, gone.enumOP.eSUB, 0, device)
        #print("score for sddmm",th.sum(th.isinf(score)))
        
        #print("score", score.size())
        #print("SUB is any nan", score.isnan().any())
        """
        score_flat = th.flatten(score).tolist()
        for i in range(len(score_flat)):
            if score_flat[i] < -100.0:
                print("score_sub it has -inf", score_flat[i], i)
                break
        """
        
        # apply expo for score
        score_exp = th.exp(score)
        """
        count = 0
        score_flat = th.flatten(score_exp).tolist()
        for i in range(len(score_flat)):
            if score_flat[i] == 0 :
                count = count + 1
                #print("score_exp it has 0", score_flat[i], i, score[i])
                #break
        
        print("score_exp it has 0", count)
        """
        
        # todo score_sum
        score_sum = gp_apis.gp_gspmmw(graph, score_exp, num_vcount, dim, gone.enumOP.eSUM, 0, device)
        
        #print("score_sum", score_sum.size())
        #print("SUM is any nan", score_sum.isnan().any())
        """
        score_flat = th.flatten(score_sum).tolist()
        for i in range(len(score_flat)):
            if score_flat[i] == 0 :
                print("score_sum it has 0", score_flat[i], i)
                #break
        """
        # todo score % score_sum.out is | E |
        out = gp_apis.gp_gsddmm(graph, score_sum, score_exp, num_ecount, dim, gone.enumOP.eDIV, 0, device)
        #print("edge softmax out", out.size())
        #print("DIV is any nan", out.isnan().any())
        #print("DIV is any inf", th.sum(th.isinf(out)))

        ctx.backward_cache = graph, dim, out, device
        return out

    @staticmethod
    def backward(ctx, dZ):
        #print("edge_softmax_backward")
        graph, dim, out, device = ctx.backward_cache
        ctx.backward_cache = None
        sds = out * dZ

        num_vcount = graph.get_vcount();
        num_ecount = graph.get_edge_count();
        
        accum = gp_apis.gp_gspmmw(graph, sds, num_vcount, dim, gone.enumOP.eSUM, 0, device)
        #print("score_sum backward", accum.size())
        #print("is any nan", accum.isnan().any())
        
        temp = gp_apis.gp_gsddmm(graph, accum, out, num_ecount, dim, gone.enumOP.eMUL, 0, device)
        
        grad_score = sds - temp
        #print("grad_score", grad_score)
        
        return None, grad_score, None, None


#dim is not useful here
class EdgeSoftmax_heads(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, efficient_score, dim, device):
        #efficient score is |E*head| size.
        heads = efficient_score.size(1)
        num_vcount = graph.get_vcount()
        num_ecount = graph.get_edge_count()
        
        #print("EdgeSoftmax_heads dim are:", efficient_score.size(), num_vcount, num_ecount, heads, dim)
        
        #print("effic score size:", efficient_score.size())
        # for score_max => |V*head|
        score_max = gp_apis.gp_gspmmw2d(graph, efficient_score, num_vcount, heads, gone.enumOP.eMAX, 0, device)
       
        #print("time for sddmm2d: score_max", score_max.size())
        #print("time result:", efficient_score.size())
        # sub from score_max
        score = gp_apis.gp_gsddmm2d(graph, score_max, efficient_score, num_ecount, heads, gone.enumOP.eSUB, 0, device)
        
        # apply expo for score
        score_exp = th.exp(score)
        #th.cuda.empty_cache()
        #del variables
        #gc.collect()
        #print(th.cuda.memory_summary(device=None, abbreviated=False)) 
        
        # score_sum
        score_sum = gp_apis.gp_gspmmw2d(graph, score_exp, num_vcount, heads, gone.enumOP.eSUM, 0, device)
        
        # score % score_sum.out is | E |
        out = gp_apis.gp_gsddmm2d(graph, score_sum, score_exp, num_ecount, heads, gone.enumOP.eDIV, 0, device)

        ctx.backward_cache = graph, out, heads, device
        #print("XXX EdgeSoftmax_heads_forward_out", out.size())
        return out

    @staticmethod
    def backward(ctx, dZ):
        #print("EdgeSoftmax_heads_backward")
        graph, out, heads, device = ctx.backward_cache
        ctx.backward_cache = None
        #print("out size", out.size())
        #print("dZ size", dZ.size())
        #print("dZ is ", dZ)
        sds = out * dZ

        num_vcount = graph.get_vcount()
        num_ecount = graph.get_edge_count()
        #print("come to next kernel") 
        accum = gp_apis.gp_gspmmw2d(graph, sds, num_vcount, heads, gone.enumOP.eSUM, 0, device)
        
        temp = gp_apis.gp_gsddmm2d(graph, accum, out, num_ecount, heads, gone.enumOP.eMUL, 0, device)
        
        grad_score = sds - temp
        #print("grad_score", grad_score)

        return None, grad_score, None, None



class GSpmm_op(th.autograd.Function):
    @staticmethod
    def forward(ctx, graph, X, edge_score_by_softmax, dim, device):
        # input is for each edge, edge_score_by_softmax is also refer to each edge
        #print("begin_gspmv_op_forward")
        num_vcount = graph.get_vcount()
        
        rst = gp_apis.gp_gspmmw_op(graph, X, edge_score_by_softmax, num_vcount, dim, gone.enumOP.eSUM, 0, device)
        #print("op dim", rst.size())
        #print("spmm_op", rst.size())
        #print("SpMM_OP is any nan", rst.isnan().any())
        
        ctx.backward_cache = graph, X, edge_score_by_softmax, dim, device
        return rst


    @staticmethod
    def backward(ctx, dZ):
        #print("begin_gspmv_op_backward")
        graph, X, edge_score_by_softmax, dim, device = ctx.backward_cache
        ctx.backward_cache = None
        reverse = 1
        num_vcount = graph.get_vcount();
        num_ecount = graph.get_edge_count();
        
        res = gp_apis.gp_gspmmw_op(graph, dZ, edge_score_by_softmax, num_vcount, dim,  gone.enumOP.eSUM, reverse, device)
        #print("spmm_op backward", res.size())
        #print("is any nan", res.isnan().any())
        escore = gp_apis.gp_gsddmme(graph, X, dZ, num_ecount, 1, gone.enumOP.eMUL, 0, device)
        #print("sddmme backward eMuL backward", escore.size())
        #print("is any nan", escore.isnan().any())
        
        return None, res, escore, None, None


class GSpmm_op_heads(th.autograd.Function):
    @staticmethod
    def forward(ctx, X, graph, edge_score_by_softmax, dim, device):
        #print("GSpmv_op_heads_forward")
        # input is for each edge, edge_score_by_softmax is also refer to each edge
        num_vcount = graph.get_vcount()
        heads = edge_score_by_softmax.size(1)
        #print("op_heads X", X.size())
        #print("op_heads Y:", edge_score_by_softmax.size())
        #print("res_dim" ,dim)
        rst = gp_apis.gp_gspmmw_op2d(graph, X, edge_score_by_softmax, num_vcount, heads, dim, gone.enumOP.eSUM, 0, device)
        
        ctx.backward_cache = graph, X, edge_score_by_softmax, dim, heads, device
        #print("GSpmv_op_heads_res_forward", rst)
        return rst


    @staticmethod
    def backward(ctx, dZ):
        #print("GSpmv_op_heads_backward before dZ is", dZ)
        #print ("9999")
        graph, X, edge_score_by_softmax, dim, heads, device = ctx.backward_cache
        ctx.backward_cache = None
        reverse = 1
        num_vcount = graph.get_vcount()
        num_ecount = graph.get_edge_count()
        
        res = gp_apis.gp_gspmmw_op2d(graph, dZ, edge_score_by_softmax, num_vcount, heads, dim,  gone.enumOP.eSUM, reverse, device)
        escore = gp_apis.gp_gsddmme2d(graph, X, dZ, num_ecount, heads, gone.enumOP.eMUL, 0, device)
        #print("backward escore", escore) 

        return res, None, escore, None, None



# This is used by GCN, GIN only.
# the gspmm has only 1 input, and then apply different operations such as sum, max on it
def run_gspmm(graph, X, norm, num_vcount, dim, device):
    return GSpmm.apply(graph, X, norm, num_vcount, dim, device)


def run_gspmm_max(graph, X, norm, num_vcount, dim, device):
    return GSpmm_max.apply(graph, X, norm, num_vcount, dim, device)

# the gspmv_op has 2 inputs, one is edge_score, another one is edge_softmax score
def run_gspmv_op(graph, X, edge_score_by_softmax, num_vcount, dim, device):
    return GSpmm_op.apply(graph, X, edge_score_by_softmax, dim, device)


def run_gspmv_op_heads(graph, X, edge_score_by_softmax, num_vcount, dim, device):
    return GSpmm_op_heads.apply(X, graph, edge_score_by_softmax, dim, device)

def apply_edge(graph, el, er, device):
    return GApplyEdges.apply(graph, el, er, device)

def apply_edge_heads(graph, el, er, device):
    return GApplyEdge_heads.apply(graph, el, er, device)



def edge_softmax(graph, efficient_score, num_vcount, dim, device):
    return EdgeSoftmax.apply(graph, efficient_score, dim, device)

def edge_softmax_heads(graph, efficient_score, num_vcount, dim, device):
    result = EdgeSoftmax_heads.apply(graph, efficient_score, dim, device)
    return result
