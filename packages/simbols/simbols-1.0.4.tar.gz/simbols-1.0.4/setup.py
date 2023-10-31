import setuptools
from pathlib import Path


long_description=(Path(__file__).parent / "README.md").read_text()

setuptools.setup(
    name="simbols",
    version="1.0.4",
    author="Fabian Schuhmann",
    author_email="fabian.schuhmann@nbi.ku.dk",
    description="A package containing similarity measures for life science purposes. The package contains or uses Fréchet Distance, Dynamic Time Warping, Hausdorff Distance, Longest Common Subsequence, Difference Distance Matrix, Wasserstein Distance and the Kullback-Leiber Divergence (Jenssen-Shannon Distance)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    url='https://gitlab.uni-oldenburg.de/quantbiolab/simbols',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'scipy',
        'mdtraj',
        'rmsd'
    ]
)
