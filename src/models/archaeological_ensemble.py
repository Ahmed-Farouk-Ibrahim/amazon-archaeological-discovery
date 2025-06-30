"""
Archaeological ensemble model using XGBoost with CPU/GPU support.
"""

import xgboost as xgb
import logging

logger = logging.getLogger(__name__)

class UltimateArchaeologicalEnsemble:
    def __init__(self, use_gpu=True):
        """
        Initialize the archaeological ensemble model.
        
        Args:
            use_gpu: Whether to use GPU acceleration (if available)
        """
        # Detect GPU availability
        gpu_available = False
        if use_gpu:
            try:
                import cupy as cp
                gpu_available = True
                logger.info("GPU detected, using GPU acceleration")
            except ImportError:
                logger.info("CuPy not available, using CPU")
        
        # Configure XGBoost parameters based on hardware
        if gpu_available and use_gpu:
            self.model = xgb.XGBClassifier(
                objective='binary:logistic',
                eval_metric='logloss',
                tree_method='gpu_hist',
                device='cuda:0',
                n_estimators=100,
                learning_rate=0.01,
                max_depth=3,
                min_child_weight=5,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=1.0,
                random_state=42
            )
        else:
            self.model = xgb.XGBClassifier(
                objective='binary:logistic',
                eval_metric='logloss',
                tree_method='hist',  # CPU version
                n_estimators=100,
                learning_rate=0.01,
                max_depth=3,
                min_child_weight=5,
                subsample=0.8,
                colsample_bytree=0.8,
                reg_alpha=0.1,
                reg_lambda=1.0,
                random_state=42
            )
        
        self.is_fitted = False

    def fit(self, X, y):
        """Train the model"""
        logger.info("Training archaeological ensemble model...")
        self.model.fit(X, y)
        self.is_fitted = True
        logger.info("Model training completed")

    def predict_proba(self, X):
        """Predict probabilities"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        return self.model.predict_proba(X)[:, 1]

    def save(self, path):
        """Save model to file"""
        import joblib
        joblib.dump(self.model, path)
        logger.info(f"Model saved to {path}")

    def load(self, path):
        """Load model from file"""
        import joblib
        self.model = joblib.load(path)
        self.is_fitted = True
        logger.info(f"Model loaded from {path}")
