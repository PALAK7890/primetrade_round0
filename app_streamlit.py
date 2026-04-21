import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Trader Sentiment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-text {
        font-size: 16px;
        color: #b0b0b0;
        margin-bottom: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    summary_df = pd.read_csv("outputs/summary_by_sentiment.csv")
    segment_df = pd.read_csv("outputs/segment_summary.csv")
    drawdown_df = pd.read_csv("outputs/drawdown_summary.csv")
    trader_df = pd.read_csv("outputs/trader_profile_segments.csv")
    return summary_df, segment_df, drawdown_df, trader_df


summary_by_sentiment, segment_summary, drawdown_summary, trader_profile = load_data()


st.markdown('<div class="main-title">Trader Performance vs Market Sentiment</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Explore how Fear and Greed sentiment affects trader performance and behavior.</div>',
    unsafe_allow_html=True
)


st.sidebar.header("Filters")

segment_choice = st.sidebar.selectbox(
    "Trader Size Segment",
    ["All", "Large Traders", "Small Traders"]
)

activity_choice = st.sidebar.selectbox(
    "Trader Activity Segment",
    ["All", "Frequent Traders", "Infrequent Traders"]
)


filtered_segment = segment_summary.copy()
filtered_traders = trader_profile.copy()

if segment_choice != "All":
    filtered_segment = filtered_segment[filtered_segment["size_segment"] == segment_choice]
    filtered_traders = filtered_traders[filtered_traders["size_segment"] == segment_choice]

if activity_choice != "All":
    filtered_traders = filtered_traders[filtered_traders["activity_segment"] == activity_choice]


fear_pnl = summary_by_sentiment.loc[
    summary_by_sentiment["sentiment_group"] == "Fear", "mean_daily_pnl"
].values

greed_pnl = summary_by_sentiment.loc[
    summary_by_sentiment["sentiment_group"] == "Greed", "mean_daily_pnl"
].values

fear_win = summary_by_sentiment.loc[
    summary_by_sentiment["sentiment_group"] == "Fear", "mean_win_rate"
].values

greed_win = summary_by_sentiment.loc[
    summary_by_sentiment["sentiment_group"] == "Greed", "mean_win_rate"
].values

fear_dd = drawdown_summary.loc[
    drawdown_summary["sentiment_group"] == "Fear", "worst_drawdown"
].values

greed_dd = drawdown_summary.loc[
    drawdown_summary["sentiment_group"] == "Greed", "worst_drawdown"
].values


st.subheader("Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric("PnL (Fear)", f"{fear_pnl[0]:.2f}" if len(fear_pnl) > 0 else "N/A")
m2.metric("PnL (Greed)", f"{greed_pnl[0]:.2f}" if len(greed_pnl) > 0 else "N/A")
m3.metric("Win Rate (Fear)", f"{fear_win[0]:.2%}" if len(fear_win) > 0 else "N/A")
m4.metric("Win Rate (Greed)", f"{greed_win[0]:.2%}" if len(greed_win) > 0 else "N/A")

st.caption(
    f"Drawdown → Fear: {fear_dd[0]:.2f} | Greed: {greed_dd[0]:.2f}"
    if len(fear_dd) > 0 and len(greed_dd) > 0 else "Drawdown not available"
)


st.subheader("Summary")
st.dataframe(summary_by_sentiment, use_container_width=True)


col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    summary_by_sentiment.plot(
        x="sentiment_group",
        y="mean_daily_pnl",
        kind="bar",
        ax=ax1,
        legend=False
    )
    ax1.set_title("PnL by Sentiment")
    plt.xticks(rotation=0)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    summary_by_sentiment.plot(
        x="sentiment_group",
        y="mean_win_rate",
        kind="bar",
        ax=ax2,
        legend=False
    )
    ax2.set_title("Win Rate by Sentiment")
    plt.xticks(rotation=0)
    st.pyplot(fig2)


col3, col4 = st.columns(2)

with col3:
    fig3, ax3 = plt.subplots()
    summary_by_sentiment.plot(
        x="sentiment_group",
        y="mean_trades_per_day",
        kind="bar",
        ax=ax3,
        legend=False
    )
    ax3.set_title("Trades per Day")
    plt.xticks(rotation=0)
    st.pyplot(fig3)

with col4:
    fig4, ax4 = plt.subplots()
    summary_by_sentiment.plot(
        x="sentiment_group",
        y="mean_trade_size_usd",
        kind="bar",
        ax=ax4,
        legend=False
    )
    ax4.set_title("Trade Size")
    plt.xticks(rotation=0)
    st.pyplot(fig4)


st.subheader("Segments")
st.write(f"Size: {segment_choice} | Activity: {activity_choice}")

left, right = st.columns([1, 1])

with left:
    st.dataframe(filtered_segment, use_container_width=True)

with right:
    fig5, ax5 = plt.subplots()

    if not filtered_segment.empty:
        if segment_choice == "All":
            pivot_seg = filtered_segment.pivot(
                index="size_segment",
                columns="sentiment_group",
                values="mean_pnl"
            )
            pivot_seg.plot(kind="bar", ax=ax5)
        else:
            ax5.bar(
                filtered_segment["sentiment_group"],
                filtered_segment["mean_pnl"]
            )

        ax5.set_title("Segment PnL")
        plt.xticks(rotation=0)
        st.pyplot(fig5)
    else:
        st.warning("No data for selected filter")


st.subheader("Risk")
r1, r2 = st.columns(2)

with r1:
    st.dataframe(drawdown_summary, use_container_width=True)

with r2:
    fig6, ax6 = plt.subplots()
    drawdown_summary.plot(
        x="sentiment_group",
        y="worst_drawdown",
        kind="bar",
        ax=ax6,
        legend=False
    )
    ax6.set_title("Worst Drawdown")
    plt.xticks(rotation=0)
    st.pyplot(fig6)


st.subheader("Traders")
st.dataframe(filtered_traders.head(20), use_container_width=True)


st.subheader("Insights")
st.markdown("""
- Performance changes between Fear and Greed
- Behavior shifts in activity and sizing
- Risk (drawdown) gives deeper insight than PnL alone
- Segment-level view is more useful than averages
""")


st.markdown("---")
st.caption("Primetrade.ai Assignment Dashboard")