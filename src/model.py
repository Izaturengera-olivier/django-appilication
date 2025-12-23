from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np
import warnings
import os
import threading

# Simple in-process cached model loader to avoid repeated joblib loads
_CACHED_MODEL = None
_CACHED_MODEL_MTIME = None
_CACHED_LOCK = threading.Lock()


def train_model(X, y, test_size=0.2, random_state=0, n_estimators=300):
    # Decide whether to stratify based on class counts
    stratify = y
    try:
        vc = y.value_counts()
        if vc.min() < 2:
            warnings.warn('Some classes have fewer than 2 samples; skipping stratified split.')
            stratify = None
    except Exception:
        # If y is not a Series or lacks value_counts, skip stratify
        stratify = None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=stratify)
    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', RandomForestClassifier(n_estimators=n_estimators, random_state=random_state, class_weight='balanced'))
    ])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds)

    # compute feature importances from underlying RF if available
    importances = None
    try:
        clf = pipe.named_steps['clf']
        feat_names = X.columns if hasattr(X, 'columns') else [f'f{i}' for i in range(X.shape[1])]
        importances = sorted(zip(feat_names, clf.feature_importances_), key=lambda x: x[1], reverse=True)
    except Exception:
        importances = None

    return pipe, acc, report, importances


def save_model(model, path):
    """Save a trained model to the specified path.
    
    Args:
        model: The trained model to save
        path: File path where to save the model. Parent directories will be created if they don't exist.
    """
    # Convert to absolute path and normalize it
    abs_path = os.path.abspath(path)
    # Ensure the directory exists
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    # On Windows, ensure we're using the correct path format
    if os.name == 'nt':
        abs_path = os.path.normpath(abs_path)
    # Save the model
    joblib.dump(model, abs_path)


def load_model(path):
    return joblib.load(path)


def load_model_cached(path, force_reload=False):
    """Load and cache the model in-process. If the file's mtime changes
    or `force_reload` is True, the model will be reloaded.
    This avoids expensive repeated disk loads per web request.
    """
    global _CACHED_MODEL, _CACHED_MODEL_MTIME
    try:
        mtime = os.path.getmtime(path)
    except Exception:
        mtime = None

    with _CACHED_LOCK:
        if not force_reload and _CACHED_MODEL is not None and _CACHED_MODEL_MTIME == mtime:
            return _CACHED_MODEL

        try:
            model = joblib.load(path, mmap_mode='r')
        except TypeError:
            # Older joblib versions may not accept mmap_mode; fall back to default
            model = joblib.load(path)
        _CACHED_MODEL = model
        _CACHED_MODEL_MTIME = mtime
        return model
