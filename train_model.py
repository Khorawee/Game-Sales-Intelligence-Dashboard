# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from xgboost import XGBRegressor
import joblib
from preprocessor import FullPreprocessor
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------
# Load data
# -------------------------------------------------------
def load_data():
    print("Loading data from MySQL...")
    
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "game_sales")
    
    engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    query = """
    SELECT
        v.game_name AS Name,
        p.name AS Platform,
        g.name AS Genre,
        pub.name AS Publisher,
        v.Year AS Year,
        v.NA_Sales,
        v.EU_Sales,
        v.JP_Sales,
        v.Other_Sales,
        v.Global_Sales
    FROM vgsales v
    JOIN platform p ON v.platform_id = p.id
    JOIN genre g ON v.genre_id = g.id
    JOIN publisher pub ON v.publisher_id = pub.id
    WHERE v.Global_Sales > 0
    """

    df = pd.read_sql(query, engine)
    print(f"Loaded {len(df):,} rows\n")
    return df

# -------------------------------------------------------
# Simple Feature Engineering (Minor additions)
# -------------------------------------------------------
def add_features(df):
    print("Adding simple features...")
    
    # 1. Total known sales
    df['Total_Known_Sales'] = df['NA_Sales'] + df['EU_Sales'] + df['JP_Sales'] + df['Other_Sales']
    
    # 2. Publisher track record (Average)
    publisher_avg = df.groupby('Publisher')['Global_Sales'].mean()
    df['Publisher_Avg'] = df['Publisher'].map(publisher_avg)
    
    # 3. Platform popularity
    platform_count = df.groupby('Platform').size()
    df['Platform_Count'] = df['Platform'].map(platform_count)
    
    return df

# -------------------------------------------------------
# Preprocessor (Add new features)
# -------------------------------------------------------
def build_preprocessor():
    te_cols = ["Publisher"]
    ohe_cols = ["Platform", "Genre"]
    num_cols = ["Year", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales",
                "Total_Known_Sales", "Publisher_Avg", "Platform_Count"]
    return FullPreprocessor(te_cols, ohe_cols, num_cols), (te_cols + ohe_cols + num_cols)

# RMSE (manual)
def rmse(y, pred):
    return float(np.sqrt(np.mean((y - pred) ** 2)))

# Train models (Hyperparameter tuning)
def train_and_evaluate(X_train, X_test, y_train, y_test):
    print("Training models (Improved)...\n")

    kfold = KFold(n_splits=5, shuffle=True, random_state=42)

    #XGBoost (Improved)
    xgb = XGBRegressor(
        tree_method="hist",
        eval_metric="rmse",
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1
    )

    xgb_params = {
        "n_estimators": [200, 300, 400, 500],
        "max_depth": [4, 5, 6, 7],
        "learning_rate": [0.02, 0.03, 0.05, 0.08],
        "subsample": [0.8, 0.9, 1.0],
        "colsample_bytree": [0.8, 0.9, 1.0],
        "min_child_weight": [1, 3, 5],
        "reg_alpha": [0, 0.1, 0.5],
        "reg_lambda": [1, 1.5, 2]
    }

    print("Tuning XGBoost...")
    xgb_search = RandomizedSearchCV(
        xgb, xgb_params, n_iter=25, cv=kfold,
        scoring="neg_mean_squared_error",
        n_jobs=-1, random_state=42, verbose=1
    )
    xgb_search.fit(X_train, y_train)
    xgb_best = xgb_search.best_estimator_

    pred_xgb = xgb_best.predict(X_test)
    rmse_xgb = rmse(y_test, pred_xgb)
    r2_xgb = r2_score(y_test, pred_xgb)

    print(f"XGBoost -> RMSE: {rmse_xgb:.4f}, R2: {r2_xgb:.4f}")
    print(f"   Best Params: {xgb_search.best_params_}\n")

    #RandomForest (Improved)
    rf = RandomForestRegressor(
        n_estimators=500,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)

    pred_rf = rf.predict(X_test)
    rmse_rf = rmse(y_test, pred_rf)
    r2_rf = r2_score(y_test, pred_rf)

    print(f"RandomForest -> RMSE: {rmse_rf:.4f}, R2: {r2_rf:.4f}\n")

    #ExtraTrees (Improved)
    et = ExtraTreesRegressor(
        n_estimators=500,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1
    )
    et.fit(X_train, y_train)

    pred_et = et.predict(X_test)
    rmse_et = rmse(y_test, pred_et)
    r2_et = r2_score(y_test, pred_et)

    print(f"ExtraTrees -> RMSE: {rmse_et:.4f}, R2: {r2_et:.4f}\n")

    return {
        "xgb": (xgb_best, rmse_xgb, r2_xgb),
        "rf": (rf, rmse_rf, r2_rf),
        "et": (et, rmse_et, r2_et)
    }

# Save models
def save_models(pre, results):
    print("Saving models...")
    os.makedirs("models", exist_ok=True)

    joblib.dump(pre, "models/preprocessor.pkl")
    joblib.dump(results["xgb"][0], "models/model_xgb.pkl")
    joblib.dump(results["rf"][0], "models/model_rf.pkl")
    joblib.dump(results["et"][0], "models/model_et.pkl")

    print("All models saved to /models folder.\n")

# MAIN
def main():
    print("="*60)
    print("GAME SALES PREDICTION - IMPROVED TRAINING")
    print("="*60 + "\n")
    
    # Load data
    df = load_data()
    
    # Add simple features
    df = add_features(df)
    
    # Build preprocessor
    pre, feature_cols = build_preprocessor()
    X = df[feature_cols]
    y = df["Global_Sales"]

    print("Fitting preprocessor...")
    X_prep = pre.fit_transform(X, y)
    print(f"Preprocessor OK ({X_prep.shape[1]} features)\n")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_prep, y, test_size=0.2, random_state=42
    )
    
    print(f"Data split: Train={len(X_train):,}, Test={len(X_test):,}\n")

    # Train models
    results = train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # Save models
    save_models(pre, results)

    # Summary
    print("="*60)
    print("FINAL SUMMARY")
    print("="*60)
    for name, (model, rmse_val, r2_val) in results.items():
        print(f"{name.upper():12s} -> R2: {r2_val:.4f} | RMSE: {rmse_val:.4f}")
    
    best = max(results.keys(), key=lambda k: results[k][2])
    print(f"\nBest Model = {best.upper()} (R2={results[best][2]:.4f})")

if __name__ == "__main__":
    main()