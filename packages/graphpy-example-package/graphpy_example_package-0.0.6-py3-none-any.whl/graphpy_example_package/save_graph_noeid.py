
from graphpy_example_package import pygraph as gone
from graphpy_example_package import create_graph as cg
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick graph directory')
    parser.add_argument('--gdir', type=str, default= './', help='pick graph directory')
    parser.add_argument('--vcount', type=int, default=0, help='pick vertex count')
    parser.add_argument('--source', type=str, default='text', help='pick text or binary')
    parser.add_argument('--skip', type=int, default=0, help='skip a few lines when parsing')
    args = parser.parse_args()
    
    file_dir = args.gdir;# "/home/ygong07/data/test2/pubmed/"
    num_vcount  = args.vcount;
    source = args.source;
    skip_lines = args.skip

    ifile = file_dir;
    if (source == 'text'): 
        print("text file");
        ingestion_flag = gone.enumGraph.eUdir
        G = cg.create_csr_graph_noeid(ifile, num_vcount, ingestion_flag)
    else :
        ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eBinarySource
        G = cg.create_csr_graph_noeid(ifile, num_vcount, ingestion_flag)
    
    ofile = ifile + "/../saved_graph/"
    is_exist = os.path.exists(ofile)
    if not is_exist:
        os.makedirs(ofile)

    G.save_graph(ofile)
