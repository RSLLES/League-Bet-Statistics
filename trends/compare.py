import os
import matplotlib.pyplot as plt

from .utils import parse_selector
from .odds_curves import gains_wrt_proba_curve
from .performance import performance
from .plot import decorate_plot, get_plot, confidence_to_color

if __name__ == '__main__':
    nb_selectors = 7
    std0 = 20
    processed_dir = "data/processed"
    save_dir = "trends/best_selectors"

    all_selectors = parse_selector(
        processed_dir=processed_dir
    )

    good_selectors = []
    for selectors in all_selectors:
        X, Y, C, nb_points, _ = gains_wrt_proba_curve(
            selectors= selectors,
            processd_dir= processed_dir,
            std= std0
        )
        score, _ = performance(
            X=X,
            Y=Y,
            C=C,
            nb_points=nb_points
        )

        if score != None:
            good_selectors.append((selectors, score))

    good_selectors.sort(key=lambda x : -x[1])
    good_selectors = good_selectors[:nb_selectors]
    for i in range(len(good_selectors)):
        selectors, _ = good_selectors[i]
        X, Y, C, nb_points, std = gains_wrt_proba_curve(
            selectors= selectors,
            processd_dir=processed_dir,
            std=std0
        )
        score, pic_index = performance(X, Y, C, nb_points)
        fig = get_plot(X, Y, confidence_to_color(C))
        fig = decorate_plot(fig,
            selectors=selectors,
            nb_points=nb_points,
            std= std,
            pic_index= pic_index,
            X=X, Y=Y, score=score
        )

        fig.savefig(os.path.join(save_dir, f"{i+1}.png"), bbox_inches='tight', dpi = 200)
        plt.close()

