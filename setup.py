import setuptools

long_description = """
NAClib is a python library for applying a global alignment method
for single-molecule fluorescence microscopy, using S/T Polynomial
Decomposition (STPD). STPD employs linear combinations of Zernike
polynomial gradients to decompose the distortion between two images,
correcting both affine and higher-order components of the distortion
in a single step, while requiring only minimal reference data.
"""

pk = setuptools.find_packages()

setuptools.setup(
    name="naclib",
    version="1",
    author="Edo van Veen, Kaley McCluskey",
    author_email="E.N.W.vanVeen@tudelft.nl",
    description="Non-Affine Corrections for microscope images",
    long_description=long_description,
    url="https://gitlab.tudelft.nl/nynke-dekker-lab/public/naclib",
    packages=pk,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
    install_requires=[
        'scipy',
        'numpy',
        'zernike'
    ]
)
