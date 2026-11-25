from pathlib import Path
import io

import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_pipeline import load_dataset, clean_dataset


# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Amazon Market Insights",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🛒 Amazon Market Insights")
st.caption(
    "An interactive e-commerce analytics platform for exploring "
    "Amazon product pricing, discounts, ratings, and customer reviews."
)


# 2. CUSTOM STYLING
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
        h1 { font-weight: 750; }
        h2, h3 { font-weight: 650; }
        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(128,128,128,0.2);
        }
        div[data-testid="stDownloadButton"] button {
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# 3. DATA LOADING
@st.cache_data
def prepare(
    uploaded_bytes: bytes | None,
    uploaded_name: str | None,
    local_path: str,
):
    """Load an uploaded CSV/Excel file or local dataset, then clean it."""
    if uploaded_bytes is not None:
        file = io.BytesIO(uploaded_bytes)
        extension = Path(uploaded_name or "").suffix.lower()

        if extension == ".csv":
            raw = pd.read_csv(file)
        elif extension in {".xlsx", ".xls"}:
            raw = pd.read_excel(file)
        else:
            raise ValueError("Upload a CSV, XLS, or XLSX file.")
    else:
        raw = load_dataset(local_path)

    return clean_dataset(raw)


# 4. SIDEBAR - DATA SOURCE
local = Path("data/raw/amazondataset.xlsx")

with st.sidebar:
    st.header("📂 Data Source")
    uploaded = st.file_uploader(
        "Upload Amazon dataset",
        type=["xlsx", "xls", "csv"],
        help="Upload the Amazon product dataset in CSV or Excel format.",
    )
    st.caption("Default dataset location: data/raw/amazondataset.xlsx")

    if local.exists():
        st.success("A local dataset was found.")
    else:
        st.info(
            "No default dataset is included in the deployed app. "
            "Upload your dataset here to get started."
        )

    st.divider()


# 5. LOAD DATASET
# The deployed app must not try to read the local workbook when it is
# absent. The source workbook is intentionally excluded from GitHub.
if uploaded is None and not local.exists():
    st.info(
        "👈 **Upload your Amazon dataset using the sidebar to get started.** "
        "The source workbook is kept out of the public GitHub repository."
    )
    st.markdown(
        """
        ### Supported files
        - Excel workbook: `.xlsx` or `.xls`
        - CSV file: `.csv`

        After uploading, the app will prepare the data and display the
        market overview, charts, product explorer, and CSV export.
        """
    )
    st.stop()

try:
    data = prepare(
        uploaded.getvalue() if uploaded is not None else None,
        uploaded.name if uploaded is not None else None,
        str(local),
    )
except Exception as exc:
    st.error("Unable to load or process the dataset.")
    st.warning(
        "Check that the file is the expected Amazon product dataset "
        "and contains the required columns."
    )
    with st.expander("Technical details"):
        st.exception(exc)
    st.stop()

if data.empty:
    st.warning("The dataset contains no records after processing.")
    st.stop()

required_columns = {
    "product_id", "product_name", "category",
    "discount_percentage", "rating", "rating_count",
}
missing_columns = required_columns.difference(data.columns)
if missing_columns:
    st.error(
        "The processed dataset is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()


# 6. SIDEBAR - FILTERS
with st.sidebar:
    st.header("🔎 Filters")
    categories = sorted(
        data["category"].dropna().astype(str).unique().tolist()
    )
    selected = st.multiselect(
        "Product Categories",
        options=categories,
        default=categories,
    )
    min_rating = st.slider(
        "Minimum Rating", 0.0, 5.0, 0.0, 0.1
    )
    min_discount = st.slider(
        "Minimum Discount (%)", 0, 100, 0, 1
    )
    st.divider()
    st.caption(
        "Adjust the filters to dynamically explore product-market indicators."
    )


# 7. FILTER DATA
view = data[data["category"].astype(str).isin(selected)].copy()
view = view[
    (pd.to_numeric(view["rating"], errors="coerce") >= min_rating)
    & (
        pd.to_numeric(view["discount_percentage"], errors="coerce")
        >= min_discount
    )
].copy()


# 8. MARKET OVERVIEW
st.subheader("📊 Market Overview")
c1, c2, c3, c4 = st.columns(4)

product_count = view["product_id"].nunique()
category_count = view["category"].nunique()
average_rating = (
    pd.to_numeric(view["rating"], errors="coerce").mean()
    if not view.empty else 0
)
median_discount = (
    pd.to_numeric(view["discount_percentage"], errors="coerce").median()
    if not view.empty else 0
)

c1.metric("Unique Products", f"{product_count:,}")
c2.metric("Categories", f"{category_count:,}")
c3.metric(
    "Average Rating",
    f"{average_rating:.2f}/5" if not view.empty else "—",
)
c4.metric(
    "Median Discount",
    f"{median_discount:.1f}%" if not view.empty else "—",
)
st.divider()


# 9. EMPTY FILTER HANDLING
if view.empty:
    st.info(
        "No products match the selected filters. Try adjusting your "
        "category, rating, or discount selections."
    )
    st.stop()


# 10. PRODUCT DISTRIBUTION BY CATEGORY
st.subheader("📦 Product Distribution by Category")
st.caption(
    "Explore the distribution of unique products across Amazon categories."
)
category_summary = (
    view.groupby("category", as_index=False)
    .agg(
        products=("product_id", "nunique"),
        avg_rating=("rating", "mean"),
    )
    .sort_values("products", ascending=True)
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
        "category": "Product Category",
    },
    title="Number of Products Across Categories",
)
fig_category.update_layout(
    height=500,
    showlegend=False,
    coloraxis_showscale=False,
    margin=dict(l=20, r=30, t=65, b=35),
    xaxis_title="Number of Unique Products",
    yaxis_title="Category",
)
fig_category.update_traces(
    hovertemplate="<b>%{y}</b><br>Products: %{x:,}<extra></extra>"
)
st.plotly_chart(fig_category, width="stretch")


# 11. DISCOUNT VS. PRODUCT RATING
st.divider()
st.subheader("🎯 Discount vs. Product Rating")
st.caption(
    "Explore ratings across discount levels. Bubble sizes represent rating counts."
)
scatter_data = view.dropna(
    subset=["discount_percentage", "rating"]
).copy()
scatter_data["rating_count"] = (
    pd.to_numeric(scatter_data["rating_count"], errors="coerce")
    .fillna(0)
    .clip(lower=0)
)
if not scatter_data.empty:
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
            "rating_count": "Rating Count",
        },
        title="Relationship Between Discounts and Customer Ratings",
    )
    fig_scatter.update_layout(
        height=580,
        margin=dict(l=20, r=30, t=65, b=35),
        legend_title="Product Category",
        xaxis_title="Discount Percentage",
        yaxis_title="Customer Rating",
    )
    fig_scatter.update_yaxes(range=[0, 5.2])
    st.plotly_chart(fig_scatter, width="stretch")
