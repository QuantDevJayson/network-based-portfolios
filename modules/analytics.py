# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import networkx as nx

def performance_metrics(returns, benchmark=None, weights=None, network=None):
    mean_return = returns.mean()
    volatility = returns.std()
    sharpe = mean_return / volatility if volatility != 0 else np.nan
    downside = returns[returns < 0].std()
    sortino = mean_return / downside if downside != 0 else np.nan
    cum_returns = returns.cumsum()
    max_drawdown = (cum_returns - cum_returns.cummax()).min()
    calmar = mean_return / abs(max_drawdown) if max_drawdown != 0 else np.nan
    turnover = np.sum(np.abs(np.diff(weights))) / len(weights) if weights is not None else np.nan
    # Alpha/Beta (vs benchmark)
    alpha, beta, info_ratio = np.nan, np.nan, np.nan
    if benchmark is not None and len(benchmark) == len(returns):
        X = benchmark.values.reshape(-1, 1)
        y = returns.values
        reg = LinearRegression().fit(X, y)
        beta = reg.coef_[0]
        alpha = reg.intercept_
        info_ratio = (returns.mean() - benchmark.mean()) / (returns - benchmark).std() if (returns - benchmark).std() != 0 else np.nan
    # Downside deviation
    downside_dev = np.sqrt(np.mean(np.minimum(returns, 0) ** 2))
    # Network centrality metrics
    centrality = {}
    if network is not None:
        centrality['degree'] = nx.degree_centrality(network)
        centrality['betweenness'] = nx.betweenness_centrality(network)
        centrality['eigenvector'] = nx.eigenvector_centrality(network)
    return {
        "Mean Return": mean_return,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_drawdown,
        "Calmar Ratio": calmar,
        "Alpha": alpha,
        "Beta": beta,
        "Information Ratio": info_ratio,
        "Turnover": turnover,
        "Downside Deviation": downside_dev,
        "Centrality Scores": centrality
    }
