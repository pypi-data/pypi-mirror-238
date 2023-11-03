# BenchNIRS

[![DOI](https://img.shields.io/badge/doi-10.3389%2Ffnrgo.2023.994969-blue)](https://doi.org/10.3389/fnrgo.2023.994969)
[![License](https://img.shields.io/gitlab/license/29059828)](https://gitlab.com/HanBnrd/benchnirs/-/blob/main/LICENSE)
[![Version](https://img.shields.io/pypi/v/benchnirs)](https://pypi.org/project/benchnirs/)
[![Downloads](https://static.pepy.tech/badge/benchnirs)](https://pepy.tech/project/benchnirs)

<img title="BenchNIRS" align="right" width="100" height="100" src="https://hanbnrd.gitlab.io/assets/img/logos/benchnirs.png" alt="BenchNIRS">

> Benchmarking framework for machine learning with fNIRS

**Links**  
&rarr; [*Latest BenchNIRS version*](https://gitlab.com/HanBnrd/benchnirs)  
&rarr; [*BenchNIRS journal version*](https://gitlab.com/HanBnrd/benchnirs/-/releases/v1.0)  
&rarr; [*Journal article*](https://www.frontiersin.org/articles/10.3389/fnrgo.2023.994969)  


![Example of figure](https://gitlab.com/HanBnrd/benchnirs/-/raw/v1.0/example.png)


## Documentation
The documentation of the framework can be found here: https://hanbnrd.gitlab.io/benchnirs.


## Recommendation checklist
A checklist of recommendations towards good practice for machine learning with fNIRS (for brain-computer interface applications) can be found [here](./CHECKLIST.md). We welcome contributions from the community in order to improve it, please see below for more information on how to contribute.


## Minimum tested requirements
[**Python 3.8**](https://www.python.org/downloads/) with the following libraries:
- [matplotlib 3.3](https://matplotlib.org/stable/)
- [mne 0.23](https://mne.tools/stable/install/index.html)
- [nirsimple 0.1](https://github.com/HanBnrd/NIRSimple#installation)
- [numpy 1.19](https://numpy.org/install/)
- [pandas 1.0](https://pandas.pydata.org/docs/getting_started/index.html#installation)
- [scikit-learn 0.24](https://scikit-learn.org/stable/install.html)
- [scipy 1.8](https://scipy.org/install/)
- [seaborn 0.11](https://seaborn.pydata.org/installing.html)
- [statsmodels 0.12.2](https://www.statsmodels.org/dev/install.html)
- [torch 1.5](https://pytorch.org/get-started/locally/)


## Setup
Download and install [Python 3.8 or greater](https://www.python.org/downloads/). During the installation process, add Python to the path for more simplicity.

Download and unzip the [*BenchNIRS* repository](https://gitlab.com/HanBnrd/benchnirs/-/archive/main/benchnirs-main.zip).

In a terminal or command prompt, navigate to the directory containing the `requirements.txt` file and run:
```bash
python -m pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html
```

Download the datasets:
- *Herff et al. 2014*: you can download the dataset by making a request [here](http://www.csl.uni-bremen.de/CorpusData/download.php?crps=fNIRS). In the examples, the unzipped folder has been renamed to *dataset_herff_2014* for clarity.
- *Shin et al. 2018*: you can download the dataset [here](http://doc.ml.tu-berlin.de/simultaneous_EEG_NIRS/NIRS/NIRS_01-26_MATLAB.zip). In the examples, the unzipped folder has been renamed to *dataset_shin_2018* for clarity.
- *Shin et al. 2016*: you can download the dataset by filling the form [here](http://doc.ml.tu-berlin.de/hBCI). Then click on *NIRS_01-29* to download the fNIRS data. In the examples, the unzipped folder has been renamed to *dataset_shin_2016* for clarity.
- *Bak et al. 2019*: you can download the dataset [here](https://figshare.com/ndownloader/files/18069143). In the examples, the unzipped folder has been renamed to *dataset_bak_2019* for clarity.

> Alternatively, the *BenchNIRS* library containing the core functions (without main scripts) is available on [PyPI](https://pypi.org/project/benchnirs/) and can be installed using `pip`:
> ```bash
> pip install benchnirs
> ```
> and updated to the newest version with:
> ```bash
> pip install --upgrade benchnirs
> ```

## Running main scripts
- `generalised.py` compares the 6 models (LDA, SVC, kNN, ANN, CNN and LSTM) on the 5 datasets with a generalised approach (testing with unseen subjects)
- `dataset_size.py` reproduces `generalised.py` but with a range different dataset sizes (50% to 100% of dataset) to study the influence of this parameter on the classification accuracy
- `window_size.py` reproduces `generalised.py` but with only the 4 models using feature extraction (LDA, SVC, kNN and ANN) and with a range different window sizes (2 to 10 sec) to study the influence of this parameter on the classification accuracy
- `sliding_window.py` reproduces `generalised.py` but with only the 4 models using feature extraction (LDA, SVC, kNN and ANN) and with a 2 sec sliding window on the 10 sec epochs
- `personalised.py` compares the 6 models (LDA, SVC, kNN, ANN, CNN and LSTM) on the 5 datasets with a personalised approach (training and testing with each subject individually)
- `visualisation.py` enables to visualise the data from the datasets with various signal processing


## Example
An example script showing how to use the framework with a custom deep learning model can be found here: https://hanbnrd.gitlab.io/benchnirs/example.html.


## Simple use case
*BenchNIRS* enables to evaluate your model in Python with simplicity on an open access dataset supported:
```python
import benchnirs as bn

epochs = bn.load_dataset('shin_2018_nb')
data = bn.process_epochs(epochs['0-back', '2-back', '3-back'])
results = bn.deep_learn(*data, my_model)

print(results)
```


## Contributing to the repository
Contributions from the community to this repository are highly appreciated. We are mainly interested in contributions to:
- improving the recommendation checklist
- adding more fNIRS signal processing techniques
- adding support for new **open access datasets**
- tracking bugs

Contributions are encouraged under the form of [issues](https://gitlab.com/HanBnrd/benchnirs/-/issues) (for reporting bugs or requesting new features) and [merge requests](https://gitlab.com/HanBnrd/benchnirs/-/merge_requests) (for fixing bugs and implementing new features).
Please refer to [this tutorial](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html) for creating merge requests from a fork of the repository.


## Citing us
Please cite us if you are using this framework:
```
@article{benerradi2023benchmarking,
  title={Benchmarking framework for machine learning classification from fNIRS data},
  author={Benerradi, Johann and Clos, Jeremie and Landowska, Aleksandra and Valstar, Michel F and Wilson, Max L},
  journal={Frontiers in Neuroergonomics},
  volume={4},
  year={2023},
  publisher={Frontiers Media},
  url={https://www.frontiersin.org/articles/10.3389/fnrgo.2023.994969},
  doi={10.3389/fnrgo.2023.994969},
  issn={2673-6195}
}
```

If you are using the datasets of the framework, please also cite those related works.

Herff et al. 2014:
```
@article{herff2014mental,
	title={Mental workload during n-back task—quantified in the prefrontal cortex using fNIRS},
	author={Herff, Christian and Heger, Dominic and Fortmann, Ole and Hennrich, Johannes and Putze, Felix and Schultz, Tanja},
	journal={Frontiers in human neuroscience},
	volume={7},
	pages={935},
	year={2014},
	publisher={Frontiers}
}
```

Shin et al. 2018:
```
@article{shin2018simultaneous,
	title={Simultaneous acquisition of EEG and NIRS during cognitive tasks for an open access dataset},
	author={Shin, Jaeyoung and Von L{\"u}hmann, Alexander and Kim, Do-Won and Mehnert, Jan and Hwang, Han-Jeong and M{\"u}ller, Klaus-Robert},
	journal={Scientific data},
	volume={5},
	pages={180003},
	year={2018},
	publisher={Nature Publishing Group}
}
```

Shin et al. 2016:
```
@article{shin2016open,
	title={Open access dataset for EEG+NIRS single-trial classification},
	author={Shin, Jaeyoung and von L{\"u}hmann, Alexander and Blankertz, Benjamin and Kim, Do-Won and Jeong, Jichai and Hwang, Han-Jeong and M{\"u}ller, Klaus-Robert},
	journal={IEEE Transactions on Neural Systems and Rehabilitation Engineering},
	volume={25},
	number={10},
	pages={1735--1745},
	year={2016},
	publisher={IEEE}
}
```

Bak et al. 2019:
```
@article{bak2019open,
	title={Open-Access fNIRS Dataset for Classification of Unilateral Finger-and Foot-Tapping},
	author={Bak, SuJin and Park, Jinwoo and Shin, Jaeyoung and Jeong, Jichai},
	journal={Electronics},
	volume={8},
	number={12},
	pages={1486},
	year={2019},
	publisher={Multidisciplinary Digital Publishing Institute}
}
```