else:
    st.info("Not enough rating and discount data to display this chart.")


# 12. PRODUCT PRICE DISTRIBUTION
st.divider()
st.subheader("💰 Product Pricing Analysis")
st.caption(
    "Understand the distribution of discounted product prices."
)
price_data = view.dropna(subset=["discounted_price"]).copy()
if not price_data.empty:
    fig_price = px.histogram(
        price_data,
        x="discounted_price",
        nbins=40,
        color_discrete_sequence=["#4C78A8"],
        labels={
            "discounted_price": "Discounted Price",
            "count": "Number of Products",
        },
        title="Distribution of Discounted Product Prices",
    )
    fig_price.update_layout(
        height=500,
        margin=dict(l=20, r=30, t=65, b=35),
        bargap=0.08,
        xaxis_title="Discounted Price",
        yaxis_title="Number of Products",
    )
    st.plotly_chart(fig_price, width="stretch")
else:
    st.info("No valid discounted-price values are available for this chart.")


# 13. TOP PRODUCTS BY RATING VOLUME
st.divider()
st.subheader("⭐ Top Products by Rating Volume")
st.caption("Identify products with the highest number of customer ratings.")
top_source = view.copy()
top_source["rating_count"] = pd.to_numeric(
    top_source["rating_count"], errors="coerce"
).fillna(0)
top_products = (
    top_source.nlargest(10, "rating_count")[
        ["product_name", "rating_count", "rating"]
    ]
    .sort_values("rating_count")
)
if not top_products.empty:
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
            "rating": "Average Rating",
        },
        title="Top 10 Products by Customer Rating Count",
    )
    fig_top.update_layout(
        height=580,
        margin=dict(l=20, r=30, t=65, b=35),
        coloraxis_colorbar_title="Rating",
        xaxis_title="Number of Ratings",
        yaxis_title="Product",
    )
    st.plotly_chart(fig_top, width="stretch")
