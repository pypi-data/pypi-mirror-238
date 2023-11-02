import torch
import dgl
import torch as th
import torch
from torch._C import device
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
# from dgl.data import MiniGCDataset
from dgl.nn.pytorch import GraphConv
from sklearn.metrics import accuracy_score
import re
from .mymodel import GINClassifier
import sys
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from random import sample
from sklearn.model_selection import train_test_split
import networkx as nx
# import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import numpy as np
import argparse
import os
os.environ["CUDA_VISIBLE_DEVICES"] = '0'
import time
DEVICE = torch.device("cuda:0")

def parse_arg():
    parser = argparse.ArgumentParser(description='GIN')
    parser.add_argument('--num-epochs', type=int, default=3000,
                        help="number of training epochs (default: 1000)")
    parser.add_argument('--batch-size', type=int, default=128,
                        help="sizes of training batches (default: 64)")
    parser.add_argument('--lr', type=float, default=0.001,
                        help="learning rate (default: 0.01)")
    parser.add_argument('--seed', type=int, default=0,
                        help="random seed for splitting the dataset into 10 (default: 0)")
    parser.add_argument('--num_layers', type=int, default=5,
                        help="number of layers INCLUDING the input one (default: 5)")
    parser.add_argument('--num_mlp_layers', type=int, default=2,
                        help="number of layers for MLP EXCLUDING the input one (default: 2). 1 means linear model.")
    parser.add_argument('--neigh-pooling-type', type=str, default="sum", choices=["sum", "mean", "max"],
                        help="Pooling for over neighboring nodes: sum, mean")
    parser.add_argument('--graph-pooling-type', type=str, default="sum", choices=["sum", "mean"],
                        help="Pooling for the graph: max, sum, mean")
    parser.add_argument('--num-tasks', type=int, default=1,
                        help="number of the  task for the framework")
    parser.add_argument('--hidden-dim', type=int, default=128,
                        help="number of hidden units")
    parser.add_argument('--feat-drop', type=float, default=0.05,
                        help="dropout rate of the feature")
    parser.add_argument('--final-drop', type=float, default=0.05,
                        help="dropout rate of the prediction layer")
    parser.add_argument('--learn-eps', action="store_true",
                        help='Whether to learn the epsilon weighting for the center nodes.')
    args = parser.parse_args()
    return args

def preprocess(path):
    passwd = []
    exp = re.compile(r'[^\x00-\x7f]')
    num=0
    try:
        with open(path, 'r', encoding='ISO-8859-1') as wordlist:
            for line in wordlist:   ###弱口令添加
                wl=line.strip()
                pd=wl
                passwd.extend([pd])
                # if len(passwd)==100000:
                #     break
    except FileNotFoundError:
        print("The password file does not exist", file=sys.stderr)
    return passwd
