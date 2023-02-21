import naclib.stpol
import naclib.util
import numpy as np


def location_arrays_translate_and_scale():
    locs0 = 0.9500000000000 * np.array([[0.0,   1.0],
                        [-0.5,  0.5],   [0.0,   0.5],   [0.5,   0.5],
        [-1.0,  0.0],   [-0.5,  0.0],   [0.0,   0.0],   [0.5,   0.0],   [1.0,   0.0],
                        [-0.5,  -0.5],  [0.0,  -0.5],   [0.5,   -0.5],
                                        [0.0,  -1.0]])
    locs1 = 1.02 * locs0 + np.array([[0.01, 0.01]])
    return locs0, locs1


def coefficients_translate_and_scale():
    a_S = {1: 0.0, 2: 0.01, 3: 0.01, 4: 0.01 * np.sqrt(2), 5: 0}
    a_T = {4: 0}
    return a_S, a_T


def test_get_coefs_translate_and_scale():

    locs0, locs1 = location_arrays_translate_and_scale()
    a_S_ref, a_T_ref = coefficients_translate_and_scale()

    # Get distortion grid.
    D = np.zeros(locs0.shape)
    D[:, 0] = locs1[:, 0] - locs0[:, 0]
    D[:, 1] = locs1[:, 1] - locs0[:, 1]

    # Get ST polynomial decomposition coefficients.
    stpol = naclib.stpol.STPolynomials(j_max_S=5, j_max_T=5)
    a_S, a_T = stpol.get_decomposition(locs0, D)

    # Check result.
    for key, value in a_S.items():
        assert np.abs(a_S[key] - a_S_ref[key]) < 1e-8
    for key, value in a_T.items():
        assert np.abs(a_T[key] - a_T_ref[key]) < 1e-8


def test_apply_coefs_translate_and_scale():

    locs0, locs1 = location_arrays_translate_and_scale()
    a_S, a_T = coefficients_translate_and_scale()

    # Get correction field.
    stpol = naclib.stpol.STPolynomials(j_max_S=5, j_max_T=5)
    P = stpol.get_field(locs0, a_S, a_T)

    # Correct spot locations, scale back from unit circle to original scale, and save.
    locs_corrected = locs0 + P

    assert(np.max(np.absolute(locs_corrected - locs1) < 1e-16))
