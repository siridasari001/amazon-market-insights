
from pathlib import Path
import io

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_pipeline import load_dataset, clean_dataset


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Amazon Market Insights",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛒 Amazon Market Insights")

st.caption(
    "An interactive e-commerce analytics platform for exploring "
    "Amazon product pricing, discounts, ratings, and customer reviews."
)


# ============================================================
# 2. CUSTOM DASHBOARD STYLING
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }

        [data-testid="stMetric"] {
            background-color: var(--secondary-background-color);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.2);
        }

        [data-testid="stMetricLabel"] {
            font-size: 14px;
            font-weight: 600;
        }

        [data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 700;
        }

        h1 {
            font-weight: 750;
        }

        h2, h3 {
            font-weight: 650;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,0.2);
        }

        div[data-testid="stDownloadButton"] button {
            border-radius: 8px;
            font-weight: 600;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 3. DATA LOADING AND PREPROCESSING
# ============================================================

@st.cache_data
def prepare(
    uploaded_bytes: bytes | None,
    uploaded_name: str | None,
    local_path: str
):
    """
    Load the Amazon dataset from an uploaded file
    or the default local dataset.

    Supports CSV, XLS, and XLSX formats.
    """

    if uploaded_bytes is not None:

        file = io.BytesIO(uploaded_bytes)

        if uploaded_name and uploaded_name.lower().endswith(".csv"):
            raw = pd.read_csv(file)
        else:
            raw = pd.read_excel(file)

    else:
        raw = load_dataset(local_path)

    return clean_dataset(raw)


# ============================================================
# 4. SIDEBAR - DATA SOURCE
# ============================================================

with st.sidebar:

    st.header("📂 Data Source")

    uploaded = st.file_uploader(
        "Upload Amazon dataset",
        type=["xlsx", "xls", "csv"]
    )

    local = Path("data/raw/amazondataset.xlsx")

    st.caption(
        "Default dataset location: "
        "data/raw/amazondataset.xlsx"
    )

    st.divider()


# ============================================================
# 5. LOAD DATASET
# ============================================================

try:

    data = prepare(
        uploaded.getvalue() if uploaded else None,
        uploaded.name if uploaded else None,
        str(local)
    )

except Exception as exc:

    st.error("Unable to load or process the dataset.")
    st.exception(exc)
    st.stop()


if data.empty:

    st.warning("The dataset contains no records.")
    st.stop()


# ============================================================
# 6. SIDEBAR - INTERACTIVE FILTERS
# ============================================================

with st.sidebar:

    st.header("🔎 Filters")

    categories = sorted(
        data["category"].dropna().unique().tolist()
    )

    selected = st.multiselect(
        "Product Categories",
        options=categories,
        default=categories
    )

    min_rating = st.slider(
        "Minimum Rating",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1
    )

    min_discount = st.slider(
        "Minimum Discount (%)",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )

    st.divider()

    st.caption(
        "Adjust the filters to dynamically explore "
        "product performance indicators."
    )


# ============================================================
# 7. FILTER DATA
# ============================================================

view = data[
    data["category"].isin(selected)
].copy()

view = view[
    (view["rating"] >= min_rating)
    & (view["discount_percentage"] >= min_discount)
].copy()


# ============================================================
# 8. MARKET OVERVIEW - KPI METRICS
# ============================================================

st.subheader("📊 Market Overview")

c1, c2, c3, c4 = st.columns(4)

product_count = view["product_id"].nunique()

category_count = view["category"].nunique()

average_rating = (
    view["rating"].mean()
    if not view.empty else 0
)

median_discount = (
    view["discount_percentage"].median()
    if not view.empty else 0
)

c1.metric(
    "Unique Products",
    f"{product_count:,}"
)

c2.metric(
    "Categories",
    f"{category_count:,}"
)

c3.metric(
    "Average Rating",
    f"{average_rating:.2f}/5"
    if not view.empty else "—"
)

c4.metric(
    "Median Discount",
    f"{median_discount:.1f}%"
    if not view.empty else "—"
)

st.divider()


# ============================================================
# 9. EMPTY FILTER HANDLING
# ============================================================

if view.empty:

    st.info(
        "No products match the selected filters. "
        "Try adjusting your category, rating, "
        "or discount selections."
    )

    st.stop()


# ============================================================
# 10. CHART 1 - PRODUCT DISTRIBUTION BY CATEGORY
# ============================================================

st.subheader("📦 Product Distribution by Category")

st.caption(
    "Explore the distribution of unique products "
    "across different Amazon product categories."
)

category_summary = (
    view.groupby("category", as_index=False)
    .agg(
        products=("product_id", "nunique"),
        avg_rating=("rating", "mean")
    )
    .sort_values(
        "products",
        ascending=True
    )
    .tail(15)
)

fig_category = px.bar(
    category_summary,
    x="products",
    y="category",
    orientation="h",
    color="products",
    color_continuous_scale="Blues",
    labels={
        "products": "Unique Products",
        "category": "Product Category"
    },
    title="Number of Products Across Categories"
)

fig_category.update_layout(
    height=500,
    showlegend=False,
    coloraxis_showscale=False,
    margin=dict(l=20, r=30, t=65, b=35),
    xaxis_title="Number of Unique Products",
    yaxis_title="Category"
)

fig_category.update_traces(
    hovertemplate=(
        "<b>%{y}</b><br>"
        "Products: %{x:,}<extra></extra>"
    )
)

st.plotly_chart(
    fig_category,
    width="stretch"
)


# ============================================================
# 11. CHART 2 - DISCOUNT VS PRODUCT RATING
# ============================================================

st.divider()

st.subheader("🎯 Discount vs. Product Rating")

st.caption(
    "Examine how product ratings vary across different "
    "discount levels. Bubble sizes represent rating counts."
)

scatter_data = view.dropna(
    subset=[
        "discount_percentage",
        "rating"
    ]
).copy()

scatter_data["rating_count"] = (
    scatter_data["rating_count"]
    .fillna(0)
    .clip(lower=0)
)

fig_scatter = px.scatter(
    scatter_data,
    x="discount_percentage",
    y="rating",
    size="rating_count",
    color="category",
    hover_name="product_name",
    opacity=0.7,
    labels={
        "discount_percentage": "Discount (%)",
        "rating": "Product Rating",
        "category": "Category",
        "rating_count": "Rating Count"
    },
    title="Relationship Between Discounts and Customer Ratings"
)

fig_scatter.update_layout(
    height=580,
    margin=dict(l=20, r=30, t=65, b=35),
    legend_title="Product Category",
    xaxis_title="Discount Percentage",
    yaxis_title="Customer Rating"
)

fig_scatter.update_yaxes(
    range=[0, 5.2]
)

st.plotly_chart(
    fig_scatter,
    width="stretch"
)


# ============================================================
# 12. CHART 3 - PRODUCT PRICE DISTRIBUTION
# ============================================================

st.divider()

st.subheader("💰 Product Pricing Analysis")

st.caption(
    "Understand the distribution of discounted product prices "
    "across the selected products."
)

price_data = view.dropna(
    subset=["discounted_price"]
)

fig_price = px.histogram(
    price_data,
    x="discounted_price",
    nbins=40,
    color_discrete_sequence=["#4C78A8"],
    labels={
        "discounted_price": "Discounted Price",
        "count": "Number of Products"
    },
    title="Distribution of Discounted Product Prices"
)

fig_price.update_layout(
    height=500,
    margin=dict(l=20, r=30, t=65, b=35),
    bargap=0.08,
    xaxis_title="Discounted Price",
    yaxis_title="Number of Products"
)

st.plotly_chart(
    fig_price,
    width="stretch"
)


# ============================================================
# 13. CHART 4 - TOP PRODUCTS BY RATING VOLUME
# ============================================================

st.divider()

st.subheader("⭐ Top Products by Rating Volume")

st.caption(
    "Identify products with the highest number of customer ratings."
)

top_products = (
    view.nlargest(
        10,
        "rating_count"
    )[
        [
            "product_name",
            "rating_count",
            "rating"
        ]
    ]
    .sort_values("rating_count")
)

fig_top = px.bar(
    top_products,
    x="rating_count",
    y="product_name",
    orientation="h",
    color="rating",
    color_continuous_scale="Viridis",
    labels={
        "rating_count": "Rating Count",
        "product_name": "Product",
        "rating": "Average Rating"
    },
    title="Top 10 Products by Customer Rating Count"
)

fig_top.update_layout(
    height=580,
    margin=dict(l=20, r=30, t=65, b=35),
    coloraxis_colorbar_title="Rating",
    xaxis_title="Number of Ratings",
    yaxis_title="Product"
)

st.plotly_chart(
    fig_top,
    width="stretch"
)


# ============================================================
# 14. PRODUCT EXPLORER
# ============================================================

st.divider()

st.subheader("🔍 Product Explorer")

st.caption(
    "Search and explore individual products, "
    "pricing information, discounts, and customer ratings."
)

search_term = st.text_input(
    "Search Products",
    placeholder="Enter a product name or keyword..."
)

explorer_data = view.copy()

if search_term:

    explorer_data = explorer_data[
        explorer_data["product_name"]
        .astype(str)
        .str.contains(
            search_term,
            case=False,
            na=False
        )
    ]


display_columns = [
    "product_name",
    "category",
    "actual_price",
    "discounted_price",
    "discount_percentage",
    "rating",
    "rating_count",
    "product_link"
]

columns = [
    col for col in display_columns
    if col in explorer_data.columns
]

if explorer_data.empty:

    st.info(
        "No products found for your search."
    )

else:

    sorted_explorer = explorer_data.sort_values(
        "rating_count",
        ascending=False
    )

    st.dataframe(
        sorted_explorer[columns],
        width="stretch",
        hide_index=True
    )

    st.caption(
        f"Showing {len(explorer_data):,} product records."
    )


# ============================================================
# 15. DOWNLOAD FILTERED DATA
# ============================================================

st.divider()

st.subheader("📥 Export Data")

csv_data = explorer_data[columns].to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Products (CSV)",
    data=csv_data,
    file_name="amazon_products_filtered.csv",
    mime="text/csv"
)


