First run
====================================

.. code-block:: python

   # Get decomposition components from calibration measurement.
   stpol = naclib.stpol.STPolynomials(j_max_S=j_max_S, j_max_T=j_max_T)
   a_S, a_T = stpol.get_decomposition(locs_calibration, D)

   # Get correction field.
   P = stpol.get_field(locs, a_S, a_T)

   # Correct spot locations.
   locs_corrected = locs + P
