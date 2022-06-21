import os
import numpy as np
from datetime import datetime

from .config import config

from .interpolate import interpolate
from .utils import normalize, get_raw_data, reduce_and_keep


###############
### Methods ###
###############

def gains_wrt_proba_curve(selectors : list[list[str]], processd_dir : str, std : float, age_threshold : float):
    """Return Odds (X), Gains (Y)"""
    S, D = get_results_over_all(selectors= selectors,processd_dir=processd_dir)
    Odds, Wins, Ages = format_in_vectors(S, D)
    
    # Changement de base
    Gains = win_to_gain(Odds, Wins)
    Proba = to_probabilities(Odds)

    # Interpolation dans la base des probas
    Long_Proba = np.linspace(min(Proba),max(Proba) + 0.01, 200)
    std = std*(Long_Proba[-1] - Long_Proba[0])
    Weights = np.exp(-Ages/age_threshold)
    Long_Gains, C = interpolate(Proba, Gains, Long_Proba, std=std, W=Weights)
    C = normalize(C)

    # Changement de base
    # Long_Odds = to_odds(Long_Odds)
    stats = {}
    stats["Length"] = len(Odds)
    stats["STD"] = std
    stats["age_weight"] = np.max(Weights)

    return Long_Proba, Long_Gains, C, stats


#############
### Utils ###
#############

def get_date(match):
    date = match['date']
    return datetime(
        year= int(date["year"]), 
        month= int(date["month"]), 
        day= int(date["day"]),
        hour= int(date["time"].split(":")[0]),
        minute= int(date["time"].split(":")[1])
    )


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
    Dates = [
        get_date(get_raw_data(os.path.join(processd_dir, file_path))) 
        for file_path in os.listdir(processd_dir)
    ]

    S = [ 
        get_results_from_selectors(
            data= get_raw_data(os.path.join(processd_dir, file)),
            selectors= selectors
        ) for file in os.listdir(processd_dir)
    ]

    S = list(filter(lambda x : len(x[1]) != 0, zip(Dates, S)))
    S = list(zip(*S))

    return reduce_and_keep(L=S[1], D=S[0])

        
def format_in_vectors(S, D):
    X = [x for x, _ in filter(lambda x : not np.isnan(x[0]), S)]
    Y = [y for _, y in filter(lambda x : not np.isnan(x[0]), S)]
    D = [
        (datetime.now() - d).total_seconds() 
        for _, d in filter(lambda X : not np.isnan(X[0][0]), zip(S, D))
    ]

    return np.array(X), np.array(Y), np.array(D)

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
    X, Y, C, _, _ = gains_wrt_proba_curve(
        selectors= [
            ['map1', 'map2', 'map3', 'map4', 'map5'], ['totalbaronsslain'], ['over1.5']
        ],
        processd_dir="C:/Users/Romain/Documents/Projets Info/LolBetStats/data/processed",
        std= config["STD"],
        age_threshold= config["AGE_THRESHOLD"]
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