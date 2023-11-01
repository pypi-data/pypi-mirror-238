import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime

from graphpy_example_package import gp_apis
from graphpy_example_package import pubmed_util
from graphpy_example_package import gcnconv as gnn
# import gcnconv as gnn
from graphpy_example_package import create_graph as cg
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--gdir', type=str, required=True, help='pick graph directory')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--graph', type=str, default= 'binary', help='pick text or binary')
    parser.add_argument('--dim', type=int, default= 16, help='intermediate feature length')
    parser.add_argument('--category', type=int, required=True, help='classification category. e.g. cora has     7')
    parser.add_argument('--feature', type=str, default= 'text', help='pick text, binary, or feature length to generate')
    args = parser.parse_args()

    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')


    graph_dir = args.gdir #"/mnt/huge_26TB/data/test2/cora/"
    if args.graph == 'text':
        graph_data_path = graph_dir + "graph_structure/graph.txt"
        ## TODO
    else:
        ofile = graph_dir + "saved_coo/"
        #ofile = graph_dir + "saved_graph/"
        graph = gp_apis.load_graph_noeid(ofile);
    
    num_vcount = graph.get_vcount();
    print(num_vcount, graph.get_edge_count())
    
    if args.feature == 'text':
        feature = pubmed_util.read_feature_info(graph_dir + "feature/feature.txt")
        feature = torch.tensor(feature).to(device)
    elif args.feature == 'binary':
        feature = torch.load(graph_dir + "feature/feature.pt")
        feature = feature.to(device)
    else :
        feature = torch.rand(num_vcount, int(args.feature))
        feature = feature.to(device)

    if args.feature == 'text' or args.feature == 'binary':
        train_id = pubmed_util.read_index_info(graph_dir + "index/train_index.txt")
        test_id = pubmed_util.read_index_info(graph_dir + "index/test_index.txt")
        test_y_label =  pubmed_util.read_label_info(graph_dir + "label/test_y_label.txt")
        train_y_label =  pubmed_util.read_label_info(graph_dir + "label/y_label.txt")
        train_id = torch.tensor(train_id).to(device)
        test_id = torch.tensor(test_id).to(device)
        train_y_label = torch.tensor(train_y_label).to(device)
        test_y_label = torch.tensor(test_y_label).to(device)

    else:
        #num_train = 480
        train = 1
        val = 0.3
        test = 0.1
        #train_mask = int(num_vcount * train) + [0
        num_train = int(num_vcount * val)
        num_test = int(num_vcount * test)
        #num_train = len(val_mask)
        #num_test = len(test_mask)
        print("train. test", num_train, num_test, num_vcount)
        train_y_label, test_y_label, train_id, test_id =  pubmed_util.ran_init_index_and_label(args.category, num_train, num_test)
        train_y_label = train_y_label.to(device)
        test_y_label = test_y_label.to(device)
        train_id = train_id.to(device)
        test_id = test_id.to(device)

   
    input_feature_dim = feature.size(1)
    net = gnn.GCN(graph, input_feature_dim, args.dim ,  args.category, device)
    net.to(device)

    
    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    start = datetime.datetime.now()
    overhead = 0
    for epoch in range(200):
        start1 = datetime.datetime.now()
        logits = net(feature)
        logp = F.log_softmax(logits, 1)
    
        loss = F.nll_loss(logp[train_id], train_y_label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        end1 = datetime.datetime.now()
        diff = end1 - start1
        overhead = overhead + diff.total_seconds()
        #print(diff)

        #logits_test = net.forward(feature)
        #logp_test = F.log_softmax(logits_test, 1)
        #acc_val = pubmed_util.accuracy(logp[test_id], test_y_label)
        #print('Epoch %d | Train_Loss %.4f | Test_accuracy: %.4f' % (epoch, loss.item(), acc_val))
        #print('Epoch %d | Train_Loss %.4f' % (epoch, loss.item()))

    end = datetime.datetime.now()
    difference = end - start
    print("GCN time of graphpy is:", difference, overhead)
    logits_test = net.forward(feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

