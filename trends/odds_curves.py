import os
import json
import numpy as np
from functools import reduce

from .interpolate import interpolate
from .utils import normalize, get_raw_data

###############
### Methods ###
###############

def gains_wrt_proba_curve(selectors : list[list[str]], processd_dir : str, std : float):
    """Return Odds (X), Gains (Y)"""
    S = get_results_over_all(selectors= selectors,processd_dir=processd_dir)
    Odds, Wins = format_in_vectors(S)
    length = len(Odds)
    
    # Changement de base
    Gains = win_to_gain(Odds, Wins)
    Proba = to_probabilities(Odds)

    # Interpolation dans la base des probas
    Long_Proba = np.linspace(min(Proba),max(Proba), 200)
    std = std/(Long_Proba[-1] - Long_Proba[0])
    Long_Gains, C = interpolate(Proba, Gains, Long_Proba, std=std)
    C = normalize(C)

    # Changement de base
    # Long_Odds = to_odds(Long_Odds)

    return Long_Proba, Long_Gains, C, length, std


#############
### Utils ###
#############

def extract_results(bet):
    assert type(bet) == list
    assert len(bet) == 2
    return tuple(map(float, bet))


def get_results_from_selectors(data, selectors):
    if len(selectors) == 0:
        return [extract_results(data)]

    s = selectors[0]
    
    if len(s) == 0:
        return []

    A = get_results_from_selectors(data[s[0]], selectors[1:]) if s[0] in data else []
    B = get_results_from_selectors(data, [s[1:]] + selectors[1:])
    return A + B


def get_results_over_all(selectors, processd_dir):
    S = map(
        lambda file : get_results_from_selectors(
            data= get_raw_data(os.path.join(processd_dir, file)),
            selectors= selectors
        ), os.listdir(processd_dir)
    )
    return reduce(lambda x,y : x+y, S)

        
def format_in_vectors(S):
    X = [x for x,y in filter(lambda x : not np.isnan(x[0]), S)]
    Y = [y for x,y in filter(lambda x : not np.isnan(x[0]), S)]

    return np.array(X), np.array(Y)

def win_to_gain(Odds, Win):
    return Odds*Win - 1

def odds_to_proper_base(Odds, e = 0.95):
    return np.log(Odds/e - 1)

def proper_base_to_odds(X, e = 0.95):
    return e*(np.exp(X) + 1)

def to_probabilities(X):
    return np.divide(1.0, X)

def to_odds(O):
    return np.divide(1.0, O)


############
### Test ###
############

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    std = 20
    X, Y, C, _, _ = gains_wrt_proba_curve(
        selectors= [
            ['map1', 'map2', 'map3', 'map4', 'map5'], ['totalbaronsslain'], ['over1.5']
        ],
        processd_dir="C:/Users/Romain/Documents/Projets Info/LolBetStats/data/processed",
        std=std
    )
    
    from .plot import get_plot, confidence_to_color
    
    fig = get_plot(X, Y, confidence_to_color(C))

    # Plot
    # plt.xlabel("Odds")
    # plt.ylabel("Gains")
    # plt.plot(X, np.zeros_like(Y))
    # plt.title(f"${len(X)}$ points, $\\sigma = {std}/{1} = {std}$")
    # plt.legend()
    plt.show()