import os
import glob
import xarray as xr
import numpy as np
import pandas as pd
from tqdm import tqdm
import datetime
import cftime
import matplotlib.pyplot as plt
from matplotlib import gridspec

class FVField:
    pass

class SEField:
    def __init__(self, da, grid_path):
        self.grid_path = grid_path
        self.da = da