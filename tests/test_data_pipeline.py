import pandas as pd
from src.data_pipeline import clean_dataset, build_category_summary, parse_numeric

def sample():
    return pd.DataFrame({
        "product_id": ["p1", "p2", "p2"],
        "product_name": ["Cable", "Charger", "Charger"],
        "category": ["Electronics", "Electronics", "Electronics"],
        "discounted_price": ["₹399", "199", "199"],
        "actual_price": ["1,099", "349", "349"],
        "discount_percentage": [0.64, 0.43, 0.43],
        "rating": [4.2, 4.0, 4.0],
        "rating_count": [100, 200, 200],
        "about_product": ["A cable", "A charger", "A charger"],
    })

def test_parse_numeric_currency():
    result = parse_numeric(pd.Series(["₹1,099", "349", None]))
    assert result.iloc[0] == 1099
    assert result.iloc[1] == 349
    assert pd.isna(result.iloc[2])

def test_clean_removes_duplicates_and_adds_features():
    cleaned = clean_dataset(sample())
    assert len(cleaned) == 2
    assert cleaned["discount_percentage"].between(0, 100).all()
    assert "savings_amount" in cleaned
    assert cleaned.attrs["duplicates_removed"] == 1

def test_category_summary():
    cleaned = clean_dataset(sample())
    summary = build_category_summary(cleaned)
    assert summary.loc[0, "product_count"] == 2
