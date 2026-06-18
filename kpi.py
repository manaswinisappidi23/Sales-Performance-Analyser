import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Sales KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales KPI Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload Sales CSV File",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Sidebar Filters
    st.sidebar.header("Filters")

    regions = st.sidebar.multiselect(
        "Select Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    products = st.sidebar.multiselect(
        "Select Product",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    filtered_df = df[
        (df["Region"].isin(regions)) &
        (df["Product"].isin(products))
    ]

    # KPI Calculations
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_quantity = filtered_df["Quantity"].sum()
    avg_order_value = total_sales / len(filtered_df)

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
    col3.metric("📦 Quantity Sold", f"{total_quantity:,}")
    col4.metric("🛒 Avg Order Value", f"₹{avg_order_value:,.0f}")

    st.divider()

    # Sales Trend
    sales_trend = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        sales_trend,
        x="Date",
        y="Sales",
        title="Sales Trend"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Region-wise Sales
    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="Region-wise Sales",
        text_auto=True
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Product-wise Sales
    product_sales = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        product_sales,
        names="Product",
        values="Sales",
        title="Product Contribution"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Profit Analysis
    profit_region = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig4 = px.bar(
        profit_region,
        x="Region",
        y="Profit",
        title="Region-wise Profit",
        color="Profit"
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Sales Data")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("Upload a sales CSV file to begin analysis.")