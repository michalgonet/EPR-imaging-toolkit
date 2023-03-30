from dataclasses import dataclass, field
import json

import numpy as np


@dataclass(frozen=True)
class AcqPars:
    img_type: str
    plane: str
    alpha_no: int
    beta_no: int
    gamma_no: int
    gradient: float


@dataclass(frozen=True)
class RecoPars:
    img_size: int
    filter: str
    cut_off: float


@dataclass
class Config:
    path: str
    input_filepath: str = field(init=False)
    output_dir: str = field(init=False)
    img_type: str = field(init=False)
    plane: str = field(init=False)
    alpha_no: int = field(init=False)
    beta_no: int = field(init=False)
    gamma_no: int = field(init=False)
    gradient: float = field(init=False)
    img_size: int = field(init=False)
    filter: str = field(init=False)
    cut_off: float = field(init=False)

    def __post_init__(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
        self.input_filepath = data["Paths"]["input"]
        self.output_dir = data["Paths"]["output"]
        self.img_type = data["Acq_pars"]["img_type"]
        self.plane = data["Acq_pars"]["plane"]
        self.alpha_no = data["Acq_pars"]["alpha_no"]
        self.beta_no = data["Acq_pars"]["beta_no"]
        self.gamma_no = data["Acq_pars"]["gamma_no"]
        self.gradient = data["Acq_pars"]["gradient"]
        self.img_size = data["Reco_pars"]["img_size"]
        self.filter = data["Reco_pars"]["filter"]
        self.cut_off = data["Reco_pars"]["cutoff"]


@dataclass
class Reconstruction:
    img: np.ndarray = field(init=False)
    acq_pars: AcqPars = field(init=False)
    reco_pars: RecoPars = field(init=False)

    def get_acq_pars(self, config: Config) -> None:
        self.acq_pars = AcqPars(img_type=config.img_type,
                                plane=config.plane,
                                alpha_no=config.alpha_no,
                                beta_no=config.beta_no,
                                gamma_no=config.gamma_no,
                                gradient=config.gradient)

    def get_reco_pars(self, config: Config) -> None:
        self.reco_pars = RecoPars(img_size=config.img_size,
                                  filter=config.filter,
                                  cut_off=config.cut_off)

        if self.acq_pars.img_type == '2D':
            self.img = np.zeros([self.reco_pars.img_size,
                                 self.reco_pars.img_size],
                                dtype=float)
        elif self.acq_pars.img_type == '3D':
            self.img = np.zeros([self.reco_pars.img_size,
                                 self.reco_pars.img_size,
                                 self.reco_pars.img_size],
                                dtype=float)
        elif self.acq_pars.img_type == '4D':
            self.img = np.zeros([self.reco_pars.img_size,
                                 self.reco_pars.img_size,
                                 self.reco_pars.img_size,
                                 self.reco_pars.img_size],
                                dtype=float)
        else:
            raise KeyError("Wrong img type in config file")
