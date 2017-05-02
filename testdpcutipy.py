"""
testdpcutipy.py
Author: simshadows

A very simple test file that just writes some data in, then reads and prints it back.

This also provides a simple demonstration of the operation of the dpcutipy library.
"""

import os
import sys
import random
import traceback

from dpcutipy import dpcutipy

dpcutipy.DvmgStartConfigureDevices() # Comment back in if needed.
dev_id = dpcutipy.DvmgGetDefaultDev()
dev_name = dpcutipy.DvmgGetDevName(dev_id)

print("Default device: " + dev_name)

# Test code

# writes = [
# 	(0, 21),
# 	(1, 42),
# 	(2, 37),
# 	(3, 44),
# 	(4, 58),
# 	(10, 194),
# ]

writes = [(64, random.randint(0,255))]

for (reg, val) in writes:
	dpcutipy.put_single_register(reg, val, dev_name)
	print("REGISTER {} WRITE: {}".format(str(reg), str(val)))

for (reg, val) in [(x,0) for x in range(0x100)]: # writes:
	ret = dpcutipy.get_single_register(reg, dev_name)
	print("REGISTER {} READ: {}".format(str(reg), str(ret)))

print("DONE!")
