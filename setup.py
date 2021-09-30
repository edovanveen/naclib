"""
To use locally:

"setup.py develop"

To remove from current environment:
"setup.py develop --uninstall"

"""
import setuptools
import os,shutil


long_description = """
"""

pk = setuptools.find_packages(exclude=['utils'])

setuptools.setup(
    name="naclib",
    version="1",
    author="Edo van Veen, Kaley McCluskey",
    author_email="E.N.W.vanVeen@tudelft.nl",
    description="Non-Affine Corrections for microscope images",
    long_description=long_description,
 #   long_description_content_type="text/markdown",
    url="https://github.com/qnano/photonpy",
    packages=pk,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
	install_requires=[
		'scipy', 
		'numpy',
		'matplotlib',
        'pandas',
        'zernike'
	]
)
