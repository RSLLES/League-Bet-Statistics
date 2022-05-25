import numpy as np
import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap

from .utils import selector_to_title, linspace_modulo
from .odds_curves import to_odds


def confidence_to_color(C):
    """ 
    Map a confidence vector (in range [0. - 1.]) to a color vector.
    In : C -> np.array (L)
    Out : colors -> np.array(L, 3)
    """

    C = C[:, np.newaxis]
    return np.concatenate([
        np.cos(0.5*np.pi*C),
        np.sin(0.5*np.pi*C),
        # np.sin(0.5*np.pi*C),
        np.zeros_like(C)
    ], axis=1)


def get_plot(X, Y, colors):
    """
    Return a matplotlib figure displaying Y with respect to X colorized by colors.
    In :
    - X : np.array [L]
    - Y : np.array [L]
    - colors : np.array [L, 3]

    Out :
    - Matplotlib figure

    """
    cmap = LinearSegmentedColormap.from_list("", colors)
    points = np.array([X, Y]).T.reshape(-1,1,2)
    segments = np.concatenate([points[:-2],points[1:-1], points[2:]], axis=1)

    lc = LineCollection(segments, cmap=cmap, linewidth=3)
    lc.set_array(X)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.add_collection(lc)
    ax.autoscale()
    return fig

def decorate_plot(fig, selectors, nb_points, std, pic_index, X, Y, score):
    ax = fig.gca()
    ax.set_title(f"{selector_to_title(selectors)}\n[{nb_points} points, std : {std:0.1f}, score = {score:0.3f}]")
    top = Y[pic_index]
    ax.plot(X[pic_index]*np.ones((50,)), np.linspace(top, 0., 50))
    plt.plot(X, np.zeros_like(X))
    
    ax_twin = ax.twiny()
    ax_twin.set_xlim(ax.get_xlim())

    ticks_proba = np.array(ax.get_xticks()[1:-1])
    ticks_odds = list(to_odds(ticks_proba))
    ticks_odds = [round(e, 2) for e in ticks_odds]
    
    # On bot : Display Probabilities
    ax.set_xlabel("Probability")

    # On top : Odds
    ax_twin.set_xticks(ticks_proba)
    ax_twin.set_xticklabels(ticks_odds)
    ax_twin.set_xlabel("Odds $=1/P$")

    # Ordonnees : Expected gains value
    ax.set_ylabel(r"$\mathbb{E}(Gains)$ : Expected Gains value")
    return fig

if __name__ == '__main__':
    n, L = 10, 100

    T = np.linspace(0, 1, L)
    X = np.linspace(0, 1, n)
    Y = np.random.random(n)
    
    from .interpolate import interpolate
    from .utils import normalize

    F, C = interpolate(X = X, Y = Y, T = T, std = 10)
    C = normalize(C)
    C = confidence_to_color(C)
    
    fig = get_plot(T, F, C)
    plt.show()