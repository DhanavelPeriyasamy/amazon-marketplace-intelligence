from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "Dataset" / "processed" / "product_master.csv"
OUT = ROOT / "Dataset" / "processed" / "product_sentiment.csv"

POSITIVE = {"good","great","excellent","love","best","amazing","perfect","worth","super","nice","awesome","satisfied"}
NEGATIVE = {"bad","poor","worst","waste","broken","disappointed","issue","defective","damage","cheap"}

def score(text):
    words = str(text).lower().split()
    return sum(w.strip(".,!?;:()[]") in POSITIVE for w in words) - sum(w.strip(".,!?;:()[]") in NEGATIVE for w in words)

if __name__ == "__main__":
    df = pd.read_csv(DATA)
    title = df.get("review_title", pd.Series("", index=df.index)).fillna("")
    body = df.get("review_content", pd.Series("", index=df.index)).fillna("")
    df["sentiment_score"] = (title.astype(str) + " " + body.astype(str)).map(score)
    df["sentiment"] = df["sentiment_score"].map(lambda x: "Positive" if x > 0 else "Negative" if x < 0 else "Neutral")
    df.to_csv(OUT, index=False)
    print(df["sentiment"].value_counts().to_dict())
