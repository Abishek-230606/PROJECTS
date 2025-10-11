import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import (roc_auc_score, roc_curve, confusion_matrix, classification_report,
                             precision_recall_curve, average_precision_score)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import shap
import joblib
import seaborn as sns

# Cell 2 & 3: Load data and Quick EDA
df = pd.read_csv('loan_detection.csv')
print("Shape:", df.shape)
print("\nColumn Names:\n", df.columns.tolist())
# Cell 3: Quick EDA summary
print(df.head())
print(df.info())
print(df.describe(include='all').T)

# Check target distribution - replace 'target' below with actual target column name (e.g., 'loan_status' or 'default')
target_col = 'Loan_Status_label'
  # <-- CHANGE this to the actual column name in your CSV
if target_col not in df.columns:
    print("WARNING: update target_col variable to the correct target column name from df.columns above.")
else:
    print("Target distribution:")
    print(df[target_col].value_counts())
    print("Proportions:")
    print(df[target_col].value_counts(normalize=True))

# Cell 4: Missing values and duplicate check
missing = df.isnull().sum().sort_values(ascending=False)
missing = missing[missing>0]
missing
print("Duplicates:", df.duplicated().sum())

# Cell 5: Identify numeric and categorical features
# You may need to adjust these lists based on your dataset observations
num_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()
cat_cols = df.select_dtypes(include=['object','category']).columns.tolist()
# remove target from features
if target_col in num_cols: num_cols.remove(target_col)
if target_col in cat_cols: cat_cols.remove(target_col)
print("Numeric:", num_cols)
print("Categorical:", cat_cols)

# Cell 6: Preprocessing pipeline
num_pipeline = Pipeline(steps=[
    ('impute', SimpleImputer(strategy='median')),
    ('scale', StandardScaler())
])

cat_pipeline = Pipeline(steps=[
    ('impute', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])


preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipeline, num_cols),
    ('cat', cat_pipeline, cat_cols)
])

# Cell 7: Train-test split (stratified)
X = df.drop(columns=[target_col])
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
print(X_train.shape, X_test.shape)

# Cell 8: Logistic Regression baseline
pipe_lr = Pipeline(steps=[('pre', preprocessor),
                          ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))])
pipe_lr.fit(X_train, y_train)
y_pred_lr = pipe_lr.predict(X_test)
y_proba_lr = pipe_lr.predict_proba(X_test)[:,1]
print("Logistic Regression - ROC AUC:", roc_auc_score(y_test, y_proba_lr))
print(classification_report(y_test, y_pred_lr))

# Cell 9: Random Forest baseline
pipe_rf = Pipeline(steps=[('pre', preprocessor),
                          ('clf', RandomForestClassifier(n_estimators=200, class_weight='balanced', random_state=42))])
pipe_rf.fit(X_train, y_train)
y_proba_rf = pipe_rf.predict_proba(X_test)[:,1]
y_pred_rf = pipe_rf.predict(X_test)
print("Random Forest - ROC AUC:", roc_auc_score(y_test, y_proba_rf))
print(classification_report(y_test, y_pred_rf))

# Cell 10: XGBoost baseline (uses scale_pos_weight if imbalance)
# compute scale_pos_weight
pos = sum(y_train==1)
neg = sum(y_train==0)
scale_pos_weight = neg / pos if pos>0 else 1
pipe_xgb = Pipeline(steps=[('pre', preprocessor),
                           ('clf', xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss',
                                                     scale_pos_weight=scale_pos_weight, random_state=42))])
pipe_xgb.fit(X_train, y_train)
y_proba_xgb = pipe_xgb.predict_proba(X_test)[:,1]
y_pred_xgb = pipe_xgb.predict(X_test)
print("XGBoost - ROC AUC:", roc_auc_score(y_test, y_proba_xgb))
print(classification_report(y_test, y_pred_xgb))

