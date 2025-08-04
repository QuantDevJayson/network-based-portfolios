# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import streamlit as st
st.set_page_config(
    page_title="Network-Based Portfolio Analytics: Global Equities, Crypto, Bonds, Commodities, ETFs",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📶"
)

import pandas as pd
import numpy as np
from modules.data import GLOBAL_INDICES, get_price_data
from modules.network import correlation_matrix, build_network, mst_network, hierarchical_clustering
from modules.portfolio import hrp_weights
from modules.analytics import performance_metrics
from modules.visualization import plot_correlation_matrix, plot_network, plot_dendrogram
import matplotlib.pyplot as plt

# Clear Streamlit cache to avoid stale data issues
st.cache_data.clear()

st.title("Network-Based / HRP & Correlation Graph Portfolios")
st.markdown("""
A platform for constructing crypto or equity portfolios using network-based clustering and hierarchical risk parity (HRP). Select assets, visualize correlation networks, and build robust portfolios.
""")

# Sidebar: Add navigation for Project Guide & Glossary
st.sidebar.header("Navigation")
page_options = ["Dashboard", "Project Guide & Glossary"]
selected_page = st.sidebar.radio("", page_options)

# Sidebar: Asset selection
st.sidebar.header("Asset Selection")
region = st.sidebar.selectbox("Select Market Region", list(GLOBAL_INDICES.keys()), help="Choose a region for asset universe (US, Europe, Asia, Crypto)")
available_tickers = GLOBAL_INDICES[region]
tickers = st.sidebar.multiselect("Select Assets/Tickers", options=available_tickers, default=available_tickers[:5], help="Pick assets for portfolio construction")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"), help="Portfolio start date")
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2025-07-31"), help="Portfolio end date")

st.sidebar.header("Factor & Strategy Selection")
factor_options = ["Correlation", "Partial Correlation", "Mutual Information"]
selected_factor = st.sidebar.selectbox("Network Factor Type", factor_options, help="Choose how edges are constructed in the network")
strategy_options = ["HRP", "MST", "Cluster-Based", "Centrality-Based", "Equal Weight", "Mean-Variance", "Minimum Volatility"]
selected_strategy = st.sidebar.selectbox("Portfolio Strategy", strategy_options, help="Select portfolio construction method")

st.sidebar.header("Benchmark Selection")
common_benchmarks = [
    "^GSPC", "^DJI", "^IXIC", "^FTSE", "^GDAXI", "^FCHI", "^N225", "^HSI", "^STOXX50E", "^SMI", "^AORD", "^GSPTSE", "BTC-USD", "ETH-USD"
]
benchmark_options = ["None"] + common_benchmarks + available_tickers
selected_benchmark = st.sidebar.selectbox("Benchmark Asset/Index", benchmark_options, help="Select a benchmark for alpha/beta and risk premium analysis")

st.sidebar.header("Performance Metrics")
metrics_options = ["Mean Return", "Volatility", "Sharpe", "Sortino", "Max Drawdown", "Calmar Ratio", "Alpha", "Beta", "Information Ratio", "Turnover", "Downside Deviation", "Centrality Scores", "Market Risk Premium"]
selected_metrics = st.sidebar.multiselect("Show Metrics", metrics_options, default=metrics_options, help="Choose which metrics to display")

st.sidebar.header("Visualizations")
viz_options = ["Correlation Matrix", "Correlation Graph", "Network Graph", "MST Network", "Dendrogram", "Drawdown"]
selected_viz = st.sidebar.multiselect("Show Visualizations", viz_options, default=viz_options, help="Select which visualizations to show")

# Sidebar: Sample split for in-sample/out-of-sample analysis
st.sidebar.header("Sample Split")
split_options = ["Total Sample", "In-Sample", "Out-of-Sample"]
split_choice = st.sidebar.selectbox("Select Sample", split_options, help="Choose which sample to visualize and evaluate")
split_ratio = st.sidebar.slider("In-Sample Ratio", min_value=0.1, max_value=0.9, value=0.7, step=0.05, help="Proportion of data for in-sample")

prices = get_price_data(tickers, start_date, end_date)
benchmark_prices = None
if selected_benchmark != "None":
    benchmark_prices = get_price_data([selected_benchmark], start_date, end_date)
    if not benchmark_prices.empty:
        benchmark = np.log(benchmark_prices[selected_benchmark] / benchmark_prices[selected_benchmark].shift(1)).dropna()
    else:
        benchmark = None
else:
    benchmark = None

