import joblib
import pandas as pd

MODEL_PATH = "ml/price_model.pkl"
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
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_price(features: list):
    df = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    model = load_model()
    return model.predict(df)
