First run
=========

The calibration data needs to be:

- of size ``(n, 2)``, with ``n`` the number of spots
- spot-paired, so ``locs0_calibration[i, :]`` corresponds to ``locs1_calibration[i, :]`` for each ``i``
- rescaled to within the unit circle

.. code-block:: python

    locs0_calibration  # Calibration data for channel 0
    locs1_calibration  # Calibration data for channel 1

There are some utility functions available to help you rescale
data to the unit circle, and find spot pairs in the calibration dataset:

.. code-block:: python

    import naclib.util

    # Find the nearest neighbours; rescale to unit circle.
    fig_size = [512, 512]  # image size in pixels
    threshold = 5  # threshold in pixels for nearest neighbor detection

    # Find nearest neighbours within threshold distance.
    mapping = naclib.util.find_neighbours(locs0_calibration_raw,
                                          locs1_calibration_raw,
                                          threshold=threshold)

    # Make spot pairs.
    locs0_pairs, locs1_pairs = naclib.util.make_pairs(locs0_raw, locs1_raw, mapping)

    # Rescale to unit circle.
    locs0_calibration, scale = naclib.util.loc_to_unitcircle(locs0_pairs, fig_size)
    locs1_calibration, scale = naclib.util.loc_to_unitcircle(locs1_pairs, fig_size)

Location arrays can be transformed back to their original coordinate system using:

.. code-block:: python

    locs0_orig = naclib.util.unitcircle_to_loc(locs0_calibration, fig_size)

The measurement data needs to be:

- of size ``(n0, 2)``, ``(n1, 2)`` with ``n0, n1`` the number of spots in channels 0 and 1
- rescaled to within the unit circle

.. code-block:: python

    locs0_measurement  # Measurement data for channel 0
    locs1_measurement  # Measurement data for channel 1

The easiest way to run the calibration and correction is to use ``naclib.DistortionCorrection``
and its sklearn-style fit/predict methods:

.. code-block:: python

    import naclib
    import numpy as np

    # Get distortion field.
    distortion_field = locs1_calibration - locs0_calibration

    # Get ST polynomial decomposition coefficients.
    model = naclib.DistortionCorrection()
    model.fit(locs0_calibration, distortion_field)

    # Get correction field.
    correction_field = model.predict(locs1_measurement)

    # Apply correction.
    locs1_measurement_corrected = locs1_measurement + correction_field
