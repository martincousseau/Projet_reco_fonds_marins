from __future__ import print_function, division
import os
import ntpath
import numpy as np
from PIL import Image
from os.path import join, exists
# local libs
from models.suim_net import SUIM_Net
from utils.data_utils import getPaths