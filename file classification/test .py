# %% [markdown]
# # Employee Performance & Retention - Club Task
#
# This notebook contains a complete, step-by-step solution for the club task:
# - Data loading and preprocessing
# - Exploratory data analysis (brief)
# - Task 1: Random Forest (classification: Attrition, regression: Performance Rating)
# - Task 2: SVM (Attrition prediction with different kernels)
# - Task 3: XGBoost (Attrition prediction and hyperparameter tuning)
# - Model comparison (metrics, training time, feature importance / explainability)
#
# Instructions:
# - Put your dataset CSV file in the same folder and set `DATA_PATH` below, or provide a path/URL.
# - Run cells in order in Jupyter Notebook.

# %%
# Imports
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings('ignore')

# %%
# User should set path to dataset here
DATA_PATH = 'data.csv'  # replace with the actual filename or path

# %% [markdown]
# ## Load dataset
# We'll try to load the dataset and print a quick summary. If the file path is wrong, change `DATA_PATH`.

# %%
try:
    df = pd.read_csv(DATA_PATH)
    print('Loaded dataset with shape:', df.shape)
except Exception as e:
    raise FileNotFoundError(f"Failed to load {DATA_PATH}. Put dataset in same folder or update DATA_PATH. Error: {e}")

# %%
# Show top rows and info
display(df.head())
print('\nData info:')
df.info()
print('\nMissing values per column:')
print(df.isnull().sum())

# %% [markdown]
# ## Basic cleaning & preprocessing strategy
# Steps performed in the notebook:
# 1. Drop or fill missing values (simple strategy: drop rows with many missing or fill with median/mode).
# 2. Convert categorical columns (Department, Job Satisfaction Level, Promotion, Attrition) into numeric labels.
# 3. Feature engineering - if needed (e.g., years category, hours per week derived, etc.).
# 4. Prepare `X` and `y` for classification (Attrition) and regression (Performance Rating).

# %%
# Make a copy
data = df.copy()

# Standardize column names (strip spaces)
data.columns = [c.strip() for c in data.columns]

# Inspect expected columns
print('Columns:', list(data.columns))

# %%
# Example cleaning rules - adapt if your dataset differs
# Fill missing values for numeric with median, categorical with mode
num_cols = data.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()

for c in num_cols:
    if data[c].isnull().sum() > 0:
        data[c].fillna(data[c].median(), inplace=True)
for c in cat_cols:
    if data[c].isnull().sum() > 0:
        data[c].fillna(data[c].mode()[0], inplace=True)

print('\nAfter filling missing values:')
print(data.isnull().sum())

# %% [markdown]
# ### Encode categorical variables
# We'll label-encode simple categorical fields. For multi-class or ordinal (Job Satisfaction: Low/Medium/High) we preserve ordering manually.

# %%
le = LabelEncoder()

# Common categorical columns based on task description
# 'Department', 'Job Satisfaction Level', 'Promotion in Last 2 Years', 'Attrition'
# Map possible column name variations to expected names
col_map = {}
for c in data.columns:
    lc = c.lower()
    if 'department' in lc:
        col_map['Department'] = c
    if 'satisfaction' in lc:
        col_map['JobSatisfaction'] = c
    if 'promotion' in lc or 'promoted' in lc:
        col_map['Promotion'] = c
    if 'attrit' in lc or 'left' in lc or 'resign' in lc:
        col_map['Attrition'] = c
    if 'performance' in lc and 'rating' in lc:
        col_map['PerformanceRating'] = c

print('\nColumn mapping detected:', col_map)

# Helper function to apply label encoding safely
def safe_label_encode(df, col, mapping=None, ordered_categories=None):
    if col not in df.columns:
        return df
    if ordered_categories is not None:
        # create a categorical with order
        df[col] = pd.Categorical(df[col], categories=ordered_categories, ordered=True)
        df[col] = df[col].cat.codes
    else:
        try:
            df[col] = le.fit_transform(df[col].astype(str))
        except Exception:
            df[col] = df[col].astype('category').cat.codes
    return df

# Apply encodings
if 'Department' in col_map:
    data = safe_label_encode(data, col_map['Department'])
