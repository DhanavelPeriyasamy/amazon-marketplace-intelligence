from __future__ import annotations

import re
from io import BytesIO
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Amazon Marketplace Intelligence", page_icon="📦", layout="wide")

REQUIRED = {"product_id", "product_name", "category"}
ALIASES = {
    "product id": "product_id", "product name": "product_name",
    "discounted price": "discounted_price", "actual price": "actual_price",
    "discount percentage": "discount_percentage", "rating count": "rating_count",
    "review title": "review_title", "review content": "review_content",
}

def money(value):
    if pd.isna(value):
        return np.nan
    cleaned = re.sub(r"[^0-9.]", "", str(value).replace(",", ""))
    try:
        return float(cleaned) if cleaned else np.nan
    except ValueError:
        return np.nan

def pct(value):
    if pd.isna(value):
        return np.nan
    cleaned = re.sub(r"[^0-9.]", "", str(value))
    try:
        return float(cleaned) if cleaned else np.nan
    except ValueError:
        return np.nan

def prepare(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [ALIASES.get(c.strip().lower(), c.strip().lower().replace(" ", "_")) for c in df.columns]
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    for col in ["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]:
        if col in df:
            df[col] = df[col].map(money if col in {"discounted_price", "actual_price"} else pct)
    if "rating" in df:
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    if "rating_count" in df:
        df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")
    df["category"] = df["category"].fillna("Uncategorised").astype(str)
    df["product_name"] = df["product_name"].fillna("Unnamed product").astype(str)
    df["discount_pct_calc"] = np.where(
        df.get("actual_price", pd.Series(index=df.index, dtype=float)).gt(0),
        (df.get("actual_price", 0) - df.get("discounted_price", 0)) / df.get("actual_price", 1) * 100,
        np.nan,
    )
    if "discount_percentage" not in df:
        df["discount_percentage"] = df["discount_pct_calc"]
    else:
        df["discount_percentage"] = df["discount_percentage"].fillna(df["discount_pct_calc"])
    df["review_text"] = (
        df.get("review_title", pd.Series("", index=df.index)).fillna("").astype(str)
        + " " + df.get("review_content", pd.Series("", index=df.index)).fillna("").astype(str)
    ).str.strip()
    positive = r"\b(good|great|excellent|love|best|amazing|perfect|worth|super|nice|awesome|satisfied)\b"
    negative = r"\b(bad|poor|worst|waste|broken|disappointed|issue|defective|damage|cheap|not working)\b"
    df["sentiment_score"] = df["review_text"].str.lower().str.count(positive) - df["review_text"].str.lower().str.count(negative)
    df["sentiment"] = np.select([df["sentiment_score"] > 0, df["sentiment_score"] < 0], ["Positive", "Negative"], default="Neutral")
    # Avoid exposing personal identifiers in the dashboard/export.
    return df.drop(columns=[c for c in ["user_id", "user_name", "username"] if c in df.columns])

def demo_data():
    return pd.DataFrame({
        "product_id": ["DEMO-01", "DEMO-02", "DEMO-03", "DEMO-04", "DEMO-05", "DEMO-06"],
        "product_name": ["Wireless headphones", "USB-C hub", "Smart LED bulb", "Laptop stand", "Bluetooth speaker", "Fitness band"],
        "category": ["Electronics|Audio", "Electronics|Accessories", "Home|Lighting", "Office|Accessories", "Electronics|Audio", "Wearables"],
        "discounted_price": [1499, 899, 499, 799, 1299, 1799],
        "actual_price": [2999, 1499, 999, 1599, 2499, 3499],
        "discount_percentage": [50, 40, 50, 50, 48, 49],
        "rating": [4.2, 4.0, 4.1, 4.3, 3.9, 4.0],
        "rating_count": [1250, 620, 880, 430, 710, 950],
        "review_title": ["Great sound", "Good value", "Nice light", "Excellent build", "Good speaker", "Works well"],
        "review_content": ["Amazing battery and great sound", "Good value for money", "Nice product and easy setup", "Excellent quality and worth it", "Good but a little bulky", "Works well and satisfied"],
    })

st.title("📦 Amazon Marketplace Intelligence")
st.caption("Product catalogue, pricing, ratings and review intelligence")
with st.sidebar:
    st.header("Data")
    uploaded = st.file_uploader("Upload Amazon catalogue CSV", type=["csv"])
    st.caption("For privacy, the source dataset is not stored in this public repository.")
    use_demo = st.checkbox("Use illustrative demo data", value=uploaded is None)

try:
    raw = pd.read_csv(uploaded) if uploaded is not None else demo_data() if use_demo else None
    if raw is None:
        st.info("Upload your CSV or enable illustrative demo data in the sidebar.")
        st.stop()
    df = prepare(raw)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

is_demo = uploaded is None
if is_demo:
    st.info("You are viewing illustrative demo data. Upload the dataset for real analysis.")

numeric = [c for c in ["discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"] if c in df]
with st.sidebar:
    st.header("Filters")
    cats = sorted(df["category"].dropna().unique().tolist())
    chosen = st.multiselect("Category", cats, default=cats)
    min_rating = st.slider("Minimum rating", 0.0, 5.0, 0.0, 0.1)
filtered = df[df["category"].isin(chosen)].copy()
if "rating" in filtered:
    filtered = filtered[filtered["rating"].fillna(0) >= min_rating]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Products", f"{filtered['product_id'].nunique():,}")
c2.metric("Categories", f"{filtered['category'].nunique():,}")
c3.metric("Average rating", f"{filtered['rating'].mean():.2f} / 5" if "rating" in filtered and filtered["rating"].notna().any() else "N/A")
c4.metric("Average discount", f"{filtered['discount_percentage'].mean():.1f}%" if "discount_percentage" in filtered and filtered["discount_percentage"].notna().any() else "N/A")

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Pricing & categories", "Customer voice", "Product explorer"])
with tab1:
    left, right = st.columns(2)
    if "category" in filtered:
        cat_counts = filtered.groupby("category")["product_id"].nunique().nlargest(12).sort_values()
        left.plotly_chart(px.bar(cat_counts, orientation="h", title="Top categories by product count", labels={"value":"Products","category":"Category"}), use_container_width=True)
    if "rating" in filtered:
        right.plotly_chart(px.histogram(filtered, x="rating", nbins=20, title="Product rating distribution", range_x=[0,5]), use_container_width=True)
    st.subheader("Data quality snapshot")
    quality = pd.DataFrame({"Metric":["Rows","Unique products","Missing ratings","Missing prices"],"Value":[len(filtered),filtered["product_id"].nunique(),filtered["rating"].isna().sum() if "rating" in filtered else len(filtered),filtered["discounted_price"].isna().sum() if "discounted_price" in filtered else len(filtered)]})
    st.dataframe(quality, hide_index=True, use_container_width=True)
with tab2:
    left, right = st.columns(2)
    if "discount_percentage" in filtered:
        left.plotly_chart(px.histogram(filtered, x="discount_percentage", nbins=25, title="Discount distribution"), use_container_width=True)
    if {"actual_price","discounted_price"}.issubset(filtered.columns):
        price_df = filtered.dropna(subset=["actual_price","discounted_price"])
        right.plotly_chart(px.scatter(price_df, x="actual_price", y="discounted_price", color="category", hover_name="product_name", title="Actual vs discounted price"), use_container_width=True)
    if "category" in filtered and "discount_percentage" in filtered:
        summary = filtered.groupby("category", as_index=False).agg(products=("product_id","nunique"), avg_discount=("discount_percentage","mean"), avg_rating=("rating","mean"))
        st.dataframe(summary.sort_values("products", ascending=False), hide_index=True, use_container_width=True)
with tab3:
    if "sentiment" in filtered:
        sentiment = filtered["sentiment"].value_counts().rename_axis("Sentiment").reset_index(name="Products / review rows")
        left, right = st.columns(2)
        left.plotly_chart(px.pie(sentiment, names="Sentiment", values="Products / review rows", title="Keyword-based sentiment mix"), use_container_width=True)
        if "rating" in filtered:
            right.plotly_chart(px.box(filtered, x="sentiment", y="rating", title="Rating by sentiment label"), use_container_width=True)
        st.caption("Sentiment is a transparent keyword heuristic, not a validated NLP classifier.")
    else:
        st.info("No review text columns were found.")
with tab4:
    query = st.text_input("Search product name")
    view = filtered[filtered["product_name"].str.contains(query, case=False, na=False)] if query else filtered
    display_cols = [c for c in ["product_id","product_name","category","actual_price","discounted_price","discount_percentage","rating","rating_count","sentiment"] if c in view]
    st.dataframe(view[display_cols], hide_index=True, use_container_width=True)
    st.download_button("Download filtered products (CSV)", view[display_cols].to_csv(index=False).encode("utf-8"), "filtered_products.csv", "text/csv")

st.divider()
st.caption("Analytical note: catalogue and review snapshots do not represent sales, revenue, profit, inventory or unique customers.")
