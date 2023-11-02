# pyCOCAP

<p align="center">
<img src="/docs/source/pics/COCAP_small.png" alt="COCAP Logo" width="500px"/>
</p>


**pyCOCAP** is the Python interface to the common COCAP database. You can find
the documentation [here](https://cocap.pages.hzdr.de/pycocap/)

## Installation


Using the Package Installer for Python PIP, you can install this interface with
following command

    
    pip install pycocap


## Usage

Once the package is installed it is as easy as this to get the COCAP data for
example the reported case numbers for Sweden and the stringency index for the
UK.

```python
import pycocap as pyc
cases = pyc.cases('Sweden')
npi = pyc.npi('United Kingdom', 'stringency')
```

If you want to get multiple NPIs into one DataFrame, you can do following

```python
npis = pyc.npis('Germany', ['school closing', 'dept relief', 'facial coverings'])
```

Defining the start and end dates of the timeseries can be done with Python's
standard `date` objects

```python
from datetime import date
deaths = pyc.death('Canada', start_date=date(2020, 5, 16), end_date=date(2021, 1, 15))
```

You can also use this to expand the timeseries and at the same time choose
with which value to fill gaps

```python
deaths = pyc.death('Canada', start_date=date(2019, 11, 1), fill_value=0)
```


## Documentation

You can find the documentation [here](https://cocap.pages.hzdr.de/pycocap/)

## Requirements

- [pandas >= 1.4.0](https://pandas.pydata.org/)
- [requests >= 2.27.1](https://requests.readthedocs.io/en/latest/)


## Contact

You can get in touch with me via [e-mail](mailto:lennart.schueler@ufz.de) or have a
look at the [source code](https://gitlab.hzdr.de/cocap/pycocap) and open
issues there.
