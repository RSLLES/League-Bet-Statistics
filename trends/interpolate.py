
import numpy as np

def interpolate(
        X : np.array, 
        Y : np.array, 
        T : np.array, 
        std : float
    ) -> np.array:
    """ 
    Return the interpolate curve from X and Y cloud points using :
    forall x in T, f(x) = sum_{i in len(X)}(Y_i * exp(-s*(X_i - x)^2)) / sum_{i in len(X)}(exp(-s*(X_i - x)^2))
    It also returns a confidence curve describing how much trust one can have on a specific point.
    Mathematically, this function is :
    forall x in T, c(x) = sum_{i in len(X)}(exp(-s*(X_i - x)^2))/n
    A score of 1 means that all points are specifically used a this location to compute this value.

    input :
        - X (1 Numpy array [n]): abscisse values
        - Y (1D Numpy array [n]): ordonnates values (must have the same size as X)
        - T (1D Numpy array [L]): points where to process the interpolate curve
        - std (float) : standard deviation s to use in the formula above

    output :
        - f(T) (1D Numpy array [L]) : Resulted points at T of the previous explained interpolated function
        - C(T) (1D Numpy array [L]) : Degree of confidence of 
    """
    assert len(X.shape) == 1
    assert len(Y.shape) == 1
    assert len(T.shape) == 1
    assert X.shape == Y.shape
    n = X.shape[0]
    L = T.shape[0]

    X = X.reshape(n,1) @ np.ones((1,L))
    T = np.ones((n,1)) @ T.reshape(1,L)
    
    Y = np.diag(Y)

    coeffs = np.exp(-std*np.square(X-T))
    S = (Y @ coeffs).sum(axis=0)
    C = coeffs.sum(axis=0)
    return S/C, C/n

############
### Test ###
############

if __name__ == '__main__':
    n, L = 10, 100

    T = np.linspace(0, 1, L)
    X = np.linspace(0, 1, n)
    Y = np.random.random(n)
    
    F, C = interpolate(X = X, Y = Y, T = T, std = 10)
    print(F)