if 'JobSatisfaction' in col_map:
    # If job satisfaction is Low/Medium/High order it
    js_col = col_map['JobSatisfaction']
    unique_vals = data[js_col].dropna().unique()
    ordered = None
    # if typical levels present
    typical = ['Low', 'Medium', 'High']
    if all(x in unique_vals for x in typical):
        ordered = typical
    data = safe_label_encode(data, js_col, ordered_categories=ordered)
if 'Promotion' in col_map:
    # yes/no map
    pcol = col_map['Promotion']
    data[pcol] = data[pcol].astype(str).str.strip().replace({'Yes':'Yes','No':'No','yes':'Yes','no':'No'})
    data = safe_label_encode(data, pcol)
if 'Attrition' in col_map:
    acol = col_map['Attrition']
    data[acol] = data[acol].astype(str).str.strip().replace({'Yes':'Yes','No':'No','yes':'Yes','no':'No'})
    data = safe_label_encode(data, acol)

# If Performance rating exists, ensure numeric
if 'PerformanceRating' in col_map:
    pr = col_map['PerformanceRating']
    try:
        data[pr] = pd.to_numeric(data[pr])
    except Exception:
        data[pr] = data[pr].astype('category').cat.codes

    # Show processed head
    display(data.head())

# %% [markdown]
# ## Feature list selection
# We will exclude identifier columns like Employee_ID if present.

# %%
features = [c for c in data.columns if 'employee' not in c.lower()]
print('Candidate features:', features)

# Choose label columns if present
attrition_col = col_map.get('Attrition', None)
perf_col = col_map.get('PerformanceRating', None)
print('Attrition column:', attrition_col, '\nPerformance column:', perf_col)

# Basic feature set (drop label columns from features)
X_cols = [c for c in features if c not in [attrition_col, perf_col]]
print('X columns used:', X_cols)

# %% [markdown]
# ## Train/Test split & scaling helper

# %%
def prepare_data_for_classification(df, X_cols, label_col, test_size=0.2, random_state=42, scale=True):
    X = df[X_cols].copy()
    y = df[label_col].copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y, random_state=random_state)
    if scale:
        scaler = StandardScaler()
        X_train[X_train.columns] = scaler.fit_transform(X_train)
        X_test[X_test.columns] = scaler.transform(X_test)
        return X_train, X_test, y_train, y_test, scaler
    else:
        return X_train, X_test, y_train, y_test, None

# For regression
def prepare_data_for_regression(df, X_cols, label_col, test_size=0.2, random_state=42, scale=True):
    X = df[X_cols].copy()
    y = df[label_col].copy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    if scale:
        scaler = StandardScaler()
        X_train[X_train.columns] = scaler.fit_transform(X_train)
        X_test[X_test.columns] = scaler.transform(X_test)
        return X_train, X_test, y_train, y_test, scaler
    else:
        return X_train, X_test, y_train, y_test, None

# %% [markdown]
# # Task 1: Random Forest
# We'll do both:
# - Classification to predict Attrition (if column exists)
# - Regression to predict Performance Rating (if column exists)

# %%
results = {}

# Task 1a: Random Forest Classification (Attrition)
if attrition_col is not None:
    print('\n=== Random Forest Classification: Attrition ===')
    X_train, X_test, y_train, y_test, scaler = prepare_data_for_classification(data, X_cols, attrition_col)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    t0 = time.time()
    clf.fit(X_train, y_train)
    t1 = time.time()
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='binary', zero_division=0)
    rec = recall_score(y_test, y_pred, average='binary', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='binary', zero_division=0)
    print('Accuracy:', acc)
    print('Precision:', prec)
    print('Recall:', rec)
    print('F1:', f1)
    print('Training time (s):', t1 - t0)
    print('\nClassification report:\n', classification_report(y_test, y_pred))

    # Feature importance (tree-based)
    fi = pd.Series(clf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    print('\nTop features by importance:')
    display(fi.head(10))

    # Permutation importance (on test set)
    perm = permutation_importance(clf, X_test, y_test, n_repeats=10, random_state=42)
    perm_imp = pd.Series(perm.importances_mean, index=X_test.columns).sort_values(ascending=False)
    print('\nTop features by permutation importance:')
    display(perm_imp.head(10))

    results['rf_classification'] = {
        'model': clf,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1,
        'train_time': t1 - t0,
        'feature_importance': fi,
        'permutation_importance': perm_imp
    }

# Task 1b: Random Forest Regression (Performance Rating)
if perf_col is not None:
    print('\n=== Random Forest Regression: Performance Rating ===')
    X_train_r, X_test_r, y_train_r, y_test_r, scaler_r = prepare_data_for_regression(data, X_cols, perf_col)
    regr = RandomForestRegressor(n_estimators=200, random_state=42)
    t0 = time.time()
    regr.fit(X_train_r, y_train_r)
    t1 = time.time()
    y_pred_r = regr.predict(X_test_r)
    mse = mean_squared_error(y_test_r, y_pred_r)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_r, y_pred_r)
    print('RMSE:', rmse)
    print('R2:', r2)

    fi_r = pd.Series(regr.feature_importances_, index=X_train_r.columns).sort_values(ascending=False)
    print('\nTop features by importance (regression):')
    display(fi_r.head(10))

    results['rf_regression'] = {
        'model': regr,
        'rmse': rmse,
        'r2': r2,
        'train_time': t1 - t0,
        'feature_importance': fi_r
    }

# %% [markdown]
# # Task 2: Support Vector Machine (SVM) - Attrition classification
# We'll train SVMs with linear, polynomial, and RBF kernels and compare.

# %%
    if attrition_col is not None:
        print('\n=== SVM Classification (kernels comparison) ===')
        X_train_s, X_test_s, y_train_s, y_test_s, scaler_s = prepare_data_for_classification(data, X_cols, attrition_col)

        svm_kernels = ['linear', 'poly', 'rbf']
        svm_results = {}
        for kernel in svm_kernels:
            print(f'\nTraining SVM with kernel={kernel}')
            if kernel == 'poly':
                model = SVC(kernel=kernel, degree=3, probability=False, random_state=42)
            else:
                model = SVC(kernel=kernel, probability=False, random_state=42)
            t0 = time.time()
            model.fit(X_train_s, y_train_s)
            t1 = time.time()
            y_pred_s = model.predict(X_test_s)
            acc = accuracy_score(y_test_s, y_pred_s)
            prec = precision_score(y_test_s, y_pred_s, average='binary', zero_division=0)
            rec = recall_score(y_test_s, y_pred_s, average='binary', zero_division=0)
            f1 = f1_score(y_test_s, y_pred_s, average='binary', zero_division=0)
            print('Accuracy:', acc, 'Precision:', prec, 'Recall:', rec, 'F1:', f1, 'Train time:', t1 - t0)
            svm_results[kernel] = {
                'model': model,
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1': f1,
                'train_time': t1 - t0
            }

        results['svm'] = svm_results

# %% [markdown]
# # Task 3: XGBoost Classification (Attrition) + Hyperparameter tuning
# We'll run a basic XGBoost classifier and then do a RandomizedSearchCV for a few important hyperparameters.

# %%
if attrition_col is not None:
    print('\n=== XGBoost Classification & Tuning ===')
    X_train_x, X_test_x, y_train_x, y_test_x, scaler_x = prepare_data_for_classification(data, X_cols, attrition_col)
    xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    t0 = time.time()
    xgb.fit(X_train_x, y_train_x)
    t1 = time.time()
    y_pred_x = xgb.predict(X_test_x)
    acc = accuracy_score(y_test_x, y_pred_x)
    prec = precision_score(y_test_x, y_pred_x, average='binary', zero_division=0)
    rec = recall_score(y_test_x, y_pred_x, average='binary', zero_division=0)
    f1 = f1_score(y_test_x, y_pred_x, average='binary', zero_division=0)
    print('Baseline XGBoost - Accuracy:', acc, 'Precision:', prec, 'Recall:', rec, 'F1:', f1, 'Train time:', t1 - t0)

    # Hyperparameter tuning (RandomizedSearch for speed) - quick search space
    param_dist = {
        'n_estimators': [50, 100, 200, 300],
        'max_depth': [3, 4, 6, 8],
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
        'subsample': [0.6, 0.8, 1.0],
        'colsample_bytree': [0.5, 0.7, 1.0]
    }
    xgb_rs = RandomizedSearchCV(XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42),
                                param_distributions=param_dist,
                                n_iter=20,
                                scoring='accuracy',
                                cv=3,
                                verbose=1,
                                random_state=42,
                                n_jobs=-1)
    t0 = time.time()
    xgb_rs.fit(X_train_x, y_train_x)
    t1 = time.time()
    print('Best params:', xgb_rs.best_params_)
    best_xgb = xgb_rs.best_estimator_
    y_pred_xb = best_xgb.predict(X_test_x)
    acc_b = accuracy_score(y_test_x, y_pred_xb)
    prec_b = precision_score(y_test_x, y_pred_xb, average='binary', zero_division=0)
    rec_b = recall_score(y_test_x, y_pred_xb, average='binary', zero_division=0)
    f1_b = f1_score(y_test_x, y_pred_xb, average='binary', zero_division=0)
    print('Tuned XGBoost - Accuracy:', acc_b, 'Precision:', prec_b, 'Recall:', rec_b, 'F1:', f1_b, 'Tuning time:', t1 - t0)

    # Feature importance
    fi_xgb = pd.Series(best_xgb.feature_importances_, index=X_train_x.columns).sort_values(ascending=False)
    print('\nTop features by XGBoost importance:')
    display(fi_xgb.head(10))

    results['xgboost'] = {
        'baseline': {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1, 'train_time': t1 - t0},
        'tuned': {'model': best_xgb, 'accuracy': acc_b, 'precision': prec_b, 'recall': rec_b, 'f1': f1_b, 'tuning_time': t1 - t0, 'feature_importance': fi_xgb}
    }

