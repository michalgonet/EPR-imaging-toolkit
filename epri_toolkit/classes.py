from dataclasses import dataclass, field
from typing import List, Dict
import json

import numpy as np


@dataclass(frozen=True)
class AcqPars:
    data: str
    time: str
    scan_time: str
    img_time: str
    exp_type: str
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
class RawData:
    raw_sinogram: np.ndarray
    raw_sinogram_pars: Dict[str, List[str]]
    raw_ref: np.ndarray = None
    raw_ref_pars: Dict[str, List[str]] = None


@dataclass(frozen=True)
class RecoPars:
    method: str
    img_size: int
    filter_spat: str
    filter_spec: str
    deconvolution: bool
    deco_filter: float
    cutoff_spat: float
    cutoff_spec: float
    baseline: bool
    alpha_no: int
    beta_no: int
    gamma_no: int
    alphas: List[float]
    betas: List[float]
    gammas: List[float]
    sart_iters: List[int]
    sart_relax: float


@dataclass
class Config:
    path: str

    def __post_init__(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
        self.sinogram_filepath = data["Paths"]["input_sino_file"]
        self.reference_filepath = data["Paths"]["input_ref_file"]
        self.output_dir = data["Paths"]["output_dir"]
        self.img_size = data["Reconstruction"]["img_size"]
        self.filter_spat = data["Reconstruction"]["filter_spatial"]
        self.filter_spec = data["Reconstruction"]["filter_spectral"]
        self.cutoff_spat = data["Reconstruction"]["cutoff_spatial"]
        self.cutoff_spec = data["Reconstruction"]["cutoff_spectral"]
        self.deconvolution = data["Reconstruction"]["deconvolution"]
        self.deco_filter = data["Reconstruction"]["deconvolution_filter"]
        self.reco_method = data["Reconstruction"]["method"]
        self.baseline = data["Reconstruction"]["remove_baseline"]
        self.sart_iters = data["Reconstruction"]["sart_iterations"]
        self.sart_relax = data["Reconstruction"]["sart_relaxation"]

