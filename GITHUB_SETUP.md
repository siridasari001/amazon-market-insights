# GitHub publishing checklist

## Repository settings
- Repository name: `amazon-market-insights`
- Suggested description: `Python data pipeline and interactive dashboard for Amazon product pricing, discounts, ratings, and review analytics.`
- Suggested topics: `python`, `pandas`, `data-analytics`, `data-cleaning`, `streamlit`, `plotly`, `exploratory-data-analysis`, `ecommerce`

## Publish from this folder
```bash
git init
git add .
git status
```
Confirm `data/raw/amazondataset.xlsx` and `data/processed/` are NOT staged. Then:
```bash
git commit -m "Build Amazon market insights analytics project"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/amazon-market-insights.git
git push -u origin main
```

## Suggested GitHub About text
Amazon product-market analytics with a reproducible Pandas cleaning pipeline, discount and pricing feature engineering, category summaries, and an interactive Streamlit dashboard.

## Suggested pinned-repository tagline
Turning product catalog and review metadata into actionable market insights.

## Before sharing
- Add a dashboard screenshot after running `streamlit run app.py`.
- Confirm Kaggle dataset license/terms before making the workbook public.
- Do not commit private credentials, user-specific data, or raw datasets unless redistribution is permitted.
