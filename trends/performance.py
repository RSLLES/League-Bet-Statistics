import numpy as np

def metric(length, mean, pic, nb_points, nb_threshold = 25):
    return pic*length*mean*(1.0 - np.exp(-nb_points/nb_threshold))

def performance(X, Y, C, nb_points):
    scores = []
    for s, e in get_all_positive_zones(Y):
        length = X[e] - X[s]
        meanC = np.mean(C[s:e])
        pic, pic_index = np.max(Y[s:e]), np.argmax(Y[s:e]) + s
        score = metric(length, meanC, pic, nb_points)
        print(f"Positive zone in [{s}, {e}[ : length = {length}, pic = {pic} in {pic_index}, avg_conf = {meanC}, score {score}")
        scores.append((score, pic_index))
    return max(scores, key = lambda x : x[0]) if len(scores) > 0 else (None, None)


def get_all_positive_zones(Y):
    in_zone = False
    begin = 0
    for i in range(len(Y)):
        if not in_zone and Y[i] > 0. :
            in_zone = True
            begin = i
        elif in_zone and (Y[i] < 0.0 or i == len(Y) - 1):
            in_zone = False
            yield (begin, i)


if __name__ == '__main__':
    X = np.linspace(0, 3*np.pi, 3*314)
    Y = np.cos(X)*(1/(1+X))
    C = np.square(np.sin(X))

    performance(X, Y, C)

    import matplotlib.pyplot as plt
    plt.plot(X, Y, label = "curve")
    plt.plot(X, C, label = "confidence")
    plt.plot(X, np.zeros_like(X))
    plt.legend()
    plt.show()