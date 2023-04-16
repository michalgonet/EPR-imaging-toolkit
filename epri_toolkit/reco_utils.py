import numpy as np
from epri_toolkit.classes import Config, AcqPars, RecoPars
from skimage.transform import iradon, iradon_sart


def get_reco_pars(config: Config, acq_pars: AcqPars) -> RecoPars:
    alphas = list(np.linspace(acq_pars.first_alpha, 180 - acq_pars.first_alpha, acq_pars.alpha_no))
    betas = list(np.linspace(acq_pars.first_alpha, 180 - acq_pars.first_alpha, acq_pars.beta_no))
    gammas = list(np.linspace(-acq_pars.max_gamma, acq_pars.max_gamma, acq_pars.gamma_no))

    return RecoPars(
        method=config.reco_method,
        img_size=int(config.img_size),
        filter_spat=config.filter_spat,
        filter_spec=config.filter_spec,
        deconvolution=bool(config.deconvolution),
        deco_filter=float(config.deco_filter),
        baseline=bool(config.baseline),
        cutoff_spat=float(config.cutoff_spat),
        cutoff_spec=float(config.cutoff_spec),
        sart_relax=float(config.sart_relax),
        sart_iters=list(config.sart_iters),
        alpha_no=acq_pars.alpha_no,
        beta_no=acq_pars.beta_no,
        gamma_no=acq_pars.gamma_no,
        alphas=alphas,
        betas=betas,
        gammas=gammas
    )


def ms_fbp3d(sinogram: np.ndarray, reco_pars: RecoPars):
    sino3d = sinogram.reshape((sinogram.shape[0], reco_pars.beta_no, reco_pars.alpha_no), order='C')
    img_stage_1 = np.zeros((reco_pars.img_size, reco_pars.img_size, reco_pars.alpha_no))
    img_stage_2 = np.zeros((reco_pars.img_size, reco_pars.img_size, reco_pars.img_size))

    for alpha in range(reco_pars.alpha_no):
        img_stage_1[:, :, alpha] = iradon(
            radon_image=sino3d[:, :, alpha],
            theta=reco_pars.alphas,
            output_size=reco_pars.img_size,
            filter_name=reco_pars.filter_spat,
            interpolation='linear',
            circle=False
        )

    for beta in range(reco_pars.img_size):
        img_stage_2[:, beta, :] = iradon(
            radon_image=img_stage_1[:, beta, :],
            theta=reco_pars.betas,
            output_size=reco_pars.img_size,
            filter_name=reco_pars.filter_spat,
            interpolation='linear',
            circle=False
        )

    return img_stage_2


def sart3d(sinogram: np.ndarray, reco_pars: RecoPars):
    sino3d = sinogram.reshape((sinogram.shape[0], reco_pars.beta_no, reco_pars.alpha_no), order='C')
    img_stage_1 = np.zeros((reco_pars.img_size, reco_pars.img_size, reco_pars.alpha_no))
    img_stage_2 = np.zeros((reco_pars.img_size, reco_pars.img_size, reco_pars.img_size))

    for alpha in range(reco_pars.alpha_no):
        img_stage_1[:, :, alpha] = iradon(
            radon_image=sino3d[:, :, alpha],
            theta=reco_pars.alphas,
            output_size=reco_pars.img_size,
            filter_name=reco_pars.filter_spat,
            interpolation='linear',
            circle=False
        )

    for i in range(reco_pars.sart_iters[0]):
        for alpha in range(reco_pars.alpha_no):
            img_stage_1[:, :, alpha] = iradon_sart(
                radon_image=sino3d[:, :, alpha],
                theta=reco_pars.alphas,
                image=img_stage_1[:, :, alpha],
                projection_shifts=None,
                clip=None,
                relaxation=reco_pars.sart_relax
            )

    for beta in range(reco_pars.img_size):
        img_stage_2[:, beta, :] = iradon(
            radon_image=img_stage_1[:, beta, :],
            theta=reco_pars.betas,
            output_size=reco_pars.img_size,
            filter_name=reco_pars.filter_spat,
            interpolation='linear',
            circle=False
        )

    for i in range(reco_pars.sart_iters[1]):
        for beta in range(reco_pars.img_size):
            img_stage_2[:, beta, :] = iradon_sart(
                radon_image=img_stage_1[:, beta, :],
                theta=reco_pars.betas,
                image=img_stage_2[:, beta, :],
                projection_shifts=None,
                clip=None,
                relaxation=reco_pars.sart_relax
            )

    return img_stage_2


def ms_fbp4d(sinogram, reco_pars):
    sino4d = sinogram.reshape((sinogram.shape[0], reco_pars.beta_no, reco_pars.alpha_no, reco_pars.gamma_no), order='F')
    img_stage_1 = np.zeros((reco_pars.img_size, reco_pars.beta_no, reco_pars.alpha_no, reco_pars.img_size,))
    img_stage_2 = np.zeros((reco_pars.img_size, reco_pars.beta_no, reco_pars.img_size, reco_pars.img_size))
    img_stage_3 = np.zeros((reco_pars.img_size, reco_pars.img_size, reco_pars.img_size, reco_pars.img_size))

    for alpha in range(reco_pars.alpha_no):
        for beta in range(reco_pars.beta_no):
            img_stage_1[:, beta, alpha, :] = iradon(
                radon_image=sino4d[:, beta, alpha, :],
                theta=reco_pars.gammas,
                output_size=reco_pars.img_size,
                filter_name=reco_pars.filter_spat,
                interpolation='linear',
                circle=False
            )

    for alpha in range(reco_pars.alpha_no):
        for j in range(reco_pars.img_size):
            img_stage_2[:, alpha, :, j] = iradon(
                radon_image=img_stage_1[:, alpha, :, j],
                theta=reco_pars.betas,
                output_size=reco_pars.img_size,
                filter_name=reco_pars.filter_spat,
                interpolation='linear',
                circle=False
            )
    for i in range(reco_pars.img_size):
        for j in range(reco_pars.img_size):
            img_stage_3[:, :, i, j] = iradon(
                radon_image=img_stage_2[:, :, i, j],
                theta=reco_pars.alphas,
                output_size=reco_pars.img_size,
                filter_name=reco_pars.filter_spat,
                interpolation='linear',
                circle=False
            )

    return img_stage_3


def reconstruct(sinogram: np.ndarray, acq_pars: AcqPars, reco_pars: RecoPars) -> np.ndarray:
    if acq_pars.img_type == '3D':
        if reco_pars.method == 'ms_fbp':
            return ms_fbp3d(sinogram, reco_pars)
        elif reco_pars.method == 'sart':
            return sart3d(sinogram, reco_pars)

    elif acq_pars.img_type == '3D + Spectral':
        if reco_pars.method == 'ms_fbp':
            return ms_fbp4d(sinogram, reco_pars)
