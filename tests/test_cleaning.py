import importlib.util
from pathlib import Path
import pandas as pd

MODULE = Path(__file__).resolve().parents[1] / "Python" / "01_profile_and_clean.py"
spec = importlib.util.spec_from_file_location("cleaning", MODULE)
cleaning = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleaning)

def test_number_parses_currency_and_commas():
    assert cleaning.number("₹1,299.00") == 1299.0

def test_number_handles_missing():
    assert pd.isna(cleaning.number(None))

def test_clean_deduplicates_and_removes_identifiers():
    df = pd.DataFrame({"product_id":["a","a"],"product_name":["one","duplicate"],"user_id":["x","y"],"rating":["4.2","4.0"]})
    out = cleaning.clean(df)
    assert len(out) == 1
    assert "user_id" not in out.columns
    assert out.iloc[0]["rating"] == 4.2
