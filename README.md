# NAClib: Non-Affine Corrections for microscope images

NAClib is a python library for applying a global alignment method
for single-molecule fluorescence microscopy, using S/T Polynomial 
Decomposition (STPD). STPD employs linear combinations of Zernike 
polynomial gradients to decompose the distortion between two images, 
correcting both affine and higher-order components of the distortion 
in a single step, while requiring only minimal reference data.

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

### Full documentation

Full documentation is available at www.edovanveen.com/naclib.

### Getting decomposition coefficients for a reference grid

First, we need to find the STPD coefficients for a reference measurement.
In this example, we use locations stored in `'example/locs_green.csv'` and
`'example/locs_red.csv'` to determine the distortion field. The result
is stored in a dataframe named `'example/STcoefficients.csv'`.

```python
# Imports.
import naclib.stpol
import naclib.util
import pandas as pd
import numpy as np

# Input.
# Spots in df_locs0 are shifted towards spots in df_locs1, the latter remain static.
# These files need to have an 'x' and a 'y' column, with pixel units.
df_locs0 = pd.read_csv('example/locs_green.csv')
df_locs1 = pd.read_csv('example/locs_red.csv')
fig_size = [512, 256]  # Original image size, needed for rescaling to unit circle.
threshold = 5  # Nearest neighbour search threshold in pixels.
j_max_S = 28  # Max term for S polynomials.
j_max_T = 15  # Max term for T polynomials.

# Output file.
output_coefficients = 'example/STcoefficients.csv'

# Find spot pairs, by finding nearest neighbours between locs0 and locs1.
locs0_raw = np.zeros((len(df_locs0), 2))
locs0_raw[:, 0] = df_locs0['x']  # If locs0 and locs1 are not well aligned, you can add an x-translation here manually.
locs0_raw[:, 1] = df_locs0['y']  # If locs0 and locs1 are not well aligned, you can add a y-translation here manually.
locs1_raw = np.zeros((len(df_locs1), 2))
locs1_raw[:, 0] = df_locs1['x']
locs1_raw[:, 1] = df_locs1['y']
mapping = naclib.util.find_neighbours(locs0_raw, locs1_raw, threshold=threshold)
locs0_pairs, locs1_pairs = naclib.util.make_pairs(locs0_raw, locs1_raw, mapping)

# Rescale spot pairs to unit circle.
locs0, scale = naclib.util.loc_to_unitcircle(locs0_pairs, fig_size)
locs1, scale = naclib.util.loc_to_unitcircle(locs1_pairs, fig_size)

# Get distortion grid.
D = np.zeros(locs0.shape)
D[:, 0] = locs1[:, 0] - locs0[:, 0]
D[:, 1] = locs1[:, 1] - locs0[:, 1]

# Get ST polynomial decomposition coefficients.
stpol = naclib.stpol.STPolynomials(j_max_S=j_max_S, j_max_T=j_max_T)
a_S, a_T = stpol.get_decomposition(locs0, D)

# Save resulting coefficients.
dict_coefs = {'type': [], 'term': [], 'value': []}
for term, value in a_S.items():
    dict_coefs['type'].append('S')
    dict_coefs['term'].append(term)
    dict_coefs['value'].append(value)
for term, value in a_T.items():
    dict_coefs['type'].append('T')
    dict_coefs['term'].append(term)
    dict_coefs['value'].append(value)
df_coefs = pd.DataFrame(dict_coefs)
df_coefs.to_csv(output_coefficients)
```

After that, we can visualize the result using:

```python
import matplotlib.pyplot as plt

# Show original distortion map.
magnitude_D = np.hypot(D[:, 0], D[:, 1]) * scale
plt.figure()
q = plt.quiver(locs0[:, 0], locs0[:, 1], D[:, 0], D[:, 1], magnitude_D, 
               pivot='mid', clim=(0, 1.2 * scale * np.amax(D)))
plt.colorbar(q)
plt.show()
plt.close()

# Show correction field.
P = stpol.get_field(locs0, a_S, a_T)
magnitude_P = np.hypot(P[:, 0], P[:, 1]) * scale
plt.figure()
q = plt.quiver(locs0[:, 0], locs0[:, 1], P[:, 0], P[:, 1], magnitude_P, 
               pivot='mid', clim=(0, 1.2 * scale * np.amax(D)))
plt.colorbar(q)
plt.show()
plt.close()

# Show residual distortion grid.
locs0_corrected = locs0 + P
D_res = np.zeros(locs0_corrected.shape)
D_res[:, 0] = locs1[:, 0] - locs0_corrected[:, 0]
D_res[:, 1] = locs1[:, 1] - locs0_corrected[:, 1]
magnitude_res = np.hypot(D_res[:, 0], D_res[:, 1]) * scale
plt.figure()
q = plt.quiver(locs0[:, 0], locs0[:, 1], D_res[:, 0], D_res[:, 1], magnitude_res, 
               pivot='mid', clim=(0, 1.2 * scale * np.amax(D)))
plt.colorbar(q)
plt.show()
plt.close()
```

### Applying correction to a new measurement

The resulting distortion correction can then be applied to a new measurement.
In this example, the locations in `'example/locs_new.csv'` are corrected using
the coefficients generated earlier.

```python
# Imports.
import naclib.stpol
import naclib.util
import pandas as pd
import numpy as np

# Input.
# Spot locations in df_locs (with columns 'x' and 'y') are corrected using coefficients in df_coefs.
df_locs = pd.read_csv('example/locs_new.csv')
df_coefs = pd.read_csv('example/STcoefficients.csv')
fig_size = [512, 256]  # Original image size, needed for rescaling to unit circle.

# Output.
output_locs = 'example/locs_corrected.csv'

# Read input data; scale to unit circle.
locs_raw = np.zeros((len(df_locs), 2))
locs_raw[:, 0] = df_locs['x']
locs_raw[:, 1] = df_locs['y']
locs, scale = naclib.util.loc_to_unitcircle(locs_raw, fig_size)
df_S = df_coefs[df_coefs['type'] == 'S']
df_T = df_coefs[df_coefs['type'] == 'T']
a_S = {row['term']: row['value'] for _, row in df_S.iterrows()} 
a_T = {row['term']: row['value'] for _, row in df_T.iterrows()}
j_max_S = df_S['term'].max()
j_max_T = df_T['term'].max()

# Get correction field.
stpol = naclib.stpol.STPolynomials(j_max_S=j_max_S, j_max_T=j_max_T)
P = stpol.get_field(locs, a_S, a_T)

# Correct spot locations, scale back from unit circle to original scale, and save.
locs_corrected = locs + P
df_locs_corrected = pd.DataFrame()
locs_scaled_corrected = naclib.util.unitcircle_to_loc(locs_corrected, fig_size)
df_locs_corrected['x'] = locs_scaled_corrected[:, 0]
df_locs_corrected['y'] = locs_scaled_corrected[:, 1]
df_locs_corrected.to_csv(output_locs)
```

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
