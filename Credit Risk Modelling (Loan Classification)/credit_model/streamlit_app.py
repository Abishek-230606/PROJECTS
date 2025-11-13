# credit_model/streamlit_app.py

import streamlit as st
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Credit Risk Model", layout="wide")
st.title("📊 Credit Risk Modelling — Loan Classification")

MODEL_PATH = os.path.join("credit_model", "best_model_pipeline.pkl")

# Load model
if not os.path.exists(MODEL_PATH):
    st.error("❌ Model file not found. Please run the training notebook first.")
    st.stop()

@st.cache_data
def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = load_model()

# File uploader
st.subheader("Upload CSV for Prediction")
uploaded = st.file_uploader("Upload a CSV file containing loan applicants", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    try:
        probs = model.predict_proba(df)[:, 1]
        preds = model.predict(df)

        df["prob_default"] = probs
        df["predicted_label"] = preds

        st.write("### Prediction Results")
        st.dataframe(df.head(20))

        st.download_button(
            label="Download Predictions CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="predictions.csv"
        )

    except Exception as e:
        st.error(f"⚠️ Prediction failed. Check if the CSV has the **same columns** as training data.\n\nError: {e}")

# Sidebar info
st.sidebar.header("Model Info")
st.sidebar.write(f"Loaded model from `{MODEL_PATH}`")

roc_path = os.path.join("credit_model", "roc_curve.png")
if os.path.exists(roc_path):
    st.sidebar.image(roc_path, caption="ROC Curve")

st.success("Streamlit App Ready ✔")
