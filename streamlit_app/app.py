import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Executive Retail Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color:#0E1117;
}

div[data-testid="metric-container"]{
    background-color:#1E1E1E;
    border:1px solid #2E2E2E;
    padding:20px;
    border-radius:15px;
}

[data-testid="stMetricValue"]{
    color:#00E5FF;
    font-size:30px;
}

h1,h2,h3{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------
df = pd.read_csv("C:\\Users\\Priyanka\\OneDrive\\Executive-Retail-Intelligence-Platform\\data\\raw\dataset.csv", encoding="latin1")

# Fix Date Parsing Error
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="mixed",
    errors="coerce"
)

# Remove invalid dates
df = df.dropna(subset=["Order Date"])

# Create Month Column
df["Month"] = df["Order Date"].dt.strftime("%Y-%m")

# -----------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------
st.sidebar.title("🔍 Executive Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

state = st.sidebar.multiselect(
    "State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

metric = st.sidebar.selectbox(
    "Select KPI",
    ["Sales", "Profit", "Quantity"]
)

start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max()
)

# -----------------------------------------------------
# FILTER DATA
# -----------------------------------------------------
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Segment"].isin(segment)) &
    (df["Category"].isin(category)) &
    (df["State"].isin(state)) &
    (df["Order Date"] >= pd.to_datetime(start_date)) &
    (df["Order Date"] <= pd.to_datetime(end_date))
]

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------
st.title("🏢 Executive Retail Intelligence Platform")
st.markdown("### Enterprise Sales & Profit Analytics Dashboard")

# -----------------------------------------------------
# KPI CARDS
# -----------------------------------------------------
sales = filtered_df["Sales"].sum()
profit = filtered_df["Profit"].sum()
orders = filtered_df["Order ID"].nunique()
customers = filtered_df["Customer ID"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${sales:,.0f}")
c2.metric("📈 Total Profit", f"${profit:,.0f}")
c3.metric("🛒 Orders", f"{orders:,}")
c4.metric("👥 Customers", f"{customers:,}")

st.markdown("---")

# -----------------------------------------------------
# SALES TREND
# -----------------------------------------------------
left, right = st.columns((2,1))

with left:

    st.subheader(f"📈 {metric} Trend")

    trend = (
        filtered_df.groupby("Month")[metric]
        .sum()
        .reset_index()
        .sort_values("Month")
    )

    fig = px.line(
        trend,
        x="Month",
        y=metric,
        markers=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.subheader("🌳 Revenue Contribution")

    fig2 = px.treemap(
        filtered_df,
        path=["Region","Category","Sub-Category"],
        values="Sales",
        color="Profit",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------
# TOP / BOTTOM PRODUCTS
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product Name")[metric]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        top_products,
        x=metric,
        y="Product Name",
        orientation="h",
        text_auto=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig3, use_container_width=True)

with col2:

    st.subheader("📉 Bottom 10 Products")

    bottom_products = (
        filtered_df.groupby("Product Name")[metric]
        .sum()
        .sort_values()
        .head(10)
        .reset_index()
    )

    fig4 = px.bar(
        bottom_products,
        x=metric,
        y="Product Name",
        orientation="h",
        text_auto=True,
        template="plotly_dark"
    )

    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------------------------------
# DISCOUNT ANALYSIS
# -----------------------------------------------------
st.subheader("🎯 Discount Impact on Profit")

fig5 = px.scatter(
    filtered_df,
    x="Discount",
    y="Profit",
    color="Category",
    size="Sales",
    hover_data=["Product Name"],
    template="plotly_dark"
)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------------------------
# SALES BY STATE
# -----------------------------------------------------
st.subheader("🗺️ Sales by State")

state_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .reset_index()
)

fig6 = px.bar(
    state_sales.sort_values("Sales", ascending=False),
    x="State",
    y="Sales",
    color="Sales",
    template="plotly_dark"
)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------------------------------------
# HEATMAP
# -----------------------------------------------------
st.subheader("🔥 Profitability Heatmap")

pivot = pd.pivot_table(
    filtered_df,
    values="Profit",
    index="Region",
    columns="Category",
    aggfunc="sum"
)

fig7 = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    template="plotly_dark"
)

st.plotly_chart(fig7, use_container_width=True)

# -----------------------------------------------------
# AI INSIGHTS
# -----------------------------------------------------
best_region = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .idxmax()
)

worst_category = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
    .idxmin()
)

st.subheader("🤖 AI Business Insights")

st.info(f"""
🏆 Highest profit generated by **{best_region}** region.

⚠️ **{worst_category}** category needs optimization.

📌 Review discount strategies to improve margins.

📈 Focus on top-performing products and customer segments.
""")

# -----------------------------------------------------
# DOWNLOAD REPORT
# -----------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "📥 Download Filtered Report",
    csv,
    "executive_report.csv",
    "text/csv"
)

st.caption("Built using Streamlit • Plotly • Python")