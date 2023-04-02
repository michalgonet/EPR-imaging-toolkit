from dataclasses import dataclass, field
from typing import List
import json

import numpy as np


@dataclass(frozen=True)
class AcqPars:
    data: str
    time: str
    scan_time: str
    img_time: str
    img_type: str
    orient: str
    points: int
    alpha_no: int
    beta_no: int
    gamma_no: int
    first_alpha: float
    max_gamma: float
    gradient: float
    sweep: float
    center_field: float
    mod_amp: float
    mod_freq: float
    power: float


@dataclass(frozen=True)
class RecoPars:
    img_size: int
    filter: str
    cutoff: float
    alpha_no: int
    beta_no: int
    gamma_no: int
    alphas: List[float]
    betas: List[float]
    gammas: List[float]


@dataclass
class Config:
    path: str
    sinogram_filepath: str = field(init=False)
    reference_filepath: str = field(init=False)
    output_dir: str = field(init=False)
    img_size: int = field(init=False)
    filter: str = field(init=False)
    cutoff: float = field(init=False)

    def __post_init__(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
        self.sinogram_filepath = data["Paths"]["input_sino_file"]
        self.reference_filepath = data["Paths"]["input_ref_file"]
        self.output_dir = data["Paths"]["output_dir"]
        self.img_size = data["Reconstruction"]["img_size"]
        self.filter = data["Reconstruction"]["filter"]
        self.cutoff = data["Reconstruction"]["cutoff"]


@dataclass
class Reconstruction:
    acq_pars: AcqPars
    reco_pars: RecoPars
    sinogram: np.ndarray
    reco_array: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        img_type = self.acq_pars.img_type
        img_size = self.reco_pars.img_size

        if img_type == '2D':
            shape = (img_size, img_size)
        elif img_type in ('3D', '3DS'):
            shape = (img_size, img_size, img_size)
        elif img_type == '4D':
            shape = (img_size, img_size, img_size, img_size)
        else:
            raise ValueError(f'Unsupported image type: {img_type}')

        self.reco_array = np.zeros(shape, dtype=float)
