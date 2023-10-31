# Simbols

## Name
SImilarity Measures for biOLogical Systems - short SiMBols

## Description
SiMBols is meant to supply a fairly easy to use tool to apply similarity measures on trajectory data obtained, while utilizing existing measures from different libraries.
SiMBols includes:
* Discrete Fréchet Distance (DFD)
* Discrete Weak Fréchet Distance (DWFD)
* Dynamic Time Warping (DTW)
* Hausdorff Distance (HD)
* Longest Common SubSequence (LCSS)
* Difference Distance Matrix (DDM)
* Wasserstein distance (WD)
* Kullback-Leibler Divergence (KLD)

Additionally, SiMBols includes two routines to read out protein simulation trajectories and align them for further analyses, for instance, employing the similarity measures.

Two working examples are supplied including input files, one dealing with the protein routines and one exclusively calculating the similarity measures. Files can be found at
* Example/example.py (Similarity Measure Example)
* ProteinPreprocessing/Example/example.py

The package is part of a publication available in [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0284736).

## Minimum Requirement
SiMBols requires at least python 3.6 to run and some of the dependencies listed below, depending on the needed parts.

## Installation
At this time, the package can be cloned to a working directory and imported to the code. The repository is located [here](gitlab.uni-oldenburg.de/quantbiolab/simbols). It is also registered in PyPI and can be installed using **pip install simbols**. The most recent version will always be the one on gitlab.

## Dependencies
The following python packages are loaded:
mdtraj, numpy, time, rmsd, concurrent.futures, scipy.stats, scipy.spatial.distance, tqdm

## Usage
The Usage is explained in the two examples, a quick overview however is the following workflow
1. Load a trajectory into a Trajectory class object
2. Load a second trajectory into a Trajectory class object
3. Create a Comparer object from the two Trajectory objects
4. Calculate the needed similarity measures, the results are saved to the comparer object
5. Save the results, plot the results

## Support
For support, send an email to fabian.schuhmann@nbi.ku.dk or open an issue. 

## Authors and acknowledgment
The package is written by 
* Fabian Schuhmann,  University of Copenhagen
* Leonie Ryvkin,  Technische Universiteit Eindhoven
* James D. McLaren,  Carl-von-Ossietzky Universität Oldenburg
* Luca Gerhards,  Carl-von-Ossietzky Universität Oldenburg
* Ilia A. Solov'yov,  Carl-von-Ossietzky Universität Oldenburg   

with acknowledgements detailed below:

Programming help was received from Jeróme Urhausen and Georg Manthey. The authors would like to thank Volkswagen Foundation (Lichtenberg Professorship to IAS), the DFG, German Research Foundation, (GRK1885 - Molecular Basis of Sensory Biology and SFB 1372 – Magnetoreception and Navigation in Vertebrates), Ministry for science and culture of Lower Saxony (Simulations meet experiments on the nanoscale: Opening up the quantum world to artificial intelligence (SMART)). Computational resources for the simulations were provided by the CARL Cluster at the Carl-von-Ossietzky Universität Oldenburg, which is supported by the DFG and the ministry for science and culture of Lower Saxony. The work was also supported by the North-German Supercomputing Alliance (HLRN).

## License
MIT