if selected_page == "Project Guide & Glossary":
    st.title("Project Guide & Glossary")
    st.markdown("""
    ## How to Use & Interpret
    - **Asset Selection:** Choose assets from global indices, sectors, or cryptos for portfolio construction.
    - **Factor & Strategy Selection:** Select how relationships are modeled (correlation, partial correlation, mutual information) and portfolio construction method (HRP, MST, cluster-based, etc.).
    - **Benchmark Selection:** Pick a benchmark index or asset for performance comparison (alpha, beta, risk premium).
    - **Performance Metrics:** View risk-adjusted returns (Sharpe, Sortino, Calmar), drawdowns, turnover, alpha/beta, centrality scores, and more.
    - **Visualizations:** Explore correlation matrices, network graphs, MSTs, dendrograms, drawdown charts, and cluster maps.
    - **Project Guide & Glossary:** Sidebar info explains all terms and metrics used.

    ## Steps in Network Interpretation
    **1. Understand the Network Construction**
    - Are edges based on Pearson correlation, partial correlation, or mutual information?
    - Is it a fully connected network, or was it filtered (e.g., MST or correlation thresholding)?
    - *Example*: Correlation-based MST might remove weak or noisy edges, showing the most important asset relationships.

    **2. Identify Key Assets (Nodes)**
    - Central nodes (degree, betweenness, eigenvector centrality) often represent influential or diversified assets.
    - Peripheral nodes may be idiosyncratic or sector-specific.

    **3. Interpret Clusters/Communities**
    - Tightly connected assets often belong to the same sector, share macroeconomic exposure, or show co-movement.
    - Use community detection algorithms (Louvain, Girvan–Newman) to identify these.

    **4. Analyze Edge Weights**
    - Strong edges (high weights) imply tight relationships—good for hedging or pair trading.
    - Weak or absent edges imply independence—good for diversification.

    **5. Topology Insights**
    - Star-like shape: centralized exposure (one dominant asset/sector).
    - Modular/clustered graph: multiple distinct sectors/regimes.
    - Sparse network: low market integration, higher diversification potential.

    ### Portfolio Construction Implications
    | Insight                | Portfolio Implication                                 |
    |------------------------|------------------------------------------------------|
    | Central node           | Can act as a proxy for the network (high beta/influence) |
    | Peripheral asset       | May offer diversification benefits                    |
    | Tightly connected cluster | Avoid overexposing to one cluster or correlated assets |
    | Network sparsity       | Higher potential for diversification                  |
    | Dynamic changes        | Track evolution over time to detect regime shifts, market stress, contagion |

    ### Network-Based Portfolio Construction Methods
    | Method                        | How It Uses the Network                                         |
    |-------------------------------|----------------------------------------------------------------|
    | Hierarchical Risk Parity (HRP) | Uses dendrograms built from correlation distances to assign weights based on hierarchy |
    | Cluster-based investing        | Allocates based on network communities (clusters)               |
    | Minimum Spanning Tree (MST) portfolios | Uses MST structure to select diversified but central assets |
    | Network centrality-based allocation | Allocates more (or less) weight to central assets depending on strategy (momentum vs contrarian) |

    ### Performance Interpretation
    - More robust to estimation error than classic mean-variance models.
    - Offers intuitive control over diversification and exposure.
    - Useful in regime detection or understanding market contagion.

    ## How to Interpret Results
    - **Sharpe/Sortino/Calmar Ratios:** Higher values indicate better risk-adjusted performance.
    - **Alpha/Beta:** Alpha is excess return over benchmark; beta is sensitivity to benchmark movements.
    - **Market Risk Premium:** Difference between portfolio and benchmark mean returns.
    - **Drawdown:** Largest drop from peak to trough; lower is better.
    - **Centrality Scores:** Higher centrality means more influence in the asset network.
    - **Clusters/Communities:** Tightly connected groups may represent sectors or regimes; diversify across clusters for robustness.
    - **Network Topology:** Star-like networks imply centralized risk; modular networks suggest diversified exposure.
    - **Strategy Choice:** HRP is robust to estimation error; MST and cluster-based methods help avoid overexposure to correlated assets.

    ## Glossary
    - **Sharpe Ratio:** Risk-adjusted return (mean/volatility)
    - **Sortino Ratio:** Risk-adjusted return using downside risk
    - **Calmar Ratio:** Mean return divided by max drawdown
    - **Alpha:** Excess return over benchmark
    - **Beta:** Sensitivity to benchmark
    - **Market Risk Premium:** Portfolio mean return minus benchmark mean return
    - **Drawdown:** Largest drop from peak to trough
    - **Centrality:** Asset's influence in the network
    - **HRP:** Hierarchical Risk Parity portfolio construction
    - **MST:** Minimum Spanning Tree network
    - **Cluster-Based:** Portfolio based on network communities
    - **Mean-Variance:** Classic Markowitz optimization
    - **Minimum Volatility:** Portfolio with lowest risk

    ## Industry Standard Thresholds
    - **Sharpe Ratio:** < 1: Suboptimal; 1–2: Acceptable; > 2: Excellent
    - **Sortino Ratio:** < 1: Suboptimal; 1–2: Acceptable; > 2: Excellent
    - **Calmar Ratio:** < 0.5: High risk; 0.5–1: Moderate; > 1: Good
    - **Max Drawdown:** < -20%: Significant risk; -10% to -20%: Moderate; > -10%: Low risk
    - **Alpha:** > 0: Outperformance; < 0: Underperformance
    - **Beta:** ~1: Moves with benchmark; < 1: Less volatile; > 1: More volatile
    - **Information Ratio:** < 0.5: Weak; 0.5–1: Moderate; > 1: Strong
    - **Turnover:** < 0.5: Low; 0.5–1: Moderate; > 1: High
    - **Centrality Scores:** High: Influential; Low: Diversifying
    """)
    st.stop()

