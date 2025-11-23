import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import category_encoders as ce

class FullPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, te_cols=None, ohe_cols=None, num_cols=None):
        self.te_cols = te_cols or []
        self.ohe_cols = ohe_cols or []
        self.num_cols = num_cols or []

        self.te = None
        self.ohe = None
        self.scaler = StandardScaler()

    def fit(self, X, y=None):
        X = pd.DataFrame(X)

        self.te = ce.TargetEncoder(cols=self.te_cols)
        self.te.fit(X[self.te_cols], y)

        self.ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.ohe.fit(X[self.ohe_cols])

        self.scaler.fit(X[self.num_cols])

        return self

    def transform(self, X):
        X = pd.DataFrame(X)
        parts = []

        parts.append(self.te.transform(X[self.te_cols]).to_numpy())
        parts.append(self.ohe.transform(X[self.ohe_cols]))
        parts.append(self.scaler.transform(X[self.num_cols]))

        return np.hstack(parts)

    def get_feature_names(self):
        return (
            list(self.te_cols) +
            list(self.ohe.get_feature_names_out(self.ohe_cols)) +
            list(self.num_cols)
        )
