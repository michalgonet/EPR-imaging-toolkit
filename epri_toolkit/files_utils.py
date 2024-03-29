from typing import Dict, List, Tuple
import os
import re
import numpy as np
from pathlib import Path
from epri_toolkit.classes import AcqPars, RawData, Config


def _get_bruker_files_path(sino_path: str) -> List[Path]:
    sinogram_path = Path(sino_path)
    if sinogram_path.suffix.upper() == '.DTA':
        paths = [sinogram_path, sinogram_path.with_suffix('.DSC')]
    elif sinogram_path.suffix.upper() == '.DSC':
        paths = [sinogram_path.with_suffix('.DTA'), sinogram_path]
    else:
        raise ValueError('Incorrect file format. Supported formats are .DTA and .DSC')
    return paths


def _load_dta_file(path) -> np.ndarray:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    try:
        with open(path, 'rb') as f:
            return np.frombuffer(f.read(), dtype='>d')
    except Exception as e:
        raise Exception(f"Error loading file: {path}. {e}")


def _load_dsc_file(file_path: Path) -> Dict[str, List[str]]:
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    data_dict = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('#') or not line:
                continue

            match = re.match(r'([a-zA-Z0-9_]+)\s+([\w.]+)\s*(\w*)\s*(.*)', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                unit = match.group(3)
                extra_info = match.group(4)

                try:
                    value = float(value)
                except ValueError:
                    try:
                        value = int(value)
                    except ValueError:
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False

                if key in data_dict:
                    data_dict[key].append(value)
                else:
                    data_dict[key] = [value]

                if unit:
                    data_dict[key].append(unit)

                if extra_info:
                    data_dict[key].append(extra_info)

    for key in data_dict:
        data_dict[key] = [str(value).strip("'") for value in data_dict[key]]

    return data_dict


def load_bruker_files(path: str) -> Tuple[np.ndarray, Dict[str, List[str]]]:
    file_paths = _get_bruker_files_path(path)
    if len(file_paths) < 2:
        raise ValueError("Both DTA and DSC files are required.")
    return _load_dta_file(file_paths[0]), _load_dsc_file(file_paths[1])


def get_acq_pars(raw_pars: Dict[str, List[str]]) -> AcqPars:
    return AcqPars(
        data=str(raw_pars["DATE"][0]),
        time=str(raw_pars["TIME"][0]),
        exp_type=str(raw_pars["EXPT"][0]),
        scan_time=str(raw_pars["SWTime"][0]),
        img_time=str(raw_pars["TotalTime"][0]),
        img_type=str(" ".join(raw_pars["ImageType"])),
        orient=str(raw_pars["ImageOrient"][0]),
        points=int(float(raw_pars["XPTS"][0])),
        alpha_no=int(float(raw_pars["NrOfAlpha"][0])),
        beta_no=int(float(raw_pars["NrOfBeta"][0])),
        gamma_no=int(float(raw_pars["NrOfPsi"][0])),
        first_alpha=float(raw_pars["FirstAlpha"][0]),
        max_gamma=float(raw_pars["MaxPsi"][0]),
        gradient=float(raw_pars["GRAD"][0] if "GRAD" in raw_pars else raw_pars["AnglePsi"][0]),
        sweep=float(raw_pars["SweepWidth"][0]),
        center_field=float(raw_pars["CenterField"][0]),
        mod_amp=float(raw_pars["ModAmp"][0]),
        mod_freq=float(raw_pars["ModFreq"][0]),
        power=float(raw_pars["Power"][0])
    )


def get_raw_data(config: Config) -> RawData:
    try:
        raw_sino, raw_sino_pars = load_bruker_files(config.sinogram_filepath)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e}")

    try:
        raw_ref, raw_ref_pars = load_bruker_files(config.reference_filepath) if config.deconvolution else (None, None)
    except FileNotFoundError:
        raw_ref, raw_ref_pars = (None, None)

    return RawData(
        raw_sinogram=raw_sino,
        raw_sinogram_pars=raw_sino_pars,
        raw_ref=raw_ref,
        raw_ref_pars=raw_ref_pars
    )