if not prices.empty:
    returns = np.log(prices / prices.shift(1)).dropna()
    # Compute correlation matrix for network construction
    if selected_factor == "Correlation":
        corr = correlation_matrix(prices)
    elif selected_factor == "Partial Correlation":
        # Placeholder: implement partial correlation if available
        corr = correlation_matrix(prices)  # fallback
    elif selected_factor == "Mutual Information":
        # Placeholder: implement mutual information if available
        corr = correlation_matrix(prices)  # fallback
    else:
        corr = correlation_matrix(prices)
    n = len(returns)
    split_idx = int(n * split_ratio)
    if split_choice == "In-Sample":
        sample_returns = returns.iloc[:split_idx]
        sample_port_returns = None
    elif split_choice == "Out-of-Sample":
        sample_returns = returns.iloc[split_idx:]
        sample_port_returns = None
    else:
        sample_returns = returns
        sample_port_returns = None
    # Portfolio weights logic (expand for more strategies)
    if selected_strategy == "HRP":
        weights, cluster_map = hrp_weights(prices)
    elif selected_strategy == "Equal Weight":
        weights = pd.Series(1 / len(prices.columns), index=prices.columns)
        cluster_map = {t: 1 for t in prices.columns}
    else:
        weights = pd.Series(1 / len(prices.columns), index=prices.columns)
        cluster_map = {t: 1 for t in prices.columns}
    st.write("Asset Clusters:", cluster_map)
    st.write("Portfolio Weights:", weights)
    port_returns = (returns * weights).sum(axis=1)
    # Sample-specific portfolio returns
    if split_choice == "In-Sample":
        sample_port_returns = port_returns.iloc[:split_idx]
    elif split_choice == "Out-of-Sample":
        sample_port_returns = port_returns.iloc[split_idx:]
    else:
        sample_port_returns = port_returns
    st.line_chart(sample_port_returns.cumsum(), use_container_width=True)
    G = build_network(corr, threshold=0.5) if "Network Graph" in selected_viz else None
    perf = performance_metrics(sample_port_returns, benchmark=benchmark, weights=weights.values, network=G)
    if benchmark is not None and "Market Risk Premium" in selected_metrics:
        perf["Market Risk Premium"] = sample_port_returns.mean() - benchmark.mean()
    st.subheader("Performance Metrics Summary (Tearsheet)")
    perf_table = pd.DataFrame({k: [perf.get(k, None)] for k in selected_metrics})
    st.dataframe(perf_table)
    st.write({k: perf.get(k, None) for k in selected_metrics})
    # Show all selected visualizations
    if "Correlation Matrix" in selected_viz:
        st.subheader("Correlation Matrix")
        fig = plot_correlation_matrix(corr)
        st.plotly_chart(fig, use_container_width=True)
    if "Correlation Graph" in selected_viz:
        st.subheader("Correlation Graph")
        # For correlation graph, build a network from the correlation matrix
        G_corr = build_network(corr, threshold=0.5)
        fig = plot_network(G_corr)
        st.plotly_chart(fig, use_container_width=True)
    if "Network Graph" in selected_viz:
        st.subheader("Network Graph")
        G = build_network(corr, threshold=0.5)
        fig = plot_network(G)
        st.plotly_chart(fig, use_container_width=True)
    if "MST Network" in selected_viz:
        st.subheader("Minimum Spanning Tree (MST) Network")
        mst = mst_network(corr)
        fig = plot_network(mst)
        st.plotly_chart(fig, use_container_width=True)
    if "Dendrogram" in selected_viz:
        st.subheader("Dendrogram")
        from scipy.cluster.hierarchy import linkage
        if 'corr' in locals():
            # Convert correlation to distance for linkage
            dist = 1 - corr
            Z = linkage(dist, method='ward')
            labels = list(prices.columns)
            fig = plot_dendrogram(Z, labels)
            st.plotly_chart(fig, use_container_width=True)
    if "Drawdown" in selected_viz:
        st.subheader("Drawdown Visualization")
        cum_returns = sample_port_returns.cumsum()
        drawdown = cum_returns - cum_returns.cummax()
        st.line_chart(drawdown, use_container_width=True)
else:
    st.info("Select assets to view network and portfolio.")

st.markdown("---")
