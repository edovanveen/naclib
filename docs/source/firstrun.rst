First run
=========

The calibration data needs to be:
- of size `(n, 2)`, with `n` the number of spots
- spot-paired
- rescaled to within the unit circle

.. code-block:: python

    locs0_calibration  # Calibration data for channel 0
    locs1_calibration  # Calibration data for channel 1

There are some utility functions available to help you rescale
data to the unit circle, and find spot pairs in the calibration dataset:

.. code-block:: python

    # Find the nearest neighbours; rescale to unit circle.
    fig_size = [512, 512]  # image size in pixels
    threshold = 5  # threshold in pixels for nearest neighbor detection
    mapping = naclib.util.find_neighbours(locs0_calibration_raw,
                                          locs1_calibration_raw,
                                          threshold=threshold)
    locs0_pairs, locs1_pairs = naclib.util.make_pairs(locs0_raw, locs1_raw, mapping)
    locs0_calibration, scale = naclib.util.loc_to_unitcircle(locs0_pairs, fig_size)
    locs1_calibration, scale = naclib.util.loc_to_unitcircle(locs1_pairs, fig_size)

The measurement data needs to be:
- of size `(n0, 2)`, `(n1, 2)` with `n0, n1` the number of spots in channels 0 and 1
- rescaled to within the unit circle

.. code-block:: python

    locs0_measurement  # Measurement data for channel 0
    locs1_measurement  # Measurement data for channel 1

The easiest way to run the calibration and correction is to use `naclib.DistortionCorrection`
and its SciPy-style fit/predict methods:

.. code-block:: python

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