# %% [markdown]
# ## Compare models (classification summary table)

# %%
if attrition_col is not None:
    rows = []
    # Random Forest
    if 'rf_classification' in results:
        r = results['rf_classification']
        rows.append(('RandomForest', r['accuracy'], r['precision'], r['recall'], r['f1'], r['train_time']))
    # SVM kernels
    if 'svm' in results:
        for k,v in results['svm'].items():
            rows.append((f'SVM-{k}', v['accuracy'], v['precision'], v['recall'], v['f1'], v['train_time']))
    # XGBoost tuned
    if 'xgboost' in results:
        xb = results['xgboost']['tuned']
        rows.append(('XGBoost-tuned', xb['accuracy'], xb['precision'], xb['recall'], xb['f1'], xb['tuning_time']))

    comp_df = pd.DataFrame(rows, columns=['model','accuracy','precision','recall','f1','time_s']).sort_values('accuracy', ascending=False)
    display(comp_df)

# %% [markdown]
# ## Plots: feature importance comparison (top 10)

# %%
if attrition_col is not None:
    plt.figure(figsize=(10,6))
    if 'rf_classification' in results:
        fi = results['rf_classification']['feature_importance'].head(10)
        fi.plot(kind='bar');
        plt.title('Random Forest - Top 10 feature importance')
        plt.tight_layout()
        plt.show()
    if 'xgboost' in results:
        fi2 = results['xgboost']['tuned']['feature_importance'].head(10)
        plt.figure(figsize=(10,6))
        fi2.plot(kind='bar')
        plt.title('XGBoost - Top 10 feature importance')
        plt.tight_layout()
        plt.show()

# %% [markdown]
# ## Save models (optional)
# You can save the trained models using joblib if you want to reuse later.

# %%
save_models = False
if save_models:
    import joblib
    if 'rf_classification' in results:
        joblib.dump(results['rf_classification']['model'], 'rf_classification.pkl')
    if 'rf_regression' in results:
        joblib.dump(results['rf_regression']['model'], 'rf_regression.pkl')
    if 'svm' in results:
        for k,v in results['svm'].items():
            joblib.dump(v['model'], f'svm_{k}.pkl')
    if 'xgboost' in results:
        joblib.dump(results['xgboost']['tuned']['model'], 'xgboost_tuned.pkl')
    print('Models saved')

# %% [markdown]
# ## Short notes for your submission / presentation
# - Explain preprocessing steps (missing value handling, encoding, scaling).
# - For classification tasks present Accuracy/Precision/Recall/F1 and confusion matrix.
# - For regression present RMSE and R2.
# - Discuss feature importance and present the top features for Random Forest and XGBoost.
# - For SVM show kernel comparison table (we included it above).
# - Mention hyperparameter tuning method and best params for XGBoost.

# %%
print('Notebook run complete. Check the results variables and plots above.')