# Cell 12: Hyperparameter tuning example for RandomForest
param_dist = {
    'clf__n_estimators': [100, 200, 400],
    'clf__max_depth': [None, 6, 10, 20],
    'clf__min_samples_split': [2, 5, 10],
    'clf__min_samples_leaf': [1, 2, 4]
}
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
search_rf = RandomizedSearchCV(pipe_rf, param_distributions=param_dist, n_iter=20, cv=skf, scoring='roc_auc', n_jobs=-1, random_state=42)
search_rf.fit(X_train, y_train)
print("Best RF params:", search_rf.best_params_)
print("Best RF cv ROC AUC:", search_rf.best_score_)
best_rf = search_rf.best_estimator_

# Cell 13: Hyperparameter tuning example for XGBoost (randomized)
param_dist_xgb = {
    'clf__n_estimators': [100,200,400],
    'clf__max_depth': [3,5,7,10],
    'clf__learning_rate': [0.01, 0.05, 0.1],
    'clf__subsample': [0.6, 0.8, 1],
    'clf__colsample_bytree': [0.6, 0.8, 1],
    'clf__reg_alpha': [0, 0.01, 0.1],
}
search_xgb = RandomizedSearchCV(pipe_xgb, param_distributions=param_dist_xgb, n_iter=30, cv=skf, scoring='roc_auc', n_jobs=-1, random_state=42)
search_xgb.fit(X_train, y_train)
print("Best XGB params:", search_xgb.best_params_)
print("Best XGB cv ROC AUC:", search_xgb.best_score_)
best_xgb = search_xgb.best_estimator_

# Cell 14: Evaluation function
def evaluate_model(model, X_test, y_test, name='Model'):
    y_proba = model.predict_proba(X_test)[:,1]
    y_pred = model.predict(X_test)
    auc = roc_auc_score(y_test, y_proba)
    ap = average_precision_score(y_test, y_proba)
    print(f"{name} - ROC AUC: {auc:.4f}, PR AUC (avg precision): {ap:.4f}")
    print(classification_report(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d')
    plt.title(f'{name} Confusion Matrix')
    plt.show()
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    plt.plot(fpr, tpr, label=f'{name} (AUC={auc:.3f})')
    plt.plot([0,1],[0,1],'--')
    plt.xlabel('FPR'); plt.ylabel('TPR'); plt.legend(); plt.show()
    
# Evaluate best models
evaluate_model(best_rf, X_test, y_test, 'Best RF')
evaluate_model(best_xgb, X_test, y_test, 'Best XGB')
evaluate_model(pipe_lr, X_test, y_test, 'Logistic Regression (baseline)')

# Cell 15: SHAP explanations (on the preprocessed feature matrix)
# The preprocessor is already fitted as part of the best_xgb pipeline.
# We extract this fitted preprocessor to ensure consistency for SHAP analysis.
fitted_preprocessor = best_xgb.named_steps['pre']

# Transform the train and test data using the same fitted preprocessor the model used.
X_train_pre = fitted_preprocessor.transform(X_train)
X_test_pre = fitted_preprocessor.transform(X_test)

# Get feature names directly from the fitted preprocessor.
# This is the robust way to get names for all columns (numeric and one-hot encoded).
feature_names = fitted_preprocessor.get_feature_names_out()
print("Total features after preprocessing:", len(feature_names))

# Use shap.Explainer for XGBoost.
# The explainer takes the trained classifier and the preprocessed training data (as background).
explainer = shap.Explainer(best_xgb.named_steps['clf'], X_train_pre)

# Calculate SHAP values on the preprocessed test data.
shap_values = explainer(X_test_pre)
shap.summary_plot(shap_values, X_test_pre, feature_names=feature_names)

# Cell 16: Save the best model
joblib.dump(best_xgb, 'best_xgb_credit_risk_model.joblib')
# Save the preprocessor separately if needed
joblib.dump(preprocessor, 'preprocessor.joblib')
