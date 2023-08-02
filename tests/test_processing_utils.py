import unittest

import numpy as np

from epri_toolkit.processing_utils import create_sino2d, sinogram_interpolation, sinogram_integration


class CreateSino2DTestCase(unittest.TestCase):
    def test_create_sino2d(self):
        raw_data = np.random.rand(100)
        acq_pars = AcqPars(points=50)
        result = create_sino2d(raw_data, acq_pars)
        self.assertEqual(result.shape, (50, 2))

    def test_sinogram_interpolation(self):
        sinogram = np.random.rand(256, 200)
        reco_pars = RecoPars(img_size=128)
        result = sinogram_interpolation(sinogram, reco_pars)
        self.assertEqual(result.shape, (128, 200))

    def test_sinogram_integration(self):
        sinogram = np.random.rand(100, 200)
        result = sinogram_integration(sinogram)
        self.assertEqual(result.shape, (100, 200))
        self.assertTrue(np.allclose(result[0], np.cumsum(sinogram, axis=0)[0]))


# Dummy class to represent the AcqPars object used in the function
class AcqPars:
    def __init__(self, points):
        self.points = points


# Dummy class to represent the RecoPars object used in the function
class RecoPars:
    def __init__(self, img_size):
        self.img_size = img_size


if __name__ == '__main__':
    unittest.main()
