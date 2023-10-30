import ctypes

RTLSDR = 0

(BAND_III, L_BAND) = (64, 65)

BAND_III_CHANNELS = ["5A","5B","5C","5D","6A","6B","6C","6D","7A","7B","7C","7D","8A","8B","8C","8D","9A","9B","9C","9D","10A","10B","10C","10D","11A","11B","11C","11D","12A","12B","12C","12D","13A","13B","13C","13D","13E","13F"]
L_BAND_CHANNELS = ["LA","LB","LC","LD","LE","LF","LG","LH","LI","LJ","LK","LL","LM","LN","LO","LP"]

(OK,INIT_ALREADY_DONE,UNKNOWN_DEVICE_TYPE,DEVICE_INIT_ERROR,INIT_DAB_ERROR,STATION_NOT_USABLE,DEVICE_NOT_INIT) = (0,1,2,3,4,5,6)

class audiodata(ctypes.Structure):
    _fields_ = [
        ("defined", ctypes.c_bool),
        ("subchId", ctypes.c_int16),
        ("startAddr", ctypes.c_int16),
        ("shortForm", ctypes.c_bool),
        ("protLevel", ctypes.c_int16),
        ("length", ctypes.c_int16),
        ("bitRate", ctypes.c_int16),
        ("ASCTy", ctypes.c_int16),
        ("language", ctypes.c_int16),
        ("programType", ctypes.c_int16),
        ("is_madePublic", ctypes.c_bool),
    ]

syncsignal_t = ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_void_p)
systemdata_t = ctypes.CFUNCTYPE(None, ctypes.c_bool, ctypes.c_int16, ctypes.c_int, ctypes.c_void_p)
ensemblename_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int32, ctypes.c_void_p)
programname_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int32, ctypes.c_void_p)
fib_quality_t = ctypes.CFUNCTYPE(None, ctypes.c_short, ctypes.c_void_p)
audioOut_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_int16), ctypes.c_int, ctypes.c_int, ctypes.c_bool, ctypes.c_void_p)
dataOut_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_void_p)
bytesOut_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_uint8), ctypes.c_int16, ctypes.c_uint8, ctypes.c_void_p)
programdata_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(audiodata), ctypes.c_void_p)
programQuality_t = ctypes.CFUNCTYPE(None, ctypes.c_int16, ctypes.c_int16, ctypes.c_int16, ctypes.c_void_p)
motdata_t = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_uint8), ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p)
tii_data_t = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
theTime_t = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_void_p)

class Callbacks(ctypes.Structure):
    _fields_ = [
        ("dabMode", ctypes.c_uint8),
        ("syncsignal_Handler", syncsignal_t),
        ("systemdata_Handler", systemdata_t),
        ("ensemblename_Handler", ensemblename_t),
        ("programname_Handler", programname_t),
        ("fib_quality_Handler", fib_quality_t),
        ("audioOut_Handler", audioOut_t),
        ("dataOut_Handler", dataOut_t),
        ("bytesOut_Handler", bytesOut_t),
        ("programdata_Handler", programdata_t),
        ("program_quality_Handler", programQuality_t),
        ("motdata_Handler", motdata_t),
        ("tii_data_Handler", tii_data_t),
        ("timeHandler", theTime_t),
    ]

class LibNotFound(Exception):
    "Raised when libsimple_dab.so is not found"
    pass

class InitAlreadyDone(Exception):
    "Raised when the init is already done"
    pass

class UnknownDeviceType(Exception):
    "Raised when the device type is unknown"
    pass

class DeviceInitError(Exception):
    "Raised when the device couldn't be initalized"
    pass

class InitDabError(Exception):
    "Raised when the initalization of dab-cmdline raised an error"
    pass

class StationUnusable(Exception):
    "Raised when the station is unusable"
    pass

class SimpleDAB:
    def __init__(self):
        self.ExceptionMap = {INIT_ALREADY_DONE : (InitAlreadyDone,"The library was already initalized"), UNKNOWN_DEVICE_TYPE : (UnknownDeviceType,"The device selected is unknown"), DEVICE_INIT_ERROR: (DeviceInitError,"The device is not present or is still used. Please try unplugging the device and then plugging it back in."), INIT_DAB_ERROR: (InitDabError,"An error occured while initalizing simple_dab"), STATION_NOT_USABLE: (StationUnusable,"The station selected is unusable")}

        try:
            if os.path.isfile("/usr/local/lib/libsimple_dab.so"):
                self.lib = ctypes.cdll.LoadLibrary("/usr/local/lib/libsimple_dab.so")
            else:
                self.lib = ctypes.cdll.LoadLibrary("libsimple_dab.so")
        except OSError:
            raise LibNotFound("Do you have simple_dab build and installed? If not follow : https://gitlab.com/1337Misom/simple_dab_lib else create an issue.")

        self.dummy_syncsignal_callback = syncsignal_t(self.lib.SDAB_DummySyncFunc)
        self.dummy_system_callback = systemdata_t(self.lib.SDAB_DummySystemFunc)
        self.dummy_ensemble_callback = ensemblename_t(self.lib.SDAB_DummyEnsembleFunc)
        self.dummy_fib_callback = fib_quality_t(self.lib.SDAB_DummyFibFunc)
        self.dummy_data_callback = dataOut_t(self.lib.SDAB_DummyDataFunc)
        self.dummy_bytes_callback = bytesOut_t(self.lib.SDAB_DummyBytesFunc)
        self.dummy_program_qual_callback = programQuality_t(self.lib.SDAB_DummyProgQualFunc)
        self.dummy_program_data_callback = programdata_t(self.lib.SDAB_DummyProgdataFunc)
        self.dummy_motdata_callback = motdata_t(self.lib.SDAB_DummyMotdataFunc)
        self.dummy_tii_callback = tii_data_t(self.lib.SDAB_DummyTiidataFunc)
        self.dummy_time_callback = theTime_t(self.lib.SDAB_DummyTimeFunc)

        self._set_function_types()

    def _call_func(self,func,*args):
        result = func(*args)
        if result != OK:
            raise self.ExceptionMap[result][0](self.ExceptionMap[result][1])
        return OK

    def _set_function_types(self):
        self.lib.SDAB_Init.argtypes = [ctypes.c_uint8, ctypes.POINTER(Callbacks), ctypes.c_int16]
        self.lib.SDAB_Init.restype = ctypes.c_int

        self.lib.SDAB_Start.argtypes = [ctypes.c_uint8, ctypes.c_char_p]
        self.lib.SDAB_Start.restype = ctypes.c_int

        self.lib.SDAB_Exit.argtypes = []
        self.lib.SDAB_Exit.restype = ctypes.c_int

        self.lib.SDAB_SwitchFrequency.argtypes = [ctypes.c_int8, ctypes.c_char_p]
        self.lib.SDAB_SwitchFrequency.restype = ctypes.c_int

        self.lib.SDAB_SwitchStationName.argtypes = [ctypes.c_char_p]
        self.lib.SDAB_SwitchStationName.restype = ctypes.c_int

        self.lib.SDAB_SetGain.argtypes = [ctypes.c_int16]
        self.lib.SDAB_SetGain.restype = ctypes.c_int

        self.lib.SDAB_SetAutoGain.argtypes = [ctypes.c_bool]
        self.lib.SDAB_SetAutoGain.restype = ctypes.c_int

        self.lib.SDAB_IsAudio.argtypes = [ctypes.c_char_p]
        self.lib.SDAB_IsAudio.restype = ctypes.c_bool

    def _check_frequency(self,band,channel):
        if type(channel) == bytes:
            channel_to_check = channel.decode("ascii")
        elif type(channel) == str:
            channel_to_check = channel
        else:
            raise TypeError("Channel not bytes or str")

        if band == BAND_III:
            band_channels = BAND_III_CHANNELS
        elif band == L_BAND:
            band_channels = L_BAND_CHANNELS
        else:
            raise ValueError("Band isn't BAND_III or L_BAND")

        if channel_to_check not in band_channels:
            raise ValueError("Channel doesn't exist in band")

        return (band,channel_to_check.encode("ascii"))

    def begin(self,device_type, callbacks, ppmCorrection=0):
        self._call_func(self.lib.SDAB_Init,device_type, callbacks, ppmCorrection)

    def start(self, band, channel):
        self._call_func(self.lib.SDAB_Start,*self._check_frequency(band,channel))

    def switch_station(self,name: bytes):
        name_bytes = name
        if type(name) == str:
            name_bytes = name.encode("utf-8")
        elif type(name) != bytes:
            raise TypeError("Name is not bytes or str")
        self._call_func(self.lib.SDAB_SwitchStationName,name_bytes)

    def switch_frequency(self,band,channel):
        self._call_func(self.lib.SDAB_SwitchFrequency,*self._check_frequency(band,channel))

    def set_gain(self,gain):
        self._call_func(self.lib.SDAB_SetGain,gain)

    def set_autogain(self,autogain):
        self._call_func(self.lib.SDAB_SetAutoGain,autogain)

    def is_audio(self,name):
        return self.lib.SDAB_IsAudio(name)

    def exit(self):
        self._call_func(self.lib.SDAB_Exit)
