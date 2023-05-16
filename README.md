# NAClib: Non-Affine Corrections for microscope images

NAClib is a python library for applying a global alignment method
for single-molecule fluorescence microscopy, using S/T Polynomial 
Decomposition (STPD). STPD employs linear combinations of Zernike 
polynomial gradients to decompose the distortion between two images, 
correcting both affine and higher-order components of the distortion 
in a single step, while requiring only minimal reference data.

## Full documentation

Full documentation is available at https://edovanveen.github.io/naclib/.

## Installation

### Manual installation

First make sure you have python 3.8 or higher installed. Then, clone
this git repo onto your computer, and install all the packages listed
in `requirements.txt`. After adding the repo root directory to
your python path, you are ready to go.

### Installation with pip

```
pip install naclib
```

## Usage

The calibration data needs to be:
- of size `(n, 2)`, with `n` the number of spots
- spot-paired
- rescaled to within the unit circle

```python 
locs0_calibration  # Calibration data for channel 0
locs1_calibration  # Calibration data for channel 1
```

There are some utility functions available to help you rescale
data to the unit circle, and find spot pairs in the calibration dataset:

```python
# Find the nearest neighbours; rescale to unit circle.
fig_size = [512, 512]  # image size in pixels
threshold = 5  # threshold in pixels for nearest neighbor detection
mapping = naclib.util.find_neighbours(locs0_calibration_raw, 
                                      locs1_calibration_raw, 
                                      threshold=threshold)
locs0_pairs, locs1_pairs = naclib.util.make_pairs(locs0_raw, locs1_raw, mapping)
locs0_calibration, scale = naclib.util.loc_to_unitcircle(locs0_pairs, fig_size)
locs1_calibration, scale = naclib.util.loc_to_unitcircle(locs1_pairs, fig_size)
```

The measurement data needs to be:
- of size `(n0, 2)`, `(n1, 2)` with `n0, n1` the number of spots in channels 0 and 1
- rescaled to within the unit circle

```python
locs0_measurement  # Measurement data for channel 0
locs1_measurement  # Measurement data for channel 1
```

The easiest way to run the calibration and correction is to use `naclib.DistortionCorrection`
and its sklearn-style fit/predict methods:

```python
import naclib
import numpy as np

# Get distortion field.
distortion_field = np.zeros(locs0_calibration.shape)
distortion_field[:, 0] = locs1_calibration[:, 0] - locs0_calibration[:, 0]
distortion_field[:, 1] = locs1_calibration[:, 1] - locs0_calibration[:, 1]

# Get ST polynomial decomposition coefficients.
model = naclib.DistortionCorrection()
model.fit(locs0_calibration, distortion_field)

# Get correction field.
correction_field = model.predict(locs1_measurement)

# Apply correction.
locs1_measurement_corrected = locs1_measurement + correction_field
```

Other examples are available in the `notebooks/` directory.

## Authors & citation

- *Edo van Veen*, Nynke Dekker Lab, Bionanoscience, TU Delft
- *Kaley McCluskey*, Nynke Dekker Lab, Bionanoscience, TU Delft

If you use this software, please cite:

McCluskey, Kaley A., et al. "Global correction of optical distortions in multicolor single-molecule microscopy using Zernike polynomial gradients." *Optics Express* 29.25 (2021): 42251-42264.

[https://doi.org/10.1364/OE.445230](https://doi.org/10.1364/OE.445230)

## Build documentation

```
sphinx-build -b html docs/source docs/build
```

## Distribute new version

- Change version in `setup.py` (2x)
- Change version in `docs/source/conf.py`
- Run `python setup.py sdist`
- Git push
- Run `twine upload --repository-url https://pypi.org/project/naclib/ dist\naclib-<newversion>.tar.gz
`