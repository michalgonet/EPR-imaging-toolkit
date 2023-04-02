import numpy as np
from scipy.interpolate import interp2d

from epri_toolkit.classes import RecoPars


def sinogram_interpolation(sinogram: np.ndarray, reco_pars: RecoPars) -> np.ndarray:
    y = np.arange(0, sinogram.shape[1])
    x = np.arange(0, sinogram.shape[0])
    new_y = np.linspace(0, sinogram.shape[1], sinogram.shape[1])
    new_x = np.linspace(0, sinogram.shape[0], reco_pars.img_size)
    interp_func = interp2d(y, x, sinogram, kind='linear')
    return interp_func(new_y, new_x)


def sinogram_integration(sinogram: np.ndarray) -> np.ndarray:
    return np.cumsum(sinogram, axis=0)
