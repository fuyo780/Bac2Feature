import configparser
import inspect
import os

import bac2feature

# get absolute path to bac2feature modules
app_path = os.path.dirname(inspect.getfile(bac2feature))
# read config.ini of bac2feature modules
config = configparser.ConfigParser()
config.read(app_path + '/../config.ini')
