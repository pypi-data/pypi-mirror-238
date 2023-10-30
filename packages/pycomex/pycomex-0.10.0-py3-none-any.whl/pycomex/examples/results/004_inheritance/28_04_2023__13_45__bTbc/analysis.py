#! /usr/bin/env python3
"""
This python module was automatically generated.

This module can be used to perform analyses on the results of an experiment which are saved in this archive
folder, without actually executing the experiment again. All the code that was decorated with the
"analysis" decorator was copied into this file and can subsequently be changed as well.
"""
import os
import json
import pathlib
from pprint import pprint
from typing import Dict, Any

# Useful imports for conducting analysis
import numpy as np
import matplotlib.pyplot as plt
from pycomex.functional.experiment import Experiment

# Importing the experiment
from code import *

PATH = pathlib.Path(__file__).parent.absolute()
CODE_PATH = os.path.join(PATH, 'code.py')
experiment = Experiment.load(CODE_PATH)
experiment.analyses = []


# == /media/ssd/Programming/pycomex/pycomex/examples/003_analysing.analysis ==
@experiment.analysis
def analysis(e):
    # (1) Note how the experiment path will be dynamically determined to be a *new*
    #     folder when actually executing the experiment, but it will refer to the
    #     already existing experiment record folder when imported from
    #     "snapshot.py"
    print(e.path)

    e.log('Starting analysis of experiment results')
    index_min, count_min = min(e['metrics/length'].items(),
                               key=lambda item: item[1])
    index_max, count_max = max(e['metrics/length'].items(),
                               key=lambda item: item[1])
    count_mean = sum(e['metrics/length'].values()) / len(e['metrics/length'])

    analysis_results = {
        'index_min': index_min,
        'count_min': count_min,
        'index_max': index_max,
        'count_max': count_max,
        'count_mean': count_mean
    }
    # (2) Committing new files to the already existing experiment record folder will
    #     also work as usual, whether executed here directly or later in "analysis.py"
    e.commit_json('analysis_results.json', analysis_results)
    e.log(f'saved analysis results')


# == __main__.analysis ==
@experiment.analysis
def analysis(e):
    # We can also add additional analysis in the sub experiments!
    e.log('hello from sub experiment analysis!')


experiment.execute_analyses()