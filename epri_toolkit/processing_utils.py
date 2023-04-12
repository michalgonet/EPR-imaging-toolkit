import numpy as np
from scipy.interpolate import interp2d
from epri_toolkit.classes import RecoPars, AcqPars, RawData


def create_sino2d(raw_data: np.ndarray, acq_pars: AcqPars) -> np.ndarray:
    return np.reshape(raw_data, [acq_pars.points, -1], order='F')


def sinogram_interpolation(sinogram: np.ndarray, reco_pars: RecoPars) -> np.ndarray:
    x, y = np.arange(0, sinogram.shape[0]), np.arange(0, sinogram.shape[1])
    new_y = np.linspace(0, sinogram.shape[1], sinogram.shape[1])
    new_x = np.linspace(0, sinogram.shape[0], reco_pars.img_size)
    interp_func = interp2d(y, x, sinogram, kind='linear')
    return interp_func(new_y, new_x)


def spectrum_interpolation(spectrum: np.ndarray, output_size: int) -> np.ndarray:
    x = np.arange(spectrum.shape[0])
    x_new = np.linspace(0, spectrum.shape[0], output_size, endpoint=False)
    return np.interp(x_new, x, spectrum)


def sinogram_integration(sinogram: np.ndarray) -> np.ndarray:
    return np.cumsum(sinogram, axis=0)


def deconvolution(grad_spectrum, non_grad_spectrum, filt):
    non_grad_spectrum = non_grad_spectrum.T
    points = grad_spectrum.shape[0]
    axis = np.linspace(0, 1024, points)
    sigma = filt / np.sqrt(2 * np.log(2))
    h = np.sqrt(2 / np.pi) * (1 / sigma) * np.exp(-2 * (axis / sigma) ** 2)
    h /= np.max(h)
    freq_resp = np.fft.fft(non_grad_spectrum)
    epsilon = 1e-10  # Small constant value to avoid zero division
    deco_temp = np.fft.ifft(np.fft.fft(grad_spectrum.T) * h / (freq_resp + epsilon)).real
    return np.fft.ifftshift(deco_temp)


def sinogram_remove_baseline(sinogram):
    out_data = sinogram
    bl = np.mean(out_data, axis=0)
    out_y = out_data - np.tile(bl, (out_data.shape[0], 1))
    sino_deco = out_y
    return sino_deco


def sinogram_preprocessing(raw_data: RawData, acq_pars: AcqPars, reco_pars: RecoPars) -> np.ndarray:
    sinogram = create_sino2d(raw_data.raw_sinogram, acq_pars)
    if reco_pars.deconvolution:
        sino = np.apply_along_axis(lambda x: deconvolution(x, raw_data.raw_ref, reco_pars.deco_filter),
                                   axis=0, arr=sinogram)
    else:
        sino = sinogram_integration(sinogram)

    if reco_pars.baseline:
        sino = sinogram_remove_baseline(sino)

    return sinogram_interpolation(sino, reco_pars)
