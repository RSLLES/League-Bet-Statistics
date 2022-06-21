from multiprocessing.sharedctypes import Value
import os
import json
import numpy as np

def reduce_and_keep(L, D):
    newL, newD = [], []
    for l,d in zip(L,D):
        if isinstance(l, list):
            newL += l
            newD += [d]*len(l)
        elif isinstance(l, tuple):
            newL += [l]
            newD += [d]
        else:
            raise ValueError(f"Unknown type : {type(l)}")
    return newL, newD

def normalize(X):
    X = (X - np.mean(X)) / np.std(X)
    return (X - min(X))/(max(X) - min(X))

def get_raw_data(file_path):
    with open(file_path, 'r') as f:
        return json.loads(f.read())

def squeeze_index(text : str) -> str:
    text = text.replace('t1_', 't#_')
    text = text.replace('t2_', 't#_')
    text = text.replace('map1', 'map@')
    text = text.replace('map2', 'map@')
    text = text.replace('map3', 'map@')
    text = text.replace('map4', 'map@')
    text = text.replace('map5', 'map@')
    return text

def expand_index(text : str) -> str:
    if '#' in text:
        return text.replace('#', '1'), text.replace('#', '2')
    if '@' in text:
        return text.replace('@', '1'), text.replace('@', '2'), text.replace('@', '3'), text.replace('@', '4'), text.replace('@', '5')
    return text

def parse_selector(processed_dir : str) -> list[list[str]]:
    """
    Find by bruteforce all types of bet in every matchs.
    """
    def rec(d : dict, path = tuple(), L : set = set()) -> list[set]:
        for key in d:
            if type(d[key]) == list:
                L.add(path + (squeeze_index(key),))
            if type(d[key]) == dict:
                rec(d[key], path + (squeeze_index(key),), L)
        return L

    all = set()
    for f in os.listdir(processed_dir):
        data = get_raw_data(os.path.join(processed_dir, f))
        all = set.union(all, rec(data))
    
    # Reformating
    def as_list(t):
        if type(t) == tuple:
            return list(t)
        if type(t) == str:
            return [t]
        raise ValueError()

    formated = []
    for path in all:
        p = []
        for s in path:
            p.append(as_list(expand_index(s)))
        formated.append(p)
    return formated

def selector_to_title(selectors):
    title = ""
    for a in selectors:
        a = [squeeze_index(e) for e in a][0]
        title = f"{title}/{a}"
    return title

def linspace_modulo(a, b, e):
    A = int(a/e) + 1
    B = int(b/e)
    N = B - A
    return [a] + list(np.linspace(A*e, B*e, N+1)) + [b]


if __name__ == '__main__':
    a = parse_selector(
        processed_dir="C:/Users/Romain/Documents/Projets Info/LolBetStats/data/processed"
    )
    print(len(a))