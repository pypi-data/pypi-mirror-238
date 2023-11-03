"""
BenchNIRS
=========
Benchmarking framework for machine learning with fNIRS
"""

from .load import load_dataset
from .viz import epochs_viz
from .process import process_epochs
from .learn import machine_learn, deep_learn
