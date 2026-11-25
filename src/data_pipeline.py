"""Cleaning and feature engineering for the Amazon product-review dataset."""
from __future__ import annotations

from pathlib import Path
import re
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {"product_id", "product_name", "category", "discounted_price",
                    "actual_price", "rating", "rating_count"}

def parse_numeric(series: pd.Series) -> pd.Series:
    """Convert numbers stored as text (including currency symbols/commas) to floats."""
    cleaned = (series.astype("string")
               .str.replace(r"[^\d.\-]", "", regex=True)
               .replace("", pd.NA))
    return pd.to_numeric(cleaned, errors="coerce")

def load_dataset(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}. Download the Kaggle dataset and place it at data/raw/amazondataset.xlsx."
        )
    if path.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(path)
    elif path.suffix.lower() == ".csv":
        frame = pd.read_csv(path)
    else:
        raise ValueError("Supported input formats are .xlsx, .xls, and .csv")
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return frame

def clean_dataset(raw: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy; do not mutate the caller's DataFrame."""
    df = raw.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    # Standardize text without discarding review/product context.
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    for col in ["discounted_price", "actual_price", "rating", "rating_count"]:
        df[col] = parse_numeric(df[col])

    # The source stores discount_percentage as a fraction (e.g. 0.64),
    # while some copies store it as a percentage (64). Normalize to 0–100.
    if "discount_percentage" in df:
        discount = parse_numeric(df["discount_percentage"])
        df["discount_percentage"] = np.where(discount <= 1, discount * 100, discount)
    else:
        df["discount_percentage"] = np.nan

    # Remove exact duplicate rows and rows without usable core product/pricing fields.
    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)
    df = df.dropna(subset=["product_id", "product_name", "category",
                           "discounted_price", "actual_price", "rating"])
    df = df[(df["actual_price"] > 0) & (df["discounted_price"] >= 0)]
    df = df[df["rating"].between(0, 5)]
    if "rating_count" in df:
        df["rating_count"] = df["rating_count"].fillna(0).clip(lower=0)

    df["savings_amount"] = (df["actual_price"] - df["discounted_price"]).round(2)
    # Recalculate from prices to avoid inconsistent source percentages.
    df["discount_percentage"] = (
        df["savings_amount"] / df["actual_price"] * 100
    ).clip(lower=0, upper=100).round(2)
    df["price_ratio"] = (df["discounted_price"] / df["actual_price"]).round(4)
    df["rating_band"] = pd.cut(
        df["rating"], bins=[-0.001, 2.5, 3.5, 4.0, 4.5, 5.001],
        labels=["Poor", "Below average", "Average", "Good", "Excellent"]
    ).astype("string")
    if "about_product" in df:
        df["description_length"] = df["about_product"].fillna("").str.len()
    if "review_content" in df:
        df["review_text_length"] = df["review_content"].fillna("").str.len()

    df.attrs["duplicates_removed"] = duplicates_removed
    return df.reset_index(drop=True)

def build_category_summary(clean: pd.DataFrame) -> pd.DataFrame:
    return (clean.groupby("category", dropna=False)
            .agg(product_count=("product_id", "nunique"),
                 avg_rating=("rating", "mean"),
                 median_discount_pct=("discount_percentage", "median"),
                 avg_discounted_price=("discounted_price", "mean"),
                 total_rating_count=("rating_count", "sum"))
            .reset_index()
            .sort_values(["product_count", "avg_rating"], ascending=[False, False]))

def run_pipeline(input_path: str | Path, output_dir: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = load_dataset(input_path)
    clean = clean_dataset(raw)
    summary = build_category_summary(clean)
    clean.to_csv(output_dir / "amazon_products_cleaned.csv", index=False)
    summary.to_csv(output_dir / "category_summary.csv", index=False)
    metrics = {
        "source_rows": int(len(raw)),
        "clean_rows": int(len(clean)),
        "rows_removed": int(len(raw) - len(clean)),
        "duplicate_rows_removed": int(clean.attrs.get("duplicates_removed", 0)),
        "unique_products": int(clean["product_id"].nunique()),
        "categories": int(clean["category"].nunique()),
    }
    pd.Series(metrics, name="value").to_csv(output_dir / "data_quality_summary.csv", header=True)
    return clean, summary

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clean Amazon product and review data.")
    parser.add_argument("--input", default="data/raw/amazondataset.xlsx")
    parser.add_argument("--output", default="data/processed")
    args = parser.parse_args()
    cleaned, category_summary = run_pipeline(args.input, args.output)
    print(f"Cleaned dataset: {len(cleaned):,} rows | {cleaned['product_id'].nunique():,} products")
    print(f"Category summary: {len(category_summary):,} categories")