else:
    st.info("No rating-count data is available for this chart.")


# 14. PRODUCT EXPLORER
st.divider()
st.subheader("🔍 Product Explorer")
st.caption(
    "Search and explore individual products, pricing, discounts, and ratings."
)
search_term = st.text_input(
    "Search Products",
    placeholder="Enter a product name or keyword...",
)
explorer_data = view.copy()
if search_term:
    explorer_data = explorer_data[
        explorer_data["product_name"]
        .astype(str)
        .str.contains(search_term, case=False, na=False)
    ]

display_columns = [
    "product_name",
    "category",
    "actual_price",
    "discounted_price",
    "discount_percentage",
    "rating",
    "rating_count",
    "product_link",
]
columns = [
    col for col in display_columns if col in explorer_data.columns
]
if explorer_data.empty:
    st.info("No products found for your search.")
else:
    if "rating_count" in explorer_data.columns:
        sorted_explorer = explorer_data.sort_values(
            "rating_count",
            ascending=False,
            na_position="last",
        )
    else:
        sorted_explorer = explorer_data
    st.dataframe(
        sorted_explorer[columns],
        width="stretch",
        hide_index=True,
    )
    st.caption(f"Showing {len(explorer_data):,} product records.")


# 15. DOWNLOAD FILTERED DATA
st.divider()
st.subheader("📥 Export Data")
csv_data = explorer_data[columns].to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Filtered Products (CSV)",
    data=csv_data,
    file_name="amazon_products_filtered.csv",
    mime="text/csv",
)


# 16. BUSINESS INTERPRETATION
st.divider()
st.subheader("💡 About This Analysis")
st.markdown(
    """
    This dashboard transforms Amazon product listing and customer review
    data into interactive market insights.

    The analysis focuses on:

    - **Product Distribution:** Understand product representation across categories.
    - **Pricing Analysis:** Explore discounted product prices and their distribution.
    - **Discount Analysis:** Examine the relationship between discounts and ratings.
    - **Customer Ratings:** Investigate product ratings and rating-volume patterns.
    - **Product Exploration:** Search, compare, and export product-level information.

    ### Business Applications

    - Product positioning and merchandising decisions.
    - Pricing and discount strategy evaluation.
    - Category-level market comparisons.
    - Product research and competitive analysis.

    ### Data Limitations

    This dataset represents a product-listing and review snapshot. It does not
    contain order-level transactions, sales dates, units sold, revenue, or
    customer-level purchase history.

    Therefore, this project analyzes product-market indicators rather than
    actual sales performance or revenue growth.
    """
)


# 17. FOOTER
st.divider()
st.caption(
    "Amazon Market Insights | Python • Pandas • Streamlit • Plotly"
)