def password2txt(password,dict_onehot,dict3):
    special_string = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    string_temp = password
    # for i in string_temp:
    i = string_temp
    j = len(i) + 1
    dict1 = {}
    list1_edge = []
    list2_edge = []
    # list3 = []
    for m in range(0, j):
        list1_edge.append(m)
        list2_edge.append(m + 1)
    edge_start, edge_end = torch.tensor(list1_edge), torch.tensor(list2_edge)
    # dict1['edge_start'] = edge_start
    # dict1['edge_end'] = edge_end
    dgl_list = list([])
    label_list = list([])
    for index1 in range(0,len(i)):
        list1=[]
        list2=[]
        list3=[]
        dict1['edge_start'] = edge_start
        dict1['edge_end'] = edge_end
        list1.append(1)
        list1.append(1)
        for index in range(2, len(edge_start)):
            if (index - 2) == index1:
                list1.append(0)
            elif edge_end[index - 2] == index1:
                list1.append(0)
            elif i[edge_start[index - 2]].isalpha() and i[edge_end[index - 2]].isalpha():
                list1.append(4)
            elif i[edge_start[index - 2]].isdigit() and i[edge_end[index - 2]].isdigit():
                list1.append(4)
            elif i[edge_start[index - 2]] in special_string and i[
                edge_end[index - 2]] in special_string:
                list1.append(1)
            elif (i[edge_start[index - 2]].isalpha() and i[edge_end[index - 2]].isdigit()) or (
                    i[edge_start[index - 2]].isdigit() and i[edge_end[index - 2]].isalpha()):
                list1.append(1)
            elif (i[edge_start[index - 2]].isalpha() and i[edge_end[index - 2]] in special_string) or (
                    i[edge_start[index - 2]] in special_string and i[edge_end[index - 2]].isalpha()):
                list1.append(4)
            elif (i[edge_start[index - 2]].isdigit() and i[edge_end[index - 2]] in special_string) or (
                    i[edge_start[index - 2]] in special_string and i[edge_end[index - 2]].isdigit()):
                list1.append(4)
        dict1['edge_weight'] = list1
        list3.append("START")
        list3.append("START")
        for m1 in range(0, j - 1):
            if m1==index1:
                list3.append('null')
            else:
                list3.append(i[m1])
        dict1['node_label'] = list3
        label = torch.tensor(dict3[i[index1]], dtype=torch.int32)
        dict1['graph_label'] = label
        dict1['number_nodes'] = j + 1
        dict1['number_edge'] = len(edge_start)
        graph_dict = dict1
        edge_start, edge_end = graph_dict['edge_start'], graph_dict['edge_end']
        node_label = list(map(lambda x: dict_onehot[x], graph_dict['node_label']))
        g = dgl.DGLGraph()
        g.add_nodes(graph_dict['number_nodes'])
        node_label = np.array(node_label)
        g.ndata['feature'] = torch.tensor(node_label)
        edge_w = torch.tensor([*(graph_dict['edge_weight']), *(graph_dict['edge_weight'])])
        g.add_edges([*edge_start, *edge_end], [*edge_end, *edge_start])  ###双向图
        g.edata['w'] = edge_w
        dgl_list.append(g)
        # label_list.append(torch.tensor(dict3[password[m]], dtype=torch.int32))
        label_list.append(graph_dict['graph_label'])
    return dgl_list,label_list

input_dim = 96
output_dim = 96
if torch.cuda.is_available():
    is_cuda = True
    torch.cuda.manual_seed_all(0)
args = parse_arg()
model = GINClassifier(args.num_layers, args.num_mlp_layers, input_dim, args.hidden_dim, output_dim, args.feat_drop,
                          args.learn_eps, args.graph_pooling_type, args.neigh_pooling_type, args.final_drop, is_cuda)
state_dict=torch.load('./data/Model-graph-500.kpl')
model.load_state_dict(state_dict)
model.eval()
model.to(DEVICE)

file1=open('./data/dict3_rockyou_psm_new_4_10w.txt','r')
dict3=eval(file1.read())
file=open('./data/element_list_psm_new_4_new_10w.txt','r')
element_list = eval(file.read())
file2=open("./data/node_label_map_rockyou_psm_new_4_new_10w.txt",'r')
string1=file2.read().replace(' ','')
string1=string1.replace('\n','')
string1=string1.replace('array','np.array')
string1=string1.replace('float32','np.float32')
# print(string1)
dict_onehot=eval(string1)

class MyDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]
# all_loader=
all_prob=[]
# model.eval()
def bpe_guess(password):
    prob_list=[]
    with torch.no_grad():
        prob=1
        graph,label=password2txt(password,dict_onehot,dict3)
        dataset = MyDataset(graph, label)
            # test_loader = DataLoader(dataset, batch_size=1, shuffle=False)
        # model.eval()
        # test_pred, test_label = [], []
        for it, (batchg, label) in enumerate(dataset):
            batchg, label = batchg.to(DEVICE), label.to(DEVICE)
            pred = torch.softmax(model(batchg), 1)
            # pred = torch.max(pred, 1)[1].view(-1)
            pred= pred.detach().cpu().numpy().tolist()
            prob_list.append(pred[0][label])
    return prob_list

# start=time.time()
print(bpe_guess("password"))
# end=time.time()
# print(end-start)