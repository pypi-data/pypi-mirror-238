import networkx as nx
from itertools import combinations

# 创建有权图
G = nx.DiGraph()

# 添加节点
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)
G.add_node(7)
G.add_node(8)
G.add_node(9)
G.add_node(10)
G.add_node(11)
G.add_node(12)
G.add_node(13)
G.add_node(14)
G.add_node(15)


chra1 = [1,3,5,7,9,11,13,15]
chra2 = [2,4,6,8,10,12,14]
chrb1 = [1,2,5,6,9,10,13,14]
chrb2 = [3,4,7,8,11,12,15]

edge_dict = {}
for chr_tmp in [chra1,chra2,chrb1,chrb2]:
    for i in range(len(chr_tmp)):
        if i == len(chr_tmp) -1:
            continue
        if (chr_tmp[i],chr_tmp[i+1]) not in edge_dict:
            edge_dict[(chr_tmp[i],chr_tmp[i+1])] = 0
        edge_dict[(chr_tmp[i],chr_tmp[i+1])] += 1
        
for i in edge_dict:
    G.add_edge(i[0],i[1], weight=edge_dict[i])


# 调用dijkstra_path()函数
# path = nx.dijkstra_path(G, 1, 4)
paths = [i for i in nx.all_simple_paths(G, 1, 4)]
print(paths)

def get_most_weighted_paths(G):
    paths_list = []
    for i,j in combinations(G.nodes, 2):
        paths_list.extend([i for i in nx.all_simple_paths(G, i, j)])

    paths_list = sorted(paths_list, key=lambda x:nx.path_weight(G, x, 'weight'), reverse=True)

    used_paths = []
    used_nodes = []

    for path in paths_list:
        if len(set(used_nodes) & set(path)) > 0:
            continue
        else:
            used_paths.append(path)
            used_nodes.extend(path)

    return used_paths

get_most_weighted_paths(G)