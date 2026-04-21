# Trader Performance vs Market Sentiment

## Overview
This project analyzes how Bitcoin market sentiment (Fear vs Greed) relates to trader behavior and performance on Hyperliquid.  

The objective is not just to compare averages, but to understand how different types of traders respond to market sentiment and how this can inform better trading decisions.

---

## Executive Summary

This analysis combines market sentiment data with trader-level activity to study how profitability, behavior, and risk change across different sentiment regimes.

### Key Findings
1. Trader performance differs between Fear and Greed conditions, both in terms of PnL and win rate.
2. Trader behavior changes with sentiment, especially in trade frequency, position size, and directional bias.
3. Segment-level analysis shows that not all traders respond the same way to market conditions.
4. Risk, measured through drawdown, provides additional insight beyond average profitability.

### Core Insight
Market sentiment is most useful when combined with trader segmentation rather than applied as a single global signal.

## Strategy Recommendations

1. Reduce position size and tighten risk controls during Fear periods to manage downside risk.

2. Increase trading activity selectively during Greed periods for trader segments with higher win rates.

3. Monitor directional exposure to avoid over-concentration in one market direction.
---

## Dataset

Two datasets were used:

1. **Bitcoin Market Sentiment (Fear/Greed Index)**
   - Date
   - Classification (Fear / Greed / Extreme values)

2. **Hyperliquid Trader Data**
   - Account
   - Trade execution details (price, size, side)
   - Closed PnL
   - Fees and positions
   - Timestamp

---

## Methodology

### Data Preparation
- Cleaned missing values and removed duplicates
- Converted timestamps to daily level
- Aligned both datasets using overlapping date ranges
- Standardized categorical variables

### Feature Engineering
- Daily trader metrics:
  - Total PnL
  - Win rate
  - Trades per day
- Behavioral features:
  - Average trade size
  - Long/short ratio
- Risk metrics:
  - Drawdown (based on cumulative PnL)

### Analysis
- Compared performance across Fear vs Greed days
- Studied behavioral changes under different sentiment regimes
- Created trader segments:
  - Large vs Small traders
  - Frequent vs Infrequent traders
  - Consistent vs Inconsistent traders

### Modeling (Bonus)
- Built a Random Forest classifier to predict next-day profitability
- Used behavioral features and sentiment signals
- Evaluated feature importance to understand predictive drivers

---

## Key Insights

### 1. Sentiment affects both performance and behavior
Fear and Greed conditions are associated with changes in both profitability and how traders behave.

### 2. Trader response is not uniform
Segment analysis shows that larger and more active traders behave differently from smaller or less active traders under the same market conditions.

### 3. Risk varies across sentiment regimes
Drawdown analysis reveals that some conditions may appear profitable but carry higher downside risk.

### 4. Behavioral signals matter
Metrics such as win rate, trade frequency, and position size provide additional predictive value beyond sentiment alone.

---

## Strategy Recommendations

1. Reduce position size and tighten risk controls during Fear periods, especially for segments with weaker performance.
2. Increase trading activity selectively, focusing on trader segments that maintain higher win rates.
3. Monitor directional bias during Greed periods to avoid overexposure to one side of the market.
4. Use sentiment as a regime filter combined with behavioral signals rather than as a standalone indicator.

---

## Business / Trading Implications

Market sentiment can be used as a contextual signal to dynamically adjust trading strategies.  

Rather than applying uniform rules, trading systems can adapt position sizing, activity levels, and risk controls based on both sentiment and trader profile. This leads to more robust and risk-aware decision-making.

---

## Dashboard

An interactive Streamlit dashboard is provided to explore:

- Performance metrics across sentiment regimes
- Trader segmentation
- Risk (drawdown) analysis
- Behavioral trends

Live application:
https://palak7890-primetrade-round0-app-streamlit-ztsnka.streamlit.app/

Run locally:

```bash
pip install -r requirements.txt
streamlit run app_streamlit.py
