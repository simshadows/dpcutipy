# dpcutipy
Python bindings for dpcutil

Please note that it's super-minimal at the moment. This shouldn't be used for production code unmodified.

# How To Use

Import `dpcutipy.py`. Initialization and termination of dpcutil is automatically handled.

To configure the device table, call `DvmgStartConfigureDevices()`. This will block and open a window for the user.

Once there's at least one device in the device table, you can connect to the default device using:

```Python
handle = DpcOpenData(DvmgGetDevName(DvmgGetDefaultDev()))
```

Handle is an `EPPDataTransferHandle` instance (see `dpcutipy.py`). The instance methods should correspond to the functions described in [the dpcutil reference manual](https://reference.digilentinc.com/_media/dpcutil_programmers_reference_manual.pdf).

Close the connection with `handle.DpcCloseData()`.

# Example Code

See `testdpcutipy.py`.
