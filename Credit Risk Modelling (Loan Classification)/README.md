## Project overview
This project trains and evaluates machine learning models to predict loan default / loan status. It includes:
- Data loading and EDA
- Preprocessing pipelines for numeric and categorical features
- Baseline models (Logistic Regression, Random Forest, XGBoost)
- Optional hyperparameter tuning with RandomizedSearchCV
- Model evaluation (ROC AUC, precision/recall, confusion matrix)
- SHAP explanations for the best XGBoost model
- Saving model and preprocessor artifacts with joblib

Dataset: `loan_detection.csv` (place in repository root). The notebook/script uses a target column variable `Loan_Status_label` by default — update if your CSV uses a different column name.

## Repository structure
- `final_model.ipynb` — main notebook (clean, documented steps + SHAP analysis)
- `test.py` — script version of the pipeline (executable)
- `loan_detection.csv` — dataset (not included in repo; add before running)
- `best_xgb_credit_risk_model.joblib` — saved best model (after running)
- `preprocessor.joblib` — saved preprocessing pipeline (after running)
- `README.md` — this file
- `requirements.txt` — (recommended) Python package list

## Requirements
Recommended minimal packages (example):
- Python 3.8+
- pandas, numpy, matplotlib, seaborn
- scikit-learn >= 1.0
- xgboost
- shap
- joblib
Install with:
Windows (PowerShell / cmd):
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Or:
```
pip install pandas numpy scikit-learn xgboost shap joblib matplotlib seaborn
```

## Quick start
1. Place `loan_detection.csv` in the repo root.
2. Activate your virtual environment and install dependencies.
3. Open `final_model.ipynb` in VS Code or Jupyter and run cells sequentially.
   - Or run `python test.py` if you prefer script mode (ensure test.py has top-level invocation guards or adapt accordingly).

## Expected outputs / artifacts
- Trained models printed & evaluated in notebook outputs
- Saved artifacts:
  - `best_xgb_credit_risk_model.joblib`
  - `preprocessor.joblib`

## Notes & troubleshooting
- Target column: change `target_col = 'Loan_Status_label'` if CSV uses a different name to avoid KeyError.
- OneHotEncoder: older scikit-learn versions use `sparse=False` (not `sparse_output`). If you see a TypeError, change the call accordingly.
- Feature names: `ColumnTransformer.get_feature_names_out()` and `OneHotEncoder.get_feature_names_out()` are available in sklearn >= 1.0. If missing, update scikit-learn or use a fallback to build feature names manually.
- SHAP: newer usage uses `shap.Explainer(...)` returning an `Explanation` object. If plotting errors occur (beeswarm requires Explanation), wrap numeric arrays into `shap.Explanation` or use `shap.TreeExplainer` for tree models.
- If training is slow, reduce dataset size / parameter grid or comment out hyperparameter tuning cells.

## Reproducibility tips
- Set `random_state=42` in model and CV objects (already used in the notebook).
- Lock package versions via `pip freeze > requirements.txt` after successful runs.

## License & attribution
- Suggested license: MIT (choose as needed).
- Data source: add dataset licensing / attribution here.

If you want, I can generate a `requirements.txt` with pinned versions that match your environment or commit `final_model.ipynb` into the repo with cleaned explanatory cells.