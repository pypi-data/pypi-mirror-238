from pathlib import Path
import os
import shutil
from inspect import getsourcefile
from os.path import abspath

cust_conf = Path(os.getcwd(), "config.py")
default = os.path.dirname(abspath(getsourcefile(lambda:0)))
default = Path(default, "default.py")
shutil.copyfile(default,cust_conf)
