"""
testdpcutipy.py
Author: simshadows

A very simple test file that just writes to a register, then reads and prints it back.

This also provides a simple demonstration of the operation of the dpcutipy library.
"""

import os
import sys
import random
import traceback

from dpcutipy import dpcutipy

reg_id = random.randint(0,64)
reg_val = random.randint(0,256)

dpcutipy.DvmgStartConfigureDevices() # Comment back in if needed.
dev_id = dpcutipy.DvmgGetDefaultDev()
dev_name = dpcutipy.DvmgGetDevName(dev_id)

print("Default device: " + dev_name)

dpcutipy.put_single_register(reg_id, reg_val, dev_name)
print("REGISTER {} WRITE: {}".format(str(reg_id), str(reg_val)))

ret = dpcutipy.get_single_register(reg_id, dev_name)
print("REGISTER {} READ: {}".format(str(reg_id), str(ret)))

print("DONE!")
