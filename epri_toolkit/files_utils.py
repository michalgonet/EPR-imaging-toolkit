from typing import Dict, List, Tuple
import numpy as np
from pathlib import Path
from epri_toolkit.classes import Config
from epri_toolkit.classes import AcqPars


def _get_bruker_files_path(sino_path: str) -> List[Path]:
    sinogram_path = Path(sino_path)
    if sinogram_path.suffix.upper() == '.DTA':
        paths = [sinogram_path, sinogram_path.with_suffix('.DSC')]
    elif sinogram_path.suffix.upper() == '.DSC':
        paths = [sinogram_path.with_suffix('.DTA'), sinogram_path]
    else:
        raise KeyError('Incorrect file format')
    return paths


def _load_dta_file(path) -> np.ndarray:
    with open(path, 'rb') as f:
        return np.frombuffer(f.read(), dtype='>d')


def _load_dsc_file(path: Path) -> Dict[str, str]:
    with open(path) as f:
        all_lines = f.readlines()

    pars_raw = {}
    for line in all_lines:
        if line.startswith(('*', '.DVC', '#')):
            continue
        words = line.strip().split()
        if len(words) > 1:
            dict_key = f'{words[0]}_{words[2]}' if len(words) == 3 else words[0]
            pars_raw[dict_key] = words[1]
    return pars_raw


def load_bruker_files(config: Config) -> Tuple[np.ndarray, AcqPars]:
    paths = _get_bruker_files_path(config.sinogram_filepath)
    raw_sinogram, raw_pars = _load_dta_file(paths[0]), _load_dsc_file(paths[1])

    acq_pars = AcqPars(data=raw_pars["DATE"],
                       time=raw_pars["TIME"],
                       scan_time=raw_pars["SWTime_s"],
                       img_time=raw_pars["TotalTime_min"],
                       img_type=raw_pars["ImageType"],
                       orient=raw_pars["ImageOrient"],
                       points=int(raw_pars["XPTS"]),
                       alpha_no=int(raw_pars["NrOfAlpha"]),
                       beta_no=int(raw_pars["NrOfBeta"]),
                       gamma_no=int(raw_pars["NrOfPsi"]),
                       first_alpha=float(raw_pars["FirstAlpha_deg"]),
                       max_gamma=float(raw_pars["MaxPsi_deg"]),
                       gradient=float(raw_pars["GRAD"]),
                       sweep=float(raw_pars["SweepWidth_G"]),
                       center_field=float(raw_pars["CenterField_G"]),
                       mod_amp=float(raw_pars["ModAmp_G"]),
                       mod_freq=float(raw_pars["ModFreq_kHz"]),
                       power=float(raw_pars["Power_mW"]))

    sinogram_2d = np.reshape(raw_sinogram,
                             [acq_pars.points, acq_pars.alpha_no * acq_pars.beta_no * acq_pars.gamma_no],
                             order='F')
    return sinogram_2d, acq_pars
