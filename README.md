# Amazon Market Insights

An interactive e-commerce analytics platform built with **Python, Pandas, Plotly, and Streamlit** to explore Amazon product listings through pricing, discounts, ratings, and review-volume analysis.

The project includes a reproducible data-cleaning pipeline, product-level feature engineering, category-level analysis, an interactive dashboard, and automated tests.

## Project Overview

Amazon Market Insights transforms raw product listing data into structured analytical insights. It helps explore product-market patterns, compare categories, investigate pricing and discount behavior, and examine customer rating and review-volume metadata.

**Data scope:** The source dataset contains 1,465 product records and 16 fields covering product information, pricing, ratings, reviewers, and review metadata.

This is a product/review snapshot, not order-level sales data. It does not contain transaction dates, units sold, revenue, or customer purchase histories. Accordingly, this project focuses on product-market signals rather than actual sales performance or revenue forecasting.

## Key Features

- **Data Cleaning:** Numeric parsing, duplicate removal, and validation of required fields.
- **Feature Engineering:** Discount percentages, savings amounts, price ratios, rating bands, and text-length metrics.
- **Category Analysis:** Category-level product counts and summary metrics.
- **Interactive Dashboard:** KPI cards, category filters, pricing and rating visualizations, and product exploration.
- **Product Explorer:** Browse and compare products using available listing attributes.
- **Data Export:** Download filtered product data as CSV.
- **Automated Testing:** Unit tests for numeric parsing, data cleaning, and category aggregation.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Data Storage | CSV, Excel |
| Testing | Pytest |
| Development | Jupyter Notebook, Git, GitHub |

## Repository Structure

```text
amazon-market-insights/
│
├── app.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
│
├── data/
│   ├── raw/                  # Local source dataset (not committed)
│   └── processed/            # Generated datasets (not committed)
│
├── notebooks/
│   └── amazon_market_insights.ipynb
│
├── reports/
│   └── figures/              # Generated visualizations
│
├── src/
│   ├── __init__.py
│   └── data_pipeline.py
│
└── tests/
    └── test_data_pipeline.py
```

## Dataset

**Source:** [Amazon Sales Dataset – Kaggle](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)

Download the dataset and place the Excel workbook at:

```text
data/raw/amazondataset.xlsx
```

Expected core columns include:

- `product_id`
- `product_name`
- `category`
- `discounted_price`
- `actual_price`
- `rating`
- `rating_count`

The raw workbook and generated data files are excluded from Git through `.gitignore`. Check the original dataset's license and terms before redistributing it.

## Getting Started

### Prerequisites

- Python 3.10 or later
- pip

### 1. Clone the repository

```bash
git clone https://github.com/siridasari001/amazon-market-insights.git
cd amazon-market-insights
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

Place `amazondataset.xlsx` inside:

```text
data/raw/
```

Alternatively, upload a supported `.xlsx`, `.xls`, or `.csv` file directly through the dashboard.

### 5. Run the data pipeline

```bash
python -m src.data_pipeline
```

The pipeline cleans the source data and generates processed datasets.

### 6. Launch the dashboard

```bash
streamlit run app.py
```

### 7. Run automated tests

```bash
python -m pytest -q
```

## Generated Outputs

The data pipeline generates:

| Output | Description |
|---|---|
| `amazon_products_cleaned.csv` | Cleaned product-level dataset with derived features |
| `category_summary.csv` | Aggregated category-level metrics |
| `data_quality_summary.csv` | Data quality and validation summary |

All generated files are saved under `data/processed/`.

## Analytical Questions

The project explores questions such as:

1. Which product categories contain the largest number of distinct listings?
2. How do listed discounts vary across categories?
3. Is there an observable relationship between listed discounts and product ratings?
4. Which products have the highest review counts?
5. How do listed prices and ratings vary across the catalog?

These analyses are descriptive. Observed relationships do not establish causation, and review counts are engagement metadata rather than verified units sold.

## Data Limitations

- The dataset represents product listings and review-related information.
- No transaction-level sales or order history is available.
- Revenue, sales growth, units sold, and customer lifetime value cannot be calculated from these fields.
- Ratings and review counts should be interpreted as customer feedback metadata, not direct measures of purchase volume.

## Future Improvements

- Add time-series analysis when dated product snapshots become available.
- Expand product-level segmentation and comparative analytics.
- Introduce additional data-quality checks and validation reports.
- Deploy the Streamlit dashboard for public interactive access.

## Author

**Siri Chandana Dasari**

[GitHub](https://github.com/siridasari001)

---

*Built as a reproducible product analytics project using Python and interactive data visualization.*
