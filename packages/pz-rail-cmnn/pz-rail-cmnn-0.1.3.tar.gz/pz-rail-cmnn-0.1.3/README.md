![DOI](https://zenodo.org/badge/223043497.svg)
![PyPI](https://img.shields.io/pypi/v/pz-rail-cmnn)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/LSSTDESC/rail_cmnn)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/LSSTDESC/rail_cmnn/main.yml)

# rail_cmnn

RAIL interface to Melissa Graham's CMNN algorithm.  A slight modification of the original code found here: <br>
[dirac-institute/CMNN_Photoz_estimator](https://github.com/dirac-institute/CMNN_Photoz_Estimator)

See https://ui.adsabs.harvard.edu/abs/2018AJ....155....1G/abstract
for more details on the code
Any use of `rail_cmnn` in a paper or report should cite [Graham et al. (2018)](https://ui.adsabs.harvard.edu/abs/2018AJ....155....1G/abstract).

The current version of the code consists of a training stage, `CMNNInformer`, that computes colors for a set of training data and an estimation stage `CMNNEstimator` that calculates the Mahalanobis distance to each training galaxy for each test galaxy. The mean value of this Guassian PDF can be estimated in one of three ways (see `selection mode` below), and the width is determined by the standard deviation of training galaxy redshifts within the threshold Mahalanobis distance.  Future implementation improvements may change the output format to include multiple Gaussians.

For the color calculation, there is an option for how to treat the "non-detections" in a band: the default choice is to ignore any colors that contain a non-detect magnitude and adjust the number of degrees of freedom in the Mahalanobis distance accordingly (this is how the CMNN algorithm was originally implemented). Or, if the configuration parameter `nondetect_replace` is set to `True` in `CMNNInformer`, the non-detected magnitudes will be replaced with the 1-sigma limiting magnitude in each band as supplied by the user via the `mag_limits` configuration parameter (or by the default 1-sigma limits if the user does not supply specific numbers). We have not done any exploration of the relative performance of these two choices, but note that there is not a significant performance difference in terms of runtime between the two methods.

`CMNNInformer` takes in a training data set and returns a model file that simply consists of the computed colors and color errors (magnitude errors added in quadrature) for that dataset, the model to be used in the `CMNNEstimator` stage. A modification of the original CMNN algorithm, "nondetections" are now replaced by the 1-sigma limiting magnitudes and the non-detect magnitude errors replaced with a value of 1.0.  The config parameters that can be set by the user for `CMNNInformer` are:<br>
- `bands`: list of the band names that should be present in the input data.<br>
- `err_bands`: list of the magnitude error column names that should be present in the input data.<br>
- `redshift_col`: a string giving the name for the redshift column present in the input data.<br>
- `mag_limits`: a dictionary with keys that match those in `bands` and a float with the 1 sigma limiting magnitude for each band.<br>
- nondetect_val: float or `np.nan`, the value indicating a non-detection, which will be replaced by the values in `mag_limits`.<br>
- `nondetect_replace`: bool, if set to False (the default) this option ignores colors with non-detected values in the Mahalanobis distance calculation, with a corresponding drop in the degrees of freedom value. If set to True, the method will replace non-detections with the 1-sigma limiting magnitudes specified via `mag_limits` (or default 1-sigma limits if not supplied), and will use all colors in the Mahalanobis distance calculation.


The parameters that can be set via the `config_params` in `CMNNEstimator` are described in brief below:<br>
- `bands`, `err_bands`, `redshift_col`, `mag_limits` are all the same as described above for `CMNNInformer`.<br>
- `ppf_value`: float, usually 0.68 or 0.95, which sets the value of the PPF used in the Mahalanobis distance calculation.<br>
- `selection_mode`: int, selects how the central value of the Gaussian PDF is calculated in the algorithm, if set to `0` randomly chooses from set within the Mahalanobis distance, if set to `1` chooses the nearest neighbor point, if set to `2` adds a distance weight to the random choice.<br>
- `min_n`: int, the minimum number of training galaxies to use.<br>
- `min_thresh`: float, the minimum threshold cutoff.  Values smaller than this threshold value will be ignored.<br>
- `min_dist`: float, the minimum Mahalanobis distance. Values smaller than this will be ignored.<br>
- `bad_redshift_val`: float, in the unlikely case that there are not enough training galaxies, this central redshift will be assigned to galaxies.<br>
- `bad_redshift_err`: float, in the unlikely case that there are not enough training galaxies, this Gaussian width will be assigned to galaxies.<br>

# RAIL: Redshift Assessment Infrastructure Layers

RAIL is a flexible software library providing tools to produce at-scale photometric redshift data products, including uncertainties and summary statistics, and stress-test them under realistically complex systematics.
A detailed description of RAIL's modular structure is available in the [Overview](https://lsstdescrail.readthedocs.io/en/latest/source/overview.html) on ReadTheDocs.

RAIL serves as the infrastructure supporting many extragalactic applications of the Legacy Survey of Space and Time (LSST) on the Vera C. Rubin Observatory, including Rubin-wide commissioning activities. 
RAIL was initiated by the Photometric Redshifts (PZ) Working Group (WG) of the LSST Dark Energy Science Collaboration (DESC) as a result of the lessons learned from the [Data Challenge 1 (DC1) experiment](https://academic.oup.com/mnras/article/499/2/1587/5905416) to enable the PZ WG Deliverables in [the LSST-DESC Science Roadmap (see Sec. 5.18)](https://lsstdesc.org/assets/pdf/docs/DESC_SRM_latest.pdf), aiming to guide the selection and implementation of redshift estimators in DESC analysis pipelines.
RAIL is developed and maintained by a diverse team comprising DESC Pipeline Scientists (PSs), international in-kind contributors, LSST Interdisciplinary Collaboration for Computing (LINCC) Frameworks software engineers, and other volunteers, but all are welcome to join the team regardless of LSST data rights. 

## Installation

Installation instructions are available under [Installation](https://lsstdescrail.readthedocs.io/en/latest/source/installation.html) on ReadTheDocs.

## Contributing

The greatest strength of RAIL is its extensibility; those interested in contributing to RAIL should start by consulting the [Contributing guidelines](https://lsstdescrail.readthedocs.io/en/latest/source/contributing.html) on ReadTheDocs.

## Citing RAIL

RAIL is open source and may be used according to the terms of its [LICENSE](https://github.com/LSSTDESC/RAIL/blob/main/LICENSE) [(BSD 3-Clause)](https://opensource.org/licenses/BSD-3-Clause).
If you make use of the ideas or software here in any publication, you must cite this repository <https://github.com/LSSTDESC/RAIL> as "LSST-DESC PZ WG (in prep)" with the [Zenodo DOI](https://doi.org/10.5281/zenodo.7017551).
Please consider also inviting the developers as co-authors on publications resulting from your use of RAIL by [making an issue](https://github.com/LSSTDESC/RAIL/issues/new/choose).
Additionally, several of the codes accessible through the RAIL ecosystem must be cited if used in a publication.
A convenient list of what to cite may be found under [Citing RAIL](https://lsstdescrail.readthedocs.io/en/latest/source/citing.html) on ReadTheDocs.
