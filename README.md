# Amazon Market Insights

A reproducible Python analytics project exploring Amazon product listings through pricing, discount, rating and review-volume analysis. It includes a data-cleaning pipeline, derived product metrics, an interactive Streamlit dashboard, and automated tests.

> **Data scope:** The supplied dataset contains 1,465 product records and 16 fields (product, pricing, rating, reviewer and review metadata). It is a product/review snapshot, not order-level sales data. It does **not** provide transaction dates, units sold, revenue, or customer purchase histories. Therefore, this project analyzes product-market signals; it does not claim to calculate sales, revenue, sales growth, or customer lifetime value.

## Features

- Robust numeric parsing for prices stored as numbers or currency-formatted text.
- Duplicate removal and validation of required product/pricing/rating fields.
- Consistent discount percentage recalculated from actual and discounted prices.
- Derived savings amount, price ratio, rating band and text-length features.
- Category-level summary metrics.
- Interactive dashboard with category/rating/discount filters, KPI cards, charts, product explorer and CSV export.
- Unit tests for cleaning, numeric parsing and aggregation.

## Repository structure

```text
amazon-market-insights/
├── app.py
├── src/
│   └── data_pipeline.py
├── tests/
│   └── test_data_pipeline.py
├── data/
│   ├── raw/              # local input; ignored by Git
│   └── processed/        # generated outputs; ignored by Git
├── reports/figures/      # generated charts; ignored by Git
├── requirements.txt
└── README.md
```

## Dataset

Original source: [Amazon Sales Dataset on Kaggle](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset).

Download the dataset from Kaggle and place the Excel file at `data/raw/amazondataset.xlsx`. The project ZIP prepared for local use includes the provided source workbook, but `.gitignore` prevents the raw workbook and generated data from being committed. Check the dataset's Kaggle license/terms before redistributing it.

Expected core columns: `product_id`, `product_name`, `category`, `discounted_price`, `actual_price`, `rating`, and `rating_count`.

## Setup

Python 3.10+ is recommended.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Put the Kaggle file at data/raw/amazondataset.xlsx

# 4. Run the cleaning pipeline
python -m src.data_pipeline

# 5. Launch the dashboard
streamlit run app.py

# 6. Run tests
pytest -q
```

You can also upload an `.xlsx`, `.xls`, or `.csv` file directly in the dashboard.

## Data outputs

The pipeline writes:
- `data/processed/amazon_products_cleaned.csv`
- `data/processed/category_summary.csv`
- `data/processed/data_quality_summary.csv`

## Analysis questions

- Which categories have the largest number of distinct products?
- How do listed discounts vary across categories?
- Do higher discounts correspond to higher product ratings in this snapshot?
- Which products have the largest review counts?
- How do listed prices and ratings vary across the catalog?

These are descriptive associations, not causal conclusions. Rating count is used as review-volume/engagement metadata, not as verified units sold.

## GitHub publishing

Create a new public repository named `amazon-market-insights`, then from this project directory:

```bash
git init
git add .
git status
git commit -m "Build Amazon market insights analytics project"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/amazon-market-insights.git
git push -u origin main
```

Before pushing, verify `git status` does not list the raw workbook or any personal/private data. Keep the source dataset local unless its license explicitly permits redistribution.

## Resume bullet (accurate version)

**Amazon Market Insights | Python, Pandas, Streamlit, Plotly, SQL-ready CSV outputs**
- Built a reproducible Python data pipeline to clean and validate 1,465 Amazon product records, normalize pricing fields, engineer discount/savings metrics, and aggregate category-level product insights.
- Developed an interactive Streamlit dashboard with category filters, rating and discount analysis, product comparisons, and downloadable filtered data.

Adjust the row count if the cleaned output differs after running the pipeline. Do not describe this dataset as actual sales transactions.
