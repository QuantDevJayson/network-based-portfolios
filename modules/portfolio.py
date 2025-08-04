# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster

# HRP Portfolio Construction

def hrp_weights(prices):
    from modules.network import hierarchical_clustering
    Z = hierarchical_clustering(prices)
    clusters = fcluster(Z, t=2, criterion="maxclust")
    assets = prices.columns
    cluster_map = dict(zip(assets, clusters))
    # Equal weight within cluster
    weights = pd.Series(0, index=assets)
    for c in np.unique(clusters):
        members = [a for a in assets if cluster_map[a] == c]
        for m in members:
            weights[m] = 1 / len(members)
    weights /= weights.sum()
    return weights, cluster_map
