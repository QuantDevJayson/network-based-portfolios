# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
from scipy.cluster.hierarchy import dendrogram
import numpy as np

def plot_correlation_matrix(corr):
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu")
    fig.update_layout(title="Correlation Matrix", margin=dict(l=0, r=0, t=40, b=0))
    return fig

def plot_network(G):
    pos = nx.spring_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color="#888"), hoverinfo="none", mode="lines"))
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text", marker=dict(size=20, color="#1f77b4"), text=list(G.nodes()), textposition="bottom center"))
    fig.update_layout(title="Network Graph", showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
    return fig

def plot_dendrogram(Z, labels):
    import scipy.cluster.hierarchy as sch
    import plotly.colors as pc
    fig = go.Figure()
    dendro = dendrogram(Z, labels=labels, orientation='top', no_plot=True)
    icoord = np.array(dendro['icoord'])
    dcoord = np.array(dendro['dcoord'])
    color_list = dendro.get('color_list', ['black'] * len(icoord))
    asset_labels = dendro.get('ivl', labels)
    palette = pc.qualitative.Plotly
    for i, (xs, ys) in enumerate(zip(icoord, dcoord)):
        color = palette[i % len(palette)] if i < len(palette) else 'black'
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', line=dict(color=color, width=3)))
    leaf_positions = [xs[1] for xs in icoord[:len(asset_labels)]]
    for x, label in zip(leaf_positions, asset_labels):
        fig.add_trace(go.Scatter(x=[x], y=[0], mode='text', text=[label], textposition='bottom center', showlegend=False))
    fig.update_layout(title="Hierarchical Clustering Dendrogram", xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=True))
    return fig
