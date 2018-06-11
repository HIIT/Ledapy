# Ledapy

Ledapy is an port of Ledalab (www.ledalab.de) for Python. It is a simplified port and does not provide a GUI. However, it is suitable for headless processing, or integration with [MIDAS](http://github.com/bwrc/midas/).

## Prerequisites

Ledapy requires Python 3 and the following packages

- numpy
- scipy
- sympy

Optionally, if one wants to plot

- matplotlib

## Usage

There are some `.mat` files in the repository, provided so that Ledapy's results can be compared to Ledalab's (which can be done separately in Matlab).

A test run can be initated as follows

```
cd ..  # assuming we start in Ledapy's directory
python3
```

```
import ledapy
import scipy.io as sio
from numpy import array as npa
filename = 'ledapy/EDA1_long_100Hz.mat'
sampling_rate = 100
matdata = sio.loadmat(filename)
rawdata = npa(matdata['data']['conductance'][0][0][0], dtype='float64')
phasicdata = ledapy.runner.getResult(rawdata, 'phasicdata', sampling_rate, downsample=4, optimisation=2)
import matplotlib.pyplot as plt
plt.plot(phasicdata)
plt.show()
```

You should obtain something like this:

![Ledapy example](long_100_example.png)

note that optimisation is performed automatically. To compare results with Ledalab, remember to press the ‘optimise’ button