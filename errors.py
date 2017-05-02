"""
errors.py
Author: simshadows

Defines errors for dpcutipy.
"""

from ctypes import c_int

# Error codes from dpcdefs.h revision 07/22/2004
_errors_src = """
const ERC ercNoError        = 0;
const ERC ercConnReject     = 3001;
const ERC ercConnType       = 3002;
const ERC ercConnNoMode     = 3003;
const ERC ercInvParam       = 3004;
const ERC ercInvCmd         = 3005;
const ERC ercUnknown        = 3006;
const ERC ercJtagConflict   = 3007;
const ERC ercNotImp         = 3008;
const ERC ercNoMem          = 3009;
const ERC ercTimeout        = 3010;
const ERC ercConflict       = 3011;
const ERC ercBadPacket      = 3012;
const ERC ercInvOption      = 3013;
const ERC ercAlreadyCon     = 3014;
const ERC ercConnected      = 3101;
const ERC ercNotInit        = 3102;
const ERC ercCantConnect    = 3103;
const ERC ercAlreadyConnect = 3104;
const ERC ercSendError      = 3105;
const ERC ercRcvError       = 3106;
const ERC ercAbort          = 3107;
const ERC ercTimeOut        = 3108;
const ERC ercOutOfOrder     = 3109;
const ERC ercExtraData      = 3110;
const ERC ercMissingData    = 3111;
const ERC ercTridNotFound   = 3201;
const ERC ercNotComplete    = 3202;
const ERC ercNotConnected   = 3203;
const ERC ercWrongMode      = 3204;
const ERC ercWrongVersion   = 3205;
const ERC ercDvctableDne    = 3301;
const ERC ercDvctableCorrupt= 3302;
const ERC ercDvcDne         = 3303;
const ERC ercDpcutilInitFail= 3304;
const ERC ercUnknownErr     = 3305;
const ERC ercDvcTableOpen   = 3306;
const ERC ercRegError       = 3307;
const ERC ercNotifyRegFull  = 3308;
const ERC ercNotifyNotFound = 3309;
const ERC ercOldDriverNewFw = 3310;
const ERC ercInvHandle      = 3311;
const ERC ercInterfaceNotSupported = 3312;
"""

# Error documentation from DPCUTIL Programmer’s Manual revision 06/03/05
# https://reference.digilentinc.com/_media/dpcutil_programmers_reference_manual.pdf
_errors_doc = """
ercNoError 0 No error occurred in transaction
ercInvParam 3004 Invalid parameter sent in API call
ercInvCmd 3005 Internal error. Please report occurrence as a bug
ercUnknown 3006 Internal error. Please report occurrence as a bug
ercNoMem 3009 Not enough memory to carry out transaction
ercNotInit 3102 Communication device not initialized
ercCantConnect 3103 Can’t connect to communication module
ercAlreadyConnect 3104 Already connected to communication device
ercSendError 3105 Error occurred while sending data to communication device
ercRcvError 3106 Error occurred while receiving data from communication device
ercAbort 3107 Error occurred while trying to abort transaction(s)
ercOutOfOrder 3109 Completion out of order
ercExtraData 3110 Too much data received from communication device
ercMissingData 3111 Nothing to send or data/address mismatched pairs
ercTridNotFound 3201 Unable to find matching TRID in transaction queue
ercNotComplete 3202 Transaction being cleared is not complete
ercNotConnected 3203 Not connected to communication device
ercWrongMode 3204 Connected in wrong mode (JTAG or data transfer)
ercWrongVersion 3205 Internal error. Please report occurrence as a bug
ercDvctableDne 3301 Device table doesn’t exist (an empty one has been created)
ercDvctableCorrupt 3302 All or part of the device table is corrupted
ercDvcDne 3303 Device does not exist in device table
ercDpcutilInitFail 3304 DpcInit API call failed
ercDvcTableOpen 3306 Communications devices dialog box already open.
ercRegError 3307 Error occurred while accessing the registry
"""

# This is the user exception.
class DpcUtiPyException(Exception):

    ERCNOERROR = 0
    
    _errors = {}
    # _errors[error_code] = error name string

    _error_descriptions = {}
    # _error_descriptions[error_code] = error description string

    # Parse the error code source and documentation
    for line in _errors_src.strip().splitlines():
        substrings = line.rsplit(maxsplit=1)
        # E.g.     "const ERC ercNoError        = 0;"
        # Becomes  ["const ERC ercNoError        =", "0;"]
        assert substrings[0][-1] == "="
        assert substrings[1][-1] == ";"
        assert len(substrings) == 2
        error_code = int(substrings[1][:-1])
        substrings = substrings[0][:-1].rsplit(maxsplit=1)
        # E.g.     ["const ERC ercNoError        =", "0;"]
        # Becomes  ["const ERC", "ercNoError"]
        assert substrings[0] == "const ERC"
        assert len(substrings) == 2
        error_name = substrings[1]
        _errors[error_code] = error_name
    for line in _errors_doc.strip().splitlines():
        substrings = line.split(maxsplit=2)
        # E.g.     "ercNoError 0 No error occurred in transaction"
        # Becomes  ["ercNoError", "0", "No error occurred in transaction"]
        error_code = int(substrings[1])
        assert substrings[0].lower() == _errors[error_code].lower()
        assert len(substrings) == 3
        _error_descriptions[error_code] = substrings[2]

    # TODO: Clean up this spaghettified mess.
    #
    # ARGUMENTS:
    #   DpcUtiPyException()
    #       Constructions an exception with no args.
    #   DpcUtiPyException(msg:str)
    #       Constructs an exception with the message `msg` describing the error
    #       context.
    #   DpcUtiPyException(erc:int)
    #   DpcUtiPyException(erc:c_int)
    #       Constructs an exception with the DPCUTIL error code being used to
    #       describe the error, as defined in dpcdefs.h.
    #   DpcUtiPyException(msg:str, erc:int)
    #   DpcUtiPyException(msg:str, erc:c_int)
    #   DpcUtiPyException(erc:int, msg:str)
    #   DpcUtiPyException(erc:c_int, msg:str)
    #       Constructs an exception with a combination of both a context
    #       message and a DPCUTIL error code.
    # PRECONDITIONS:
    #   - If `msg` is supplied, then it is a non-empty string (after whitespace
    #     stripping).
    #   - Behaviour is undefined for argument combinations other than those
    #     documented above. This is assert-checked.
    def __init__(self, *args):
        assert len(args) < 3
        # These will remain None if unused.
        self.error_cntxt = None # Error context
        self.erc = None         # Error code from dpcdefs.h
        self.error_name = None  # Error name from dpcdefs.h
        self.error_desc = None  # Error description from documentation
        buf = ""
        buf_msg = None
        buf_erc = None
        # Read Arguments
        if len(args) == 0:
            buf_msg = "Unknown error (no error code or context string given)."
        else:
            for arg in args:
                if isinstance(arg, int):
                    assert self.erc is None
                    self.erc = arg
                elif isinstance(arg, c_int):
                    assert self.erc is None
                    self.erc = arg.value
                else: # Assumed to be a string
                    assert isinstance(arg, str) and (len(arg.strip()) > 0)
                    assert self.error_cntxt is None
                    buf_msg = self.error_cntxt = arg.strip()
        if not self.erc is None:
            template = "DPCUTIL error {name} ({erc}){desc}"
            erc = self.erc # Easier reference
            name = None
            desc = None
            if erc in self._errors:
                name = self.error_name = self._errors[erc]
            else:
                name = "UNKNOWN_DPCUTIL_ERROR"
            if erc in self._error_descriptions:
                self.error_desc = self._error_descriptions[erc]
                desc = " " + self.error_desc
            else:
                desc = ""
            buf_erc = template.format(name=name, erc=str(erc), desc=desc)
        assert (buf_msg is None) or isinstance(buf_msg, str)
        assert (buf_erc is None) or isinstance(buf_erc, str)
        assert not buf_msg is buf_erc is None
        if not buf_msg is None:
            buf = buf_msg
        if (not buf_erc is None) and (self.erc != self.ERCNOERROR):
            if len(buf) > 0:
                if not buf.endswith("."):
                    buf += "."
                buf += " "
            buf += buf_erc
        return super(DpcUtiPyException, self).__init__(buf)
