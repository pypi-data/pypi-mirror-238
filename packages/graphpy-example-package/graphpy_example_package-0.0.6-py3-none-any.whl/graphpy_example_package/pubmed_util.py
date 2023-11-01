import torch
import os
import numpy as np
import torch
import scipy.sparse as sp


def read_index_info(file_path):
    crs = open(file_path, "r")
    #print (crs.read())
    a = [line.split() for line in crs]
    result = []
    for each in a:
#         print(each)
        result.append(int(each[0]))
    
#     # convert the edge to src and dst
#     src = []
#     dst = []
#     for each_edge in array:
#         src.append(int(each_edge[0]))
#         dst.append(int(each_edge[1]))
    return result



def read_label_info(file_path):
    crs = open(file_path, "r")
#     print ("Output of Read function is ")
#     #print (crs.read())
    a = [line.split() for line in crs]
    result = []
    for each in a:
        result.append(int(each[0]))
    return result




def read_feature_info(file_path):
    crs = open(file_path, "r")
#     print ("Output of Read function is ")
#     #print (crs.read())
    a = [line.split() for line in crs]
#     print(a[0])
    result = []
    for each in a:
        temp = []
#         print(each)
        for each_ele in each:
#             print(each_ele)
            temp.append(float(each_ele))
        result.append(temp)
    return result



def accuracy(output, labels):
    # preds = output.max(1)[1].type_as(labels)
    # correct = preds.eq(labels).double()
    # correct = correct.sum()
    correct = 0
    predict = torch.max(output, 1).indices
    # print("emmmm?")
    #print(predict.size(), predict)
    #print(labels.size(), labels)
    correct = torch.sum(predict==labels)
    return correct/len(labels)

def accuracy_slow(output, labels):
    # preds = output.max(1)[1].type_as(labels)
    # correct = preds.eq(labels).double()
    # correct = correct.sum()
    correct = 0
    predict = torch.max(output, 1).indices
    # print("emmmm?")
    #print(predict.size(), predict)
    #print(labels.size(), labels)
    for i in range(len(labels)):
        if (predict[i] == labels[i]):
            correct = correct + 1
    return correct / len(labels)


def create_label(num_classes, num_nodes):
    result = torch.randint(0, num_classes, (num_nodes,))
    return result

def create_train_index(num_nodes):
    v= np.arange(0,num_nodes)
    torch_v = torch.from_numpy(v)
    return torch_v

def create_test_index(num_nodes):
    v= np.arange(1 + num_nodes, 1 + 2*num_nodes)
    torch_v = torch.from_numpy(v)
    return torch_v

def ran_init_index_and_label(num_classes, num_train, num_test):
    train_label = create_label(num_classes, num_train)
    test_label = create_label(num_classes, num_test)
    train_id = create_train_index(num_train)
    test_id = create_test_index(num_test)
    return train_label, test_label, train_id, test_id
