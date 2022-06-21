import numpy as np

def batch_weighted_sum(
        X : np.array,
        W : np.array
    ) -> np.array :
    """
    Input :
        X : 1D Array (d,)
        W : 2D Array (B,d)
    Output :
        Y : 1D Array (B,), where for i in [[1, B]], Y_i = (X|W_i)/||W_i||
    """
    assert len(X.shape) == 1
    assert len(W.shape) == 2
    assert X.shape[0] == W.shape[1]

    return np.einsum("d,bd->b", X, W)/np.sum(W, axis=1)

def batch_exp_weights(
        X : np.array,
        x : np.array,
        std : float
    ) -> np.array :
    """
    Input :
        X : 1D Array (d,)
    x : 1D Array (B,)
        std : float
    Output :
        Y : 2D Array (B,d), where for i,j in [[1, B]]x[[1, d]], Y_(i,j) = exp(-((X_(i,j) - x_i)/std)^2)
    """
    assert len(X.shape) == 1
    assert len(x.shape) == 1
    assert isinstance(std, float) and std > 0.
    B, = x.shape    
    d, = X.shape

    X = np.repeat(np.expand_dims(X, axis=0), B, axis=0)
    x = np.repeat(np.expand_dims(x, axis=1), d, axis=1)
    X = (X - x)/std
    X = np.square(X)
    return np.exp(-X)


def interpolate(
        X : np.array, 
        Y : np.array, 
        T : np.array, 
        std : float,
        W : np.array = None
    ) -> np.array:
    """ 
    Return the interpolate curve from X and Y cloud points using :
    forall x in T, f(x) = sum_{i in len(X)}(Y_i * exp(-s*(X_i - x)^2)) / sum_{i in len(X)}(exp(-s*(X_i - x)^2))
    It also returns a confidence curve describing how much trust one can have on a specific point.
    Mathematically, this function is :
    forall x in T, c(x) = sum_{i in len(X)}(exp(-s*(X_i - x)^2))/n
    A score of 1 means that all points are specifically used a this location to compute this value.

    input :
        - X (1D Numpy array [n]): abscisse values
        - Y (1D Numpy array [n]): ordonnates values (must have the same size as X)
        - T (1D Numpy array [L]): points where to process the interpolate curve
        - std (float) : standard deviation s to use in the formula above
        - W (1D Numpy array [n], optionnal ) : Weight for all points in X

    output :
        - f(T) (1D Numpy array [L]) : Resulted points at T of the previous explained interpolated function
        - C(T) (1D Numpy array [L]) : Degree of confidence of 
    """
    assert len(X.shape) == 1
    if W is None:
        W = np.ones_like(X)
    assert len(W.shape) == 1
    assert len(Y.shape) == 1
    assert len(T.shape) == 1
    assert X.shape == Y.shape
    assert X.shape == W.shape
    n, = X.shape
    L, = T.shape

    W = np.repeat(np.expand_dims(W, axis=0), L, axis=0)
    W = batch_exp_weights(X= X, x=T, std=std)*W
    F = batch_weighted_sum(X=Y, W=W)
    C = np.sum(W, axis=1)
    return F, C

############
### Test ###
############

if __name__ == '__main__':
    n, L = 10, 1000

    X = np.linspace(0, 1, n)
    Y = np.sin(np.pi*X)
    
    T = np.linspace(0, 1, L)
    F, C = interpolate(X = X, Y = Y, T = T, std = 0.05)
    print(F)
    import matplotlib.pyplot as plt
    plt.plot(X, Y, label="originale")
    plt.plot(T, F, label="Interpolated")
    plt.legend()
    plt.show()
    
