import numpy as np


def load_dta_file(path):
    with open(path, 'rb') as f:
        return np.frombuffer(f.read(), dtype='>d')


def load_dsc_file(path):
    pars_raw = {}
    with open(path) as f:
        all_lines = f.readlines()

    for line in all_lines:
        if line.startswith(('*', '.DVC', '#')):
            continue
        words = line.strip().split()
        if len(words) > 1:
            pars_raw[words[0]] = words[1:]
    return pars_raw
