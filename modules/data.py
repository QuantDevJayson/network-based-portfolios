# Project by @QuantDevJayson
# GitHub: https://github.com/QuantDevJayson
# PyPI: https://pypi.org/user/jayson.ashioya
# LinkedIn: https://www.linkedin.com/in/jayson-ashioya-c-082814176/

import yfinance as yf
import pandas as pd
import numpy as np

# Expanded global indices, sectors, themes, and crypto tickers
GLOBAL_INDICES = {
    'US': [
        '^GSPC', '^DJI', '^IXIC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'JPM', 'V', 'UNH', 'HD', 'PG', 'BAC', 'DIS', 'MA', 'NFLX', 'XOM', 'PFE', 'KO', 'PEP', 'T', 'CSCO', 'WMT', 'INTC', 'CVX', 'MRK', 'C', 'GS', 'BA', 'MCD', 'IBM', 'GE', 'FDX', 'CAT', 'MMM', 'RTX', 'LMT', 'TMO', 'MDT', 'HON', 'LOW', 'DHR', 'AMGN', 'GILD', 'SBUX', 'BKNG', 'ADP', 'BLK', 'SPGI', 'MS', 'USB', 'PNC', 'SCHW', 'CB', 'AIG', 'AON', 'TRV', 'AXP', 'ALL', 'CME', 'ICE', 'NDAQ', 'VLO', 'PSX', 'COP', 'EOG', 'OXY', 'SLB', 'HAL', 'KMI', 'WMB', 'OKE', 'MPC', 'HES', 'FANG', 'DVN', 'APA', 'PXD', 'XEC', 'CXO', 'NBL', 'MRO', 'NFX', 'RRC', 'SWN', 'AR', 'CHK', 'CPE', 'CRK', 'SM', 'MTDR', 'LPI', 'WPX', 'QEP', 'WLL', 'OAS', 'NOG', 'CDEV', 'REI', 'SN', 'GST', 'HK', 'EXXI', 'MEMP', 'LGCY', 'BBG', 'BCEI', 'DNR', 'SGY', 'SNMP', 'VNR', 'VNRAP', 'VNRBP', 'VNRCP', 'VNRDP', 'VNRGP', 'VNRHP', 'VNRIP', 'VNRJP', 'VNRKP', 'VNRLP', 'VNRMP', 'VNROP', 'VNRPP', 'VNRQP', 'VNRRP', 'VNRSP', 'VNRT', 'VNRUP', 'VNRVP', 'VNRWP', 'VNRXP', 'VNRY', 'VNRZ', 'BRK-B', 'REGN', 'VRTX', 'ISRG', 'ILMN', 'BMY', 'ZTS', 'ABT', 'ABBV', 'TMO', 'DHR', 'SYK', 'EW', 'ALGN', 'IDXX', 'STE', 'PKI', 'MTD', 'BIO', 'A', 'WAT', 'TECH', 'QGEN', 'RGEN', 'LH', 'DGX', 'EXAS', 'HOLX', 'HCA', 'UHS', 'UNH', 'CI', 'ANTM', 'CNC', 'HUM', 'MOH', 'GTS', 'MGLN', 'HQY', 'TDOC', 'CLOV', 'OSCR', 'ALC', 'COO', 'BSX', 'ZBH', 'XRAY', 'NVCR', 'PODD', 'TNDM', 'DXCM', 'SENS', 'MDT', 'SYK', 'EW', 'ABMD', 'IART', 'GMED', 'NUVA', 'OFIX', 'SPNE', 'SIBN', 'ATEC', 'OMI', 'CFMS', 'BAX', 'BCR', 'BARD', 'CRY', 'CSII', 'CUTR', 'ELMD', 'ICUI', 'IRTC', 'LMAT', 'MASI', 'MDXG', 'MMSI', 'NRC', 'NXTM', 'PEN', 'PRXL', 'SRTS', 'SXT', 'TCMD', 'TMDX', 'TRHC', 'VAPO', 'VCRA', 'VREX', 'XENT', 'ZBH', 'ZOLL'
    ],
    'Europe': [
        '^FTSE', '^GDAXI', '^FCHI', '^STOXX50E', '^SMI', 'SAP', 'SIE.DE', 'BNP.PA', 'AIR.PA', 'DTE.DE', 'BAS.DE', 'ALV.DE', 'VOW3.DE', 'RDSA.AS', 'ASML.AS', 'ADYEN.AS', 'INGA.AS', 'PHIA.AS', 'DSM.AS', 'AKZA.AS', 'RAND.AS', 'HEIA.AS', 'MT.AS', 'UNA.AS', 'WKL.AS', 'ABN.AS', 'AGN.AS', 'AAL.L', 'BARC.L', 'BP.L', 'GSK.L', 'HSBA.L', 'RIO.L', 'SHEL.L', 'VOD.L', 'AZN.L', 'DGE.L', 'LLOY.L', 'PRU.L', 'RDSB.L', 'RBS.L', 'STAN.L', 'TSCO.L', 'ULVR.L', 'BATS.L', 'BLND.L', 'CNA.L', 'CPG.L', 'CRH.L', 'EXPN.L', 'HL.L', 'IMB.L', 'ITV.L', 'JMAT.L', 'KGF.L', 'LAND.L', 'MKS.L', 'NG.L', 'REL.L', 'RR.L', 'SBRY.L', 'SGE.L', 'SSE.L', 'SVT.L', 'TW.L', 'WPP.L', 'NOVN.SW', 'ROG.SW', 'UBSG.SW', 'CSGN.SW', 'ZURN.SW', 'SLHN.SW', 'GEBN.SW', 'LONN.SW', 'SREN.SW', 'CFR.SW', 'ADEN.SW', 'UHR.SW', 'LOGN.SW', 'SCHN.SW', 'BKW.SW', 'BAS.SW', 'BOSS.DE', 'FME.DE', 'FRE.DE', 'HEN3.DE', 'LIN.DE', 'MTX.DE', 'QIA.DE', 'SDF.DE', 'WDI.DE', 'ZAL.DE'
    ],
    'Asia': [
        '^N225', '^HSI', '9988.HK', '700.HK', '2318.HK', '1299.HK', '1398.HK', '941.HK', '883.HK', '857.HK', '2600.HK', '2628.HK', '3328.HK', '3968.HK', '3988.HK', '601318.SS', '600519.SS', '601166.SS', '601398.SS', '601857.SS', '601988.SS', '601939.SS', '601628.SS', '601288.SS', '601818.SS', '601328.SS', '601688.SS', '601800.SS', '601601.SS', '601211.SS', '601012.SS', '601555.SS', '601336.SS', '601899.SS', '601888.SS', '6862.T', '6501.T', '6758.T', '7203.T', '7267.T', '8035.T', '8058.T', '8306.T', '8316.T', '8411.T', '8604.T', '8766.T', '9432.T', '9433.T', '9434.T', '9984.T', '4502.T', '4503.T', '4507.T', '4519.T', '4523.T', '4528.T', '4568.T', '4578.T', '4581.T', '4901.T', '4911.T', '5108.T', '5201.T', '5401.T', '5706.T', '5802.T', '6301.T', '6502.T', '6701.T', '6752.T', '6753.T', '6754.T', '6841.T', '6902.T', '6954.T', '6971.T', '7201.T', '7261.T', '7269.T', '7270.T', '7731.T', '7751.T', '8001.T', '8002.T', '8031.T', '8053.T', '8058.T', '8303.T', '8304.T', '8306.T', '8316.T', '8411.T', '8601.T', '8604.T', '8766.T', '8801.T', '8802.T', '8803.T', '9001.T', '9005.T', '9007.T', '9008.T', '9009.T', '9020.T', '9021.T', '9022.T', '9024.T', '9025.T', '9027.T', '9028.T', '9029.T', '9031.T', '9032.T', '9033.T', '9034.T', '9035.T', '9036.T', '9037.T', '9038.T', '9039.T', '9040.T', '9041.T', '9042.T', '9043.T', '9044.T', '9045.T', '9046.T', '9047.T', '9048.T', '9049.T', '9050.T', '9051.T', '9052.T', '9053.T', '9054.T', '9055.T', '9056.T', '9057.T', '9058.T', '9059.T', '9060.T', '9061.T', '9062.T', '9063.T', '9064.T', '9065.T', '9066.T', '9067.T', '9068.T', '9069.T', '9070.T', '9071.T', '9072.T', '9073.T', '9074.T', '9075.T', '9076.T', '9077.T', '9078.T', '9079.T', '9080.T', '9081.T', '9082.T', '9083.T', '9084.T', '9085.T', '9086.T', '9087.T', '9088.T', '9089.T', '9090.T', '9091.T', '9092.T', '9093.T', '9094.T', '9095.T', '9096.T', '9097.T', '9098.T', '9099.T'
    ],
    'Africa': [
        'JSE:J200', 'JSE:J203', 'JSE:J250', 'JSE:J257', 'JSE:J580', 'JSE:J330', 'JSE:J430', 'JSE:J520', 'JSE:J540', 'JSE:J560', 'JSE:J590', 'JSE:J790', 'NSEASI', 'EGX30', 'EGX70', 'NGSEINDX', 'KEN:NASI', 'KEN:NSE20', 'KEN:NSE25', 'GSECI', 'BVMT', 'MASI', 'SEMDEX', 'TUNINDEX', 'BRVMCI', 'BRVMAC', 'BRVMSP', 'BRVMIN', 'BRVMTR', 'BRVMAG', 'BRVMFN', 'BRVMID', 'BRVMIT', 'BRVMTP', 'BRVMUC', 'BRVMPR', 'BRVMEN', 'BRVMIN', 'BRVMTP', 'BRVMUC', 'BRVMPR', 'BRVMEN'
    ],
    'Middle East': [
        'TASI', 'DFMGI', 'ADXGI', 'QSI', 'BLOM', 'EGX30', 'EGX70', 'KSE', 'MSM30', 'BHB', 'ASE', 'TADAWUL', 'TADAWULMT', 'TADAWULRE', 'TADAWULEN', 'TADAWULHC', 'TADAWULBS', 'TADAWULTC', 'TADAWULIN', 'TADAWULCS', 'TADAWULCO', 'TADAWULMA', 'TADAWULCE', 'TADAWULTE', 'TADAWULFO', 'TADAWULTR', 'TADAWULEN', 'TADAWULHC', 'TADAWULBS', 'TADAWULTC', 'TADAWULIN', 'TADAWULCS', 'TADAWULCO', 'TADAWULMA', 'TADAWULCE', 'TADAWULTE', 'TADAWULFO', 'TADAWULTR'
    ],
    'LATAM': [
        'IBOV', 'MEXBOL', 'COLCAP', 'IGPA', 'BVL', 'MERVAL', 'IPSA', 'IPC', 'IBRA', 'IBRX', 'IBXX', 'IBOVESPA', 'IBOVESPAF', 'IBOVESPAI', 'IBOVESPAM', 'IBOVESPAP', 'IBOVESPAS', 'IBOVESPAT', 'IBOVESPAU', 'IBOVESPAV', 'IBOVESPAW', 'IBOVESPAZ', 'BOVESPA', 'BOVESPAF', 'BOVESPAI', 'BOVESPAM', 'BOVESPAP', 'BOVESPAS', 'BOVESPAT', 'BOVESPAU', 'BOVESPAV', 'BOVESPAW', 'BOVESPAZ', 'BOVESPA', 'BOVESPAF', 'BOVESPAI', 'BOVESPAM', 'BOVESPAP', 'BOVESPAS', 'BOVESPAT', 'BOVESPAU', 'BOVESPAV', 'BOVESPAW', 'BOVESPAZ'
    ],
    'Crypto': [
        'BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD', 'XRP-USD', 'DOGE-USD', 'BNB-USD', 'AVAX-USD', 'DOT-USD', 'MATIC-USD', 'LTC-USD', 'TRX-USD', 'LINK-USD', 'ATOM-USD', 'XLM-USD', 'BCH-USD', 'UNI1-USD', 'AAVE-USD', 'EOS-USD', 'XTZ-USD', 'SAND-USD', 'AXS-USD', 'RUNE-USD', 'CAKE-USD', 'FTM-USD', 'GRT-USD', 'ENJ-USD', 'CHZ-USD', 'CRV-USD', 'COMP-USD', 'SNX-USD', 'YFI-USD', '1INCH-USD', 'ZRX-USD', 'REN-USD', 'BAL-USD', 'KNC-USD', 'CVC-USD', 'BNT-USD', 'LRC-USD', 'MKR-USD', 'SUSHI-USD', 'UMA-USD', 'DODO-USD', 'DIA-USD', 'FET-USD', 'OCEAN-USD', 'RLC-USD', 'ANT-USD', 'MLN-USD', 'STAKE-USD', 'KAVA-USD', 'AKRO-USD', 'BAND-USD', 'CTSI-USD', 'DGB-USD', 'ELF-USD', 'GNO-USD', 'IDEX-USD', 'KMD-USD', 'NMR-USD', 'PNT-USD', 'QKC-USD', 'RDN-USD', 'STMX-USD', 'TOMO-USD', 'XEM-USD', 'XVS-USD', 'ZIL-USD'
    ],
    'Commodities': [
        'GC=F', 'SI=F', 'CL=F', 'NG=F', 'HG=F', 'ZC=F', 'ZS=F', 'ZW=F', 'LE=F', 'HE=F', 'OJ=F', 'KC=F', 'SB=F', 'CT=F', 'CC=F', 'LBS=F', 'PL=F', 'PA=F', 'RB=F', 'HO=F', 'BZO=F', 'F=F', 'W=F', 'C=F', 'S=F', 'O=F', 'RR=F', 'SM=F', 'BO=F', 'L=F', 'QO=F', 'QG=F', 'QH=F', 'QW=F', 'QZ=F', 'QK=F', 'QJ=F', 'QX=F', 'QY=F', 'QF=F', 'QG=F', 'QH=F', 'QW=F', 'QZ=F', 'QK=F', 'QJ=F', 'QX=F', 'QY=F', 'QF=F'
    ],
    'Bonds': [
        'TLT', 'IEF', 'SHY', 'BND', 'AGG', 'LQD', 'HYG', 'JNK', 'MUB', 'TIP', 'BNDX', 'EMB', 'VWOB', 'SCHO', 'SCHR', 'SCHZ', 'SPAB', 'SPBO', 'SPTL', 'SPTS', 'SPHY', 'SPLB', 'SPSB', 'SPXB', 'SPMB', 'SPTI', 'SPTS', 'SPTL', 'SPTS', 'SPHY', 'SPLB', 'SPSB', 'SPXB', 'SPMB', 'SPTI', 'SPTS', 'SPTL', 'SPTS'
    ],
    'ETFs': [
        'SPY', 'IVV', 'VOO', 'QQQ', 'VTI', 'DIA', 'IWM', 'EFA', 'EEM', 'VWO', 'VEA', 'VUG', 'VTV', 'VO', 'VB', 'VYM', 'VNQ', 'VHT', 'VGT', 'XLF', 'XLY', 'XLC', 'XLI', 'XLE', 'XLB', 'XLV', 'XLU', 'XBI', 'XME', 'XOP', 'XRT', 'XHB', 'XAR', 'XSD', 'XTL', 'XSW', 'XHS', 'XHE', 'XPH', 'XSHD', 'XSHQ', 'XSLV', 'XSOE', 'XTH', 'XT', 'XWEB', 'XW', 'XWP', 'XWS', 'XWT', 'XWW', 'XWY', 'XWZ'
    ]
}

