# 🛒 Amazon Market Insights

### Interactive E-Commerce Product Analytics Platform

An interactive analytics platform built with **Python, Pandas, Plotly, and Streamlit** to explore Amazon product listings through pricing, discounts, customer ratings, and review-volume analysis.

[🚀 Live Dashboard](https://amazon-market-insights-9fsblybivnw35yedw4mtqg.streamlit.app/) · [📂 GitHub Repository](https://github.com/siridasari001/amazon-market-insights)

---

## 🌐 Live Demo

**Explore the deployed application:**

👉 https://amazon-market-insights-9fsblybivnw35yedw4mtqg.streamlit.app/

The application is hosted on Streamlit Community Cloud. Upload the Amazon dataset through the sidebar to interact with the dashboard.

## 📌 Project Overview

Amazon Market Insights transforms raw product listing data into structured analytical insights through data cleaning, feature engineering, exploratory analysis, and interactive visualization.

The platform allows users to investigate product distribution, compare category-level pricing patterns, examine discount and rating relationships, and explore products using interactive filters.

The project demonstrates an end-to-end data analytics workflow, from raw dataset processing to interactive dashboard deployment.

### Key Performance Indicators

The processed dataset produces the following dashboard metrics:

| Metric | Result |
|---|---:|
| Unique Products | 1,352 |
| Product Categories | 9 |
| Average Product Rating | 4.10 / 5 |
| Median Discount | 50.0% |

*Metrics reflect the processed dataset and default dashboard filters.*

## ✨ Key Features

### 1. Data Cleaning & Preprocessing
- Handles numeric values stored as numbers or currency-formatted text.
- Removes duplicate product records.
- Validates required product, pricing, and rating fields.
- Standardizes pricing and discount information.
- Generates structured, analysis-ready datasets.

### 2. Feature Engineering
Creates additional analytical attributes, including:
- Discount percentage
- Savings amount
- Price ratio
- Rating bands
- Text-length metrics

### 3. Interactive Market Dashboard

The dashboard includes four primary visualizations:

| Visualization | Analytical Purpose |
|---|---|
| Product Distribution by Category | Compares unique product listings across categories |
| Discount vs. Product Rating | Examines relationships between discounts and ratings |
| Product Pricing Analysis | Explores discounted product price distributions |
| Top Products by Rating Volume | Identifies products with the highest rating counts |

### 4. Interactive Filters
- Filter products by category.
- Set minimum customer ratings.
- Adjust minimum discount percentages.
- Dynamically update dashboard metrics and visualizations.

### 5. Product Explorer
- Search products by name or keyword.
- Explore product categories and pricing.
- Compare discounts, ratings, and rating counts.
- Browse filtered product records.

### 6. Data Export
Download filtered product information as CSV for further analysis.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Data Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard Development | Streamlit |
| Data Sources | Excel, CSV |
| Testing | Pytest |
| Development Environment | Jupyter Notebook, VS Code |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

---

## 📊 Dataset

**Source:** [Amazon Sales Dataset – Kaggle](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)

The source dataset contains 1,465 product records and 16 fields covering product information, pricing, ratings, reviewers, and review metadata.

### Expected Core Columns

- `product_id`
- `product_name`
- `category`
- `discounted_price`
- `actual_price`
- `rating`
- `rating_count`

### Dataset Setup

The original Excel workbook is intentionally excluded from the public GitHub repository.

To use the dashboard:
1. Download the dataset from Kaggle.
2. Launch the application.
3. Upload the `.xlsx`, `.xls`, or `.csv` file through the sidebar.

For local execution, the default expected dataset location is:

`data/raw/amazondataset.xlsx`

Please review the original dataset's license and terms before redistributing it.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or later
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/siridasari001/amazon-market-insights.git

cd amazon-market-insights
```

### 2. Create a Virtual Environment

**Windows PowerShell**

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Dataset (Optional for Local Execution)

Place the downloaded Excel workbook inside:

```text
data/raw/amazondataset.xlsx
```

Alternatively, upload the dataset directly through the dashboard.

### 5. Run the Data Pipeline

```bash
python -m src.data_pipeline
```

The pipeline generates cleaned product data, category summaries, and data quality reports.

### 6. Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

The application will open locally in your browser.

### 7. Run Automated Tests

```bash
python -m pytest -v
```

---

## 📁 Project Structure

```text
amazon-market-insights/
│
├── app.py
├── requirements.txt
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── GITHUB_SETUP.md
│
├── data/
│   ├── raw/                 # Source dataset (excluded from Git)
│   └── processed/           # Generated datasets (excluded from Git)
│
├── notebooks/
│   └── amazon_market_insights.ipynb
│
├── reports/
│   └── figures/             # Generated visualizations
│
├── src/
│   ├── __init__.py
│   └── data_pipeline.py
│
└── tests/
    └── test_data_pipeline.py
```

---

## 📈 Analytical Questions

The project explores several product-market questions:

1. Which product categories contain the largest number of unique listings?
2. How do listed discounts vary across product categories?
3. Is there an observable relationship between discounts and customer ratings?
4. Which products have the highest customer rating counts?
5. How are discounted product prices distributed across the catalog?

The analysis focuses on descriptive patterns and associations rather than causal conclusions.

---

## ⚠️ Data Limitations

The dataset represents a product-listing and review snapshot, not an order-level transaction dataset.

It does not contain:
- Transaction dates
- Units sold
- Actual sales revenue
- Customer purchase histories
- Customer lifetime value

Consequently, this project focuses on product-market intelligence and e-commerce listing analytics rather than actual sales forecasting, revenue analysis, or sales growth calculations.

Rating counts are interpreted as customer feedback metadata, not verified product sales.

---

## 🔮 Future Enhancements

- Expand product-level segmentation and comparative analytics.
- Introduce additional data-quality validation checks.
- Add time-series analysis when dated product snapshots become available.
- Improve dashboard customization and filtering capabilities.
- Expand deployment and application monitoring.

---

## 👩‍💻 Author

**Siri Chandana Dasari**

Master's in Computer Science | Data Analytics | Business Intelligence | Data Engineering

- GitHub: [@siridasari001](https://github.com/siridasari001)
- Project Repository: [Amazon Market Insights](https://github.com/siridasari001/amazon-market-insights)
- Live Application: [Explore Dashboard](https://amazon-market-insights-9fsblybivnw35yedw4mtqg.streamlit.app/)

---

⭐ If you find this project interesting, feel free to explore the repository and interact with the live dashboard.

*Built with Python, data analytics, and interactive visualization.*
