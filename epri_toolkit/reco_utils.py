import numpy as np

from epri_toolkit.classes import Config, AcqPars, RecoPars
from skimage.transform import iradon


def get_reco_pars(config: Config, acq_pars: AcqPars) -> RecoPars:
    alphas = list(np.linspace(acq_pars.first_alpha, 180 - acq_pars.first_alpha, acq_pars.alpha_no))
    betas = list(np.linspace(acq_pars.first_alpha, 180 - acq_pars.first_alpha, acq_pars.beta_no))
    gammas = list(np.linspace(-acq_pars.max_gamma, acq_pars.max_gamma, acq_pars.gamma_no))

    return RecoPars(img_size=int(config.img_size),
                    filter=config.filter,
                    cutoff=config.cutoff,
                    alpha_no=acq_pars.alpha_no,
                    beta_no=acq_pars.beta_no,
                    gamma_no=acq_pars.gamma_no,
                    alphas=alphas,
                    betas=betas,
                    gammas=gammas)


def fbp3d(sinogram: np.ndarray, reco_pars: RecoPars):
    sino3d = np.reshape(sinogram, [sinogram.shape[0], reco_pars.beta_no, reco_pars.alpha_no], order='C')
    img_stage_1 = np.zeros([reco_pars.img_size, reco_pars.img_size, reco_pars.alpha_no])
    img_stage_2 = np.zeros([reco_pars.img_size, reco_pars.img_size, reco_pars.img_size])

    for alpha in range(reco_pars.alpha_no):
        img_stage_1[:, :, alpha] = iradon(radon_image=sino3d[:, :, alpha],
                                          theta=reco_pars.alphas,
                                          output_size=reco_pars.img_size,
                                          filter_name=reco_pars.filter,
                                          interpolation='linear',
                                          circle=False)
    for beta in range(reco_pars.img_size):
        img_stage_2[:, beta, :] = iradon(radon_image=img_stage_1[:, beta, :],
                                         theta=reco_pars.betas,
                                         output_size=reco_pars.img_size,
                                         filter_name=reco_pars.filter,
                                         interpolation='linear',
                                         circle=False)

    return img_stage_2
