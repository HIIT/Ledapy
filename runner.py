#!/usr/bin/env python3
"""
Main ledapy module for interfacing with callers.

example usage (single process):
import ledapy
import scipy.io as sio
from numpy import array as npa
filename = 'EDA1_long_100Hz.mat'
sampling_rate = 100
matdata = sio.loadmat(filename)
rawdata = npa(matdata['data']['conductance'][0][0][0], dtype='float64')
phasicdata = ledapy.runner.getResult(rawdata, 'phasicdata', sampling_rate, downsample=4, optimisation=2)

also contains multiprocess interface pipes to be used as a separate process
"""
from __future__ import division
import numpy as np
from numpy import array as npa
from . import leda2
from . import utils
from . import analyse
from . import deconvolution


def getResult(raw_vector, result_type, sampling_rate, downsample=1, optimisation=0, pipeout=None):
    """
    Run main analysis: extract phasic driver (returned) and set all leda2 values

    parameters:
    raw_vector : raw data
    result_type : what we want returned. Either 'phasicdriver' or 'phasicdata'
    sampling_rate : input samping rate
    downsample : downsampling factor to reduce computing time (1 == no downsample)
    optimisation : level of optimization
    pipeout : if set, sends driver through pipe instead of returning it
    """
    leda2.reset()
    leda2.current.do_optimize = optimisation
    import_data(raw_vector, sampling_rate, downsample)
    deconvolution.sdeco(optimisation)
    if result_type.lower() == 'phasicdata':
        result = leda2.analysis.phasicData
    elif result_type.lower() == 'phasicdriver':
        result = leda2.analysis.driver
    else:
        raise ValueError('result_type not recognised (was ' + result_type + ')')
    if pipeout is not None:
        pipeout.send(result)
        pipeout.close()
    else:
        return result


def import_data(raw_data, srate, downsample=1):
    """
    Sets leda2 object to its appropriate values to allow analysis
    Adapted from main/import/import_data.m
    """
    if not isinstance(raw_data, np.ndarray):
        raw_data = npa(raw_data, dtype='float64')
    time_data = utils.genTimeVector(raw_data, srate)
    conductance_data = npa(raw_data, dtype='float64')
    if downsample > 1:
        (time_data, conductance_data) = utils.downsamp(time_data, conductance_data, downsample, 'mean')
    leda2.data.samplingrate = srate / downsample
    leda2.data.time_data = time_data
    leda2.data.conductance_data = conductance_data
    leda2.data.conductance_error = np.sqrt(np.mean(pow(np.diff(conductance_data), 2)) / 2)
    leda2.data.N = len(conductance_data)
    leda2.data.conductance_min = np.min(conductance_data)
    leda2.data.conductance_max = np.max(conductance_data)
    (leda2.data.conductance_smoothData, leda2.data.conductance_smoothData_win) = utils.smooth_adapt(conductance_data, srate, .00001)
    analyse.trough2peak_analysis()


def calculateMinMax(driver, sample_rate, iscr_win, minmax_win, pipeout):
    """
    Compute minimum and maximum ISCR values for normalisation.
    Intented to be used as a separate process to allow caller to process raw data.

    parameters:
    driver : scr phasic driver
    sample_rate : post-analysis sampling rate
    iscr_win : window (s) for iscr calculation
    minmax_win : window size (s) for minmax calculation (set to 0 to cover whole driver)
    pipeout : sends min and max through this pipe
    pipes out a tuple (iscr_min, iscr_max)
    """
    iscr_min = float('inf')
    iscr_max = float('-inf')
    if minmax_win == 0:
        startpoint = -len(driver)
    else:
        startpoint = int(-minmax_win * sample_rate)
    endpoint = startpoint + iscr_win * sample_rate
    while endpoint <= 0:
        iscr = driver[startpoint:endpoint].sum()
        if iscr > iscr_max:
            iscr_max = iscr
        if iscr < iscr_min:
            iscr_min = iscr
        startpoint += 1
        endpoint += 1
    pipeout.send((iscr_min, iscr_max))
    pipeout.close()
