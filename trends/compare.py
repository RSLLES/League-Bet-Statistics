import os
import matplotlib.pyplot as plt

from .config import config

from .utils import parse_selector
from .odds_curves import gains_wrt_proba_curve
from .performance import performance
from .plot import decorate_plot, get_plot, confidence_to_color

if __name__ == '__main__':
    all_selectors = parse_selector(
        processed_dir= config["PROCESSED_DIR"]
    )

    good_selectors = []
    for selectors in all_selectors:
        X, Y, C, stats = gains_wrt_proba_curve(
            selectors= selectors,
            processd_dir= config["PROCESSED_DIR"],
            std= config["STD"],
            age_threshold= config["AGE_THRESHOLD"]
        )
        score, _ = performance(
            X=X,
            Y=Y,
            C=C,
            nb_points=stats["Length"],
            age_weight= stats["age_weight"]
        )

        if score != None:
            good_selectors.append((selectors, score))

    good_selectors.sort(key=lambda x : -x[1])
    good_selectors = good_selectors[:config["NB_GRAPH"]]
    for i in range(len(good_selectors)):
        selectors, _ = good_selectors[i]
        X, Y, C, stats = gains_wrt_proba_curve(
            selectors= selectors,
            processd_dir= config["PROCESSED_DIR"],
            std=config["STD"],
            age_threshold= config["AGE_THRESHOLD"]
        )
        score, pic_index = performance(X, Y, C, stats["Length"], stats["age_weight"])
        fig = get_plot(X, Y, confidence_to_color(C))
        fig = decorate_plot(fig,
            selectors=selectors,
            nb_points=stats["Length"],
            std= stats["STD"],
            pic_index= pic_index,
            X=X, Y=Y, score=score
        )

        fig.savefig(os.path.join(config["SAVE_DIR"], f"{i+1}.png"), bbox_inches='tight', dpi = 100)
        plt.close()

