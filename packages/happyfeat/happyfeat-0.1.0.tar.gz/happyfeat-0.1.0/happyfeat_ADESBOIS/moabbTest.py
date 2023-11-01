import sys
import warnings
import matplotlib.pyplot as plt
import pandas as pd
from mne.decoding import CSP
import numpy as np

import moabb
from moabb.datasets import PhysionetMI
from moabb.evaluations import WithinSessionEvaluation
from moabb.paradigms import LeftRightImagery
from moabb.datasets.utils import find_intersecting_channels

if __name__ == '__main__':
    moabb.set_log_level("info")

    dataset = PhysionetMI()
    dataset.subject_list = [1]
    sessions = dataset.get_data(subjects=[1])
    paradigm = LeftRightImagery()
    X, labels, meta = paradigm.get_data(dataset=dataset, subjects=[1], return_epochs=True)
    [electrodes] = find_intersecting_channels([dataset])
    a = 0


