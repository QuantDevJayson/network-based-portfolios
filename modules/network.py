# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import numpy as np
import pandas as pd
import networkx as nx
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.metrics import pairwise_distances

# Network construction utilities

def correlation_matrix(prices):
    returns = np.log(prices / prices.shift(1)).dropna()
    return returns.corr()

def build_network(corr, threshold=0.5):
    G = nx.Graph()
    for i in corr.columns:
        for j in corr.columns:
            if i != j and abs(corr.loc[i, j]) > threshold:
                G.add_edge(i, j, weight=corr.loc[i, j])
    return G

def mst_network(corr):
    # Minimum Spanning Tree from correlation distances
    dist = 1 - np.abs(corr)
    G = nx.Graph()
    for i in corr.columns:
        for j in corr.columns:
            if i != j:
                G.add_edge(i, j, weight=dist.loc[i, j])
    mst = nx.minimum_spanning_tree(G)
    return mst

def hierarchical_clustering(prices):
    returns = np.log(prices / prices.shift(1)).dropna()
    Z = linkage(returns.T, method="ward")
    return Z
