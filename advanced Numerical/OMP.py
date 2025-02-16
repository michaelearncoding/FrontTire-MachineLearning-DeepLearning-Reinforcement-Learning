import numpy as np
from sklearn.linear_model import OrthogonalMatchingPursuit
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class OMPRegressor:
    def __init__(self, n_nonzero_coefs=None, tol=None):
        """
        Initialize OMP regressor
        Args:
            n_nonzero_coefs: target number of non-zero coefficients
            tol: tolerance for error
        """
        self.scaler = StandardScaler()
        self.omp = OrthogonalMatchingPursuit(
            n_nonzero_coefs=n_nonzero_coefs,
            tol=tol
        )
        
    def fit(self, X, y):
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        # Fit OMP model
        self.omp.fit(X_scaled, y)
        return self
        
    def predict(self, X):
        # Scale new data using same parameters
        X_scaled = self.scaler.transform(X)
        return self.omp.predict(X_scaled)
    
    def get_support(self):
        """Return indices of selected features"""
        return self.omp.n_nonzero_coefs_

if __name__ == "__main__":
    # Generate synthetic sparse data
    n_samples, n_features = 100, 500
    n_informative = 5
    
    # Create random sparse coefficients
    true_coef = np.zeros(n_features)
    indices = np.random.choice(n_features, n_informative, replace=False)
    true_coef[indices] = np.random.randn(n_informative)
    
    # Generate data
    X = np.random.randn(n_samples, n_features)
    y = np.dot(X, true_coef) + np.random.normal(0, 0.1, n_samples)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    omp = OMPRegressor(n_nonzero_coefs=n_informative)
    omp.fit(X_train, y_train)
    
    # Make predictions
    y_pred = omp.predict(X_test)
    
    # Evaluate
    print(f"R² Score: {r2_score(y_test, y_pred):.3f}")
    print(f"MSE: {mean_squared_error(y_test, y_pred):.3f}")
    print(f"Number of non-zero coefficients: {omp.get_support()}")