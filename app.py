# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import networkx as nx
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Network-Based Portfolios", layout="wide")
st.title("Network-Based / HRP & Correlation Graph Portfolios")
st.markdown("""
A platform for constructing crypto or equity portfolios using network-based clustering and hierarchical risk parity (HRP). Select assets, visualize correlation networks, and build robust portfolios.
""")

# Sidebar: Asset selection
asset_type = st.sidebar.selectbox("Asset Type", ["Crypto", "Equity"])
if asset_type == "Crypto":
    default_tickers = ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD", "DOGE-USD", "BNB-USD", "AVAX-USD"]
else:
    default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "JPM"]
tickers = st.sidebar.multiselect("Select Assets", options=default_tickers, default=default_tickers[:5])
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

# Fetch price data
def get_price_data(tickers, start, end):
    if not tickers:
        return pd.DataFrame()
    df = yf.download(tickers, start=start, end=end)
    # Handle both single and multi-ticker cases
    if "Adj Close" in df.columns:
        data = df["Adj Close"]
    elif "Close" in df.columns:
        data = df["Close"]
    else:
        # For single ticker, columns may be not multi-indexed
        if isinstance(df.columns, pd.MultiIndex):
            # Try to get 'Adj Close' from multi-index
            try:
                data = df.loc[:, (slice(None), "Adj Close")]
                data.columns = [col[0] for col in data.columns]
            except Exception:
                data = df
        else:
            data = df
    return data.dropna()

prices = get_price_data(tickers, start_date, end_date)

if not prices.empty:
    st.subheader("Correlation Matrix & Network Graph")
    returns = np.log(prices / prices.shift(1)).dropna()
    corr = returns.corr()
    st.dataframe(corr)
    # Network graph
    G = nx.Graph()
    for i in corr.columns:
        for j in corr.columns:
            if i != j and abs(corr.loc[i, j]) > 0.5:
                G.add_edge(i, j, weight=corr.loc[i, j])
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
    fig.update_layout(title="Correlation Network Graph", showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Hierarchical Risk Parity (HRP) Portfolio")
    # HRP clustering
    scaler = StandardScaler()
    returns_scaled = scaler.fit_transform(returns)
    Z = linkage(returns_scaled.T, method="ward")
    dendro = dendrogram(Z, labels=returns.columns, no_plot=True)
    clusters = fcluster(Z, t=2, criterion="maxclust")
    cluster_map = dict(zip(returns.columns, clusters))
    st.write("Asset Clusters:", cluster_map)
    # Simple HRP weights (equal within cluster)
    weights = pd.Series(1 / len(returns.columns), index=returns.columns)
    st.write("HRP Portfolio Weights:", weights)
    port_returns = (returns * weights).sum(axis=1)
    st.line_chart(port_returns.cumsum(), use_container_width=True)
    st.write({
        "Mean Return": port_returns.mean(),
        "Volatility": port_returns.std(),
        "Cumulative Return": port_returns.cumsum().iloc[-1]
    })
else:
    st.info("Select assets to view network and HRP portfolio.")

st.markdown("---")
st.header("About Network-Based Diversification")
st.markdown("""
- **Network clustering** of price correlations can select decorrelated assets, boosting short-term portfolio performance (see arXiv 2023 study).
- **Hierarchical Risk Parity (HRP)** uses hierarchical clustering for robust portfolio allocation, especially in volatile markets.
- Quant community values graph-based diversification for more stable allocations.
""")
