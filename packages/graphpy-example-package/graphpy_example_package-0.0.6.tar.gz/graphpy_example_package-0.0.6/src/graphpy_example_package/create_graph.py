from graphpy_example_package import pygraph as gone
from graphpy_example_package import kernel
import numpy as np
import datetime
import os

def memoryview_to_np(memview, nebr_dt):
    arr = np.array(memview, copy=False)
    #a = arr.view(nebr_dt).reshape(nebr_reader.get_degree())
    a = arr.view(nebr_dt)
    return a;

def create_csr_graph(ifile, num_vcount, ingestion_flag):
    num_sources = 1
    num_thread = 64

    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])
    csr_dt = np.dtype([('dst', np.int32), ('edgeid', np.int32)])
    offset_dt = np.dtype([('offset', np.int32)])

    outdir = ""
    graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_vcount, True, "gtype") # initiate the vertex type
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt) # initiate the pgraph

    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_managerW(0) # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(ifile, ingestion_flag)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    #manager.run_bfs(1)

    #snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    
    offset_csr1, offset_csc1, nebrs_csr1, nebrs_csc1 = gone.create_csr_view(pgraph);
    offset_csr = memoryview_to_np(offset_csr1, offset_dt);
    offset_csc = memoryview_to_np(offset_csc1, offset_dt);
    nebrs_csr = memoryview_to_np(nebrs_csr1, csr_dt);
    nebrs_csc = memoryview_to_np(nebrs_csc1, csr_dt);
    

    kernel_graph_flag = 0; #eADJ graph
    csr_graph = kernel.init_graph(offset_csr, nebrs_csr, offset_csc, nebrs_csc, kernel_graph_flag, num_vcount);
    """
    x = offset_csr[0]
    print("1st node", x)
    for i in range(100):
        print("csr",nebrs_csr[i],nebrs_csc[i])
    csr_graph.run_bfs(1);
    """
    
    

    return csr_graph;

def create_csr_graph_noeid(ifile, num_vcount, ingestion_flag):
    num_sources = 1
    num_thread = 16

    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32)])
    csr_dt = np.dtype([('dst', np.int32)])
    offset_dt = np.dtype([('offset', np.int32)])
    # below is the dtype for zhai's graph
    #csr_dt = np.dtype(np.int32)
    #offset_dt = np.dtype(np.int32)

    outdir = ""
    graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_vcount, True, "gtype") # initiate the vertex type
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt) # initiate the pgraph

    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_manager(0) # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(ifile, ingestion_flag)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    #manager.run_bfs(1)

    #snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)

    offset_csr1, offset_csc1, nebrs_csr1, nebrs_csc1 = gone.create_csr_view(pgraph);
    offset_csr = memoryview_to_np(offset_csr1, offset_dt);
    offset_csc = memoryview_to_np(offset_csc1, offset_dt);
    nebrs_csr = memoryview_to_np(nebrs_csr1, csr_dt);
    nebrs_csc = memoryview_to_np(nebrs_csc1, csr_dt);
    
    """
    Below is the code to generate the zhai's graph
    print("check type", type(offset_csr), len(offset_csr), len(nebrs_csr))
    a_off = offset_csr.tolist()
    b_neb = nebrs_csr.tolist()
    with open('graph.txt', 'a') as the_file:
        for each in a_off:
            the_file.write(str(int(each)))
            the_file.write(" ")
        the_file.write("\n")
        for each in b_neb:
            the_file.write(str(int(each)))
            the_file.write(" ")
    """
    #offset_save = torch.Tensor(offset_csr)
    #nebrs_save = torch.Tensor(nebrs_csr)
    #torch.save(offset_save, 'tensor_off.pt')
    #torch.save(nebrs_save, 'tensor_nebr.pt')

    kernel_graph_flag = 0; #eADJ graph
    csr_graph = kernel.init_graph(offset_csr, nebrs_csr, offset_csc, nebrs_csc, kernel_graph_flag, num_vcount);

    #print("graph2 created")

    #csr_graph.run_bfs(1);

    return csr_graph;

def create_snb_graph(ifile, num_vcount, ingestion_flag):
    num_sources = 1
    num_thread = 2

    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32)])
    nebr_dt = np.dtype([('src', np.int16), ('dst', np.int16)])
    offset_dt = np.dtype([('offset', np.int32)])

    outdir = ""
    graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_vcount, True, "gtype")  # initiate the vertex type
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt)  # initiate the pgraph

    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_manager(0)  # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(ifile, ingestion_flag)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    #manager.run_bfs(1)

    #snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    
    offset_csr1, offset_csc1, nebrs_csr1, nebrs_csc1 = gone.create_csr_view(pgraph);
    offset_csr = memoryview_to_np(offset_csr1, offset_dt);
    offset_csc = memoryview_to_np(offset_csc1, offset_dt);
    nebrs_csr = memoryview_to_np(nebrs_csr1, nebr_dt);
    nebrs_csc = memoryview_to_np(nebrs_csc1, nebr_dt);
    
    kernel_graph_flag = 1; #eSNB graph
    snb_graph = kernel.init_graph(offset_csr, nebrs_csr, offset_csc, nebrs_csc, kernel_graph_flag, num_vcount);
    
    print("created successfuly")

    #snb_graph.set_vcount(num_vcount)
    #actual_vcount = snb_graph.get_vcount()

    
    #snap_t.run_bfs(1);
    
    ofile = ifile + "../saved_graph/"
    is_exist = os.path.exists(ofile)
    if not is_exist:
        os.makedirs(ofile)

    csr_graph.save_graph(ofile)

    return snb_graph;
