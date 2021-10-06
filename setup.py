from distutils.core import setup

setup(
  name = 'naclib',
  packages = ['naclib'],
  version = '0.1',
  license='MIT',
  description = 'Non-Affine Corrections on microscopy images using S/T Polynomial Decomposition',
  author = 'Edo van Veen & Kaley McCluskey',
  author_email = 'e.n.w.vanveen@tudelft.nl',
  url = 'https://gitlab.tudelft.nl/nynke-dekker-lab/public/naclib',
  keywords = ['colocalization', 'microscopy', 'distortion correction', 'STPD'],
  install_requires=[
        'scipy',
        'numpy',
        'zernike'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Scientists',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
  ],
)