# Example equity categories (sectors, themes)
EQUITY_CATEGORIES = {
    'Sectors': ['Technology', 'Healthcare', 'Financials', 'Consumer Discretionary', 'Industrials', 'Energy', 'Materials', 'Utilities', 'Real Estate', 'Consumer Staples', 'Telecom'],
    'Themes': ['Growth', 'Value', 'Dividend', 'ESG', 'Blue Chip', 'Small Cap', 'Large Cap', 'Momentum', 'Quality', 'Low Volatility']
}


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
        if isinstance(df.columns, pd.MultiIndex):
            try:
                data = df.loc[:, (slice(None), "Adj Close")]
                data.columns = [col[0] for col in data.columns]
            except Exception:
                data = df
        else:
            data = df
    return data.dropna()

# Denoising utilities

def rolling_mean(prices, window=5):
    return prices.rolling(window=window).mean()

def zscore(prices):
    return (prices - prices.mean()) / prices.std()

def winsorize(prices, limits=[0.01, 0.99]):
    lower = prices.quantile(limits[0])
    upper = prices.quantile(limits[1])
    return prices.clip(lower, upper)

def denoise(prices):
    # Example: rolling mean + winsorization + z-score
    smoothed = rolling_mean(prices, window=5)
    clipped = winsorize(smoothed)
    return zscore(clipped)