# ============================================================
# 16. BUSINESS INTERPRETATION
# ============================================================

st.divider()

st.subheader("💡 About This Analysis")

st.markdown(
    """
    This dashboard transforms Amazon product listing and
    customer review data into interactive market insights.

    The analysis focuses on:

    - **Product Distribution:** Understand the representation
      of products across different categories.
    - **Pricing Analysis:** Explore discounted product prices
      and their distribution.
    - **Discount Analysis:** Examine the relationship between
      product discounts and customer ratings.
    - **Customer Ratings:** Investigate product ratings and
      rating-volume patterns.
    - **Product Exploration:** Search, compare, and export
      product-level information.

    ### Business Applications

    The insights can support:

    - Product positioning and merchandising decisions.
    - Pricing and discount strategy evaluation.
    - Category-level market comparisons.
    - Product research and competitive analysis.

    ### Data Limitations

    This dataset represents a product-listing and review
    snapshot. It does not contain order-level transactions,
    sales dates, units sold, revenue, or customer-level
    purchase history.

    Therefore, this project analyzes product-market indicators
    rather than actual sales performance or revenue growth.
    """
)


# ============================================================
# 17. FOOTER
# ============================================================

st.divider()

st.caption(
    "Amazon Market Insights | "
    "Python • Pandas • Streamlit • Plotly"
)
