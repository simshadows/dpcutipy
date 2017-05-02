"""
dpcutipy.py
Author: simshadows

dpcutipy is a glue code module for dpcutil

Design documentation used to build this module:
https://reference.digilentinc.com/_media/dpcutil_programmers_reference_manual.pdf
http://hamsterworks.co.nz/mediawiki/index.php/Module_18
"""

import os
import sys
import traceback
import collections
import atexit
from ctypes import *

from .errors import DpcUtiPyException

BUFFER_SIZE = 512
# Placeholder value for mutable ctypes buffers.
# TODO: Please secure for buffer overflow issues.

###############################################################################
# MODULE INITIALIZATION #######################################################
###############################################################################

_dpcutil = None
_cwd = os.path.dirname(__file__)

# Attempt to load dpcutil
_dpcutil = cdll.dpcutil
# try: # TODO: Make something more robust.
#     _dpcutil = cdll.dpcutil
# except Exception as e:
#     # Alternative Imports.
#     pass 
#     # try:
#     #     _dpcutil = CDLL(os.path.join(_cwd, "dpcutil_sys32.dll"))
#     # except Exception as e0:
#     #     try:
#     #         _dpcutil = CDLL(os.path.join(_cwd, "dpcutil_syswow64.dll"))
#     #     except Exception as e1:
#     #         _dpcutil = None
if _dpcutil is None:
    raise DpcUtiPyException("Failed to import dpcutil.")

def _DpcInit():
    erc = c_int(0)
    if not _dpcutil.DpcInit(byref(erc)):
        raise DpcUtiPyException(erc)
    return

def _DpcTerm():
    _dpcutil.DpcTerm()
    return

_DpcInit()
atexit.register(_DpcTerm)

###############################################################################
# MODULE BASIC INTERFACE ######################################################
###############################################################################
# For function behaviour, see DPCUTIL Programmers Reference Manual.

# PARAMETERS:
#   hwnd (Optional)
#       Handle to parent window. No type-checking is done, but this should be
#       a relevant ctypes type, likely `c_void_p`.
def DvmgStartConfigureDevices(hwnd=None):
    erc = c_int(0)
    _dpcutil.DvmgStartConfigureDevices(hwnd, byref(erc))
    if erc.value != DpcUtiPyException.ERCNOERROR:
        raise DpcUtiPyException(erc)
    return

# RETURNS:
#   The index of the default device, as an integer.
def DvmgGetDefaultDev():
    erc = c_int(0)
    device_id = _dpcutil.DvmgGetDefaultDev(byref(erc))
    if device_id == -1:
        raise DpcUtiPyException("No devices in the device table.", erc)
    assert isinstance(device_id, int)
    return device_id

# RETURNS:
#   Name of the queried device.
def DvmgGetDevName(device_id):
    erc = c_int(0)
    cbuf = create_string_buffer(BUFFER_SIZE)
    if not _dpcutil.DvmgGetDevName(device_id, cbuf, byref(erc)):
        raise DpcUtiPyException(erc)
    ret = cbuf.value.decode("ascii")
    assert isinstance(ret, str)
    return ret

# RETURNS:
#   A class that represents the data transfer HANDLE object from the DLL API.
#   This class contains methods that mimic the operations available to be
#   performed on this HANDLE.
def DpcOpenData(dev_name):
    return EPPDataTransferHandle(dev_name)

class EPPDataTransferHandle:
    def __init__(self, dev_name):
        self._chif = c_void_p(0) # ctypes pointer to a HANDLE.
        erc = c_int(0)
        buf = dev_name.encode() # str to bytes
        if not _dpcutil.DpcOpenData(byref(self._chif), buf, byref(erc), None):
            raise DpcUtiPyException(erc)
        return

    def DpcCloseData(self):
        erc = c_int(0)
        if not _dpcutil.DpcCloseData(self._chif, byref(erc)):
            raise DpcUtiPyException(erc)
        return

    def DpcPutReg(self, b_addr, b_data):
        assert isinstance(b_addr, int) and (0x00 <= b_addr <= 0xFF)
        assert isinstance(b_data, int) and (0x00 <= b_data <= 0xFF)
        b_addr = c_byte(b_addr)
        b_data = c_byte(b_data)
        erc = c_int(0)
        if not _dpcutil.DpcPutReg(self._chif, b_addr, b_data, byref(erc), None):
            raise DpcUtiPyException(erc)
        return

    def DpcGetReg(self, b_addr):
        assert isinstance(b_addr, int) and (0x00 <= b_addr <= 0xFF)
        b_addr = c_byte(b_addr)
        b_data = c_byte(0)
        erc = c_int(0)
        if not _dpcutil.DpcGetReg(self._chif, b_addr, byref(b_data), byref(erc), None):
            raise DpcUtiPyException(erc)
        b_data = b_data.value
        b_data = (b_data + 0x100) % 0x100
        assert isinstance(b_data, int) and (0x00 <= b_data <= 0xFF)
        return b_data

    def DpcPutRegSet(*args, **kwargs):
        raise NotImplementedError

    def DpcGetRegSet(*args, **kwargs):
        raise NotImplementedError

    def DpcPutRegRepeat(*args, **kwargs):
        raise NotImplementedError

    def DpcGetRegRepeat(*args, **kwargs):
        raise NotImplementedError

    # RETURNS:
    #   Nothing.
    # EXCEPTIONS:
    #   If DPCUTIL's DpcGetFirstError returns an error code, this method will
    #   raise the error code as an exception.
    # TODO:
    #   Reimplement error codes as enum, and make this method return the error
    #   as an enum. This may require refactoring.
    def DpcGetFirstError(self):
        ret = _dpcutil.DpcGetFirstError(self._chif)
        if ret != DpcUtiPyException.ERCNOERROR:
            raise DpcUtiPyException(ret)
        return

###############################################################################
# MODULE EXTENDED INTERFACE ###################################################
###############################################################################

def put_single_register(b_addr, b_data, dev_name):
    handle = DpcOpenData(dev_name)
    try:
        handle.DpcPutReg(b_addr, b_data)
        handle.DpcGetFirstError()
    finally:
        handle.DpcCloseData()
    return

def get_single_register(b_addr, dev_name):
    handle = DpcOpenData(dev_name)
    data = None
    try:
        data = handle.DpcGetReg(b_addr)
        handle.DpcGetFirstError()
    finally:
        handle.DpcCloseData()
    return data
