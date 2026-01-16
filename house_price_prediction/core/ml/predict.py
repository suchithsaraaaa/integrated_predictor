# Imports moved inside functions for lazy loading (Memory Optimization)

import os

# Use absolute path relative to this file to avoid CWD issues
MODEL_PATH = os.path.join(os.path.dirname(__file__), "price_model.pkl")
_model = None

FEATURE_COLUMNS = [
    "area_sqft",
    "bedrooms",
    "bathrooms",
    "crime",
    "traffic",
    "accessibility",
    "year",
]


def load_model():
    global _model
    if _model is None:
        import joblib
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_price(features: list):
    import pandas as pd
    df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    model = load_model()
    return model.predict(df)
