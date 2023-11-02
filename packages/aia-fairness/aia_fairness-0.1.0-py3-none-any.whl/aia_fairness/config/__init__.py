from pathlib import Path
import os
import shutil
from inspect import getsourcefile
from os.path import abspath

cust_conf = Path(os.getcwd(), "config.py")
if os.path.exists(cust_conf):
    lib = os.path.dirname(abspath(getsourcefile(lambda:0)))


    shutil.copyfile(cust_conf,Path(lib,"tmp_conf.py"))
    from .tmp_conf import *

else:
    from .default import *
