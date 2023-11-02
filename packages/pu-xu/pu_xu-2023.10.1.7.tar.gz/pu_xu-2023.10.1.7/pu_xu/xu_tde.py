import os.path
from ctypes import *


dllname="xu_tde.dll"
dllpath= os.path.dirname(os.path.abspath(__file__))+os.path.sep+dllname

mydll = cdll.LoadLibrary(dllpath)

# Define the Result struct
# Define the Result struct
class Result(Structure):
    _fields_ = [("length", c_int),
                ("data", c_uint32),
                ("str", c_char * 50)
                ]


def EepromRead(pid,address):
    x = int(pid, 16)
    y=int(address, 16)
    #print (x)
    a=mydll.readeeprom(x,y )
    if a<0:
        return -1,"fail to read"
    return 0,hex(a)


def EepromWrite(pid,address,val):
    x = int(pid, 16)
    y=int(address, 16)
    z=int(val, 16)
    #print (z)
    a=mydll.writeeeprom(x,y,z )
    if a<0:
        #print(a)
        return -1,"fail to write"
    #print(a)
    return 0,"Done:"+hex(a)



def TestXuRead(pid,address):
    """
    XU_UNDEFINED_CONTROL	0x00
    XU_TEST_REGISTER_ADDRESS_CONTROL	0x01
    XU_TEST_REGISTER_ACCESS_CONTROL	0x02
    XU_TEST_EEPROM_ADDRESS_CONTROL	0x03
    XU_TEST_EEPROM_ACCESS_CONTROL	0x04
    XU_TEST_SENSOR_ADDRESS_CONTROL	0x05
    XU_TEST_SENSOR_ACCESS_CONTROL	0x06
    XU_PERIPHERAL_MODE _CONTROL	0x07
    XU_PERIPHERAL_OP_CONTROL	0x08
    XU_PERIPHERAL_ACCESS_CONTROL	0x09
    XU_TEST_TDE_MODE_CONTROL	0x0A
    XU_TEST_GAIN_ACCESS_CONTROL	0x0B
    XU_TEST_LOW_LIGHT_PRIORITY_CONTROL	0x0C
    XU_TEST_COLOR_PROCESSING_DISABLE_CONTROL	0x0D
    XU_TEST_PIXEL_DEFECT_CORRECTION_CONTROL	0x0E
    XU_TEST_LENS_SHADING_COMPENSATION_CONTROL	0x0F
    XU_TEST_GAMMA_CONTROL	0x10
    XU_TEST_INTEGRATION_TIME_CONTROL	0x11
    XU_TEST_RAW_DATA_BITS_PER_PIXEL_CONTROL	0x12
    XU_TEST_ISP_ADDRESS_CONTROL	0x13
    XU_TEST_ISP_ACCESS_CONTROL	0x14
    XU_PERIPHERAL_ACCESS_EXT_CONTROL	0x15
    XU_H264_FRAME_NO_CONTROL	0x16

    """
    x = int(pid, 16)
    y=int(address, 16)
    #print (x)
    mydll.readtestXu.argtypes = [c_int, c_int]
    mydll.readtestXu.restype = Result
    result=mydll.readtestXu(x,y)
    length = result.length
    if length<=0:
        return -1,"failed"
    data = result.str.decode("utf-8")
    string=str(data)
    return length,string



def TestXuWrite(pid,address,val):
    x = int(pid, 16)
    y=int(address, 16)
    z=int(val, 16)
    #print (z)
    a=mydll.writetestXu(x,y,z )
    if a<0:
        #print(a)
        return -1,"fail to write"
    #print(a)
    return 0,"Done:"+hex(a)



def VideoXuRead(pid,address):
    x = int(pid, 16)
    y=int(address, 16)
    mydll.readvideoXu.argtypes = [c_int, c_int]
    mydll.readvideoXu.restype = Result
    result=mydll.readvideoXu(x,y)
    length = result.length
    if length<=0:
        return -1,"failed"
    data = result.str.decode("utf-8")
    string=str(data)
    return length,string



def VideoXuWrite(pid,address,val):
    """
    XU_UNDEFINED_CONTROL	0x00
    XU_VIDEO_COLOR_BOOST_CONTROL	0x01
    XU_VIDEO_NATIVE_MODE_FORCED_CONTROL	0x02
    XU_VIDEO_NATIVE_MODE_AUTO_CONTROL	0x03
    XU_VIDEO_RIGHTLIGHT_MODE_CONTROL	0x04
    XU_VIDEO_RIGHTLIGHT_ZOI_CONTROL	0x05
    XU_VIDEO_FW_ZOOM_CONTROL	0x06
    XU_VIDEO_DUAL_ISO_ENABLE_CONTROL	0x07
    XU_VIDEO_SENSOR_CROPPING_DIMENSION_CONTROL	0x08
    XU_VIDEO_MJPEG_RESYNC_MARKER_CONTROL	0x09
    XU_VIDEO_ADVANCE_DIGITAL_ZOOM_CONTROL	0x0A
    XU_VIDEO_MJPEG_COMPRESS_RATIO_CONTROL	0x0B
    XU_VIDEO_HDR_CONTROL	0x0C

    """
    x = int(pid, 16)
    y=int(address, 16)
    z=int(val, 16)
    #print (z)
    a=mydll.writevideoXu(x,y,z )
    if a<0:
        #print(a)
        return -1,"fail to write"
    #print(a)
    return 0,"Done:"+hex(a)

def PCXuRead(pid,address):
    x = int(pid, 16)
    y=int(address, 16)
    mydll.readpcXu.argtypes = [c_int, c_int]
    mydll.readpcXu.restype = Result
    result=mydll.readpcXu(x,y)
    length = result.length
    if length<=0:
        return -1,"failed"
    data = result.str.decode("utf-8")
    string=str(data)
    return length,string




def PCXuWrite(pid,address,val):
    """
    lvreg pcxu write
    XU_UNDEFINED_CONTROL	0x00
    XU_PERIPHERALCONTROL_PANTILT_RELATIVE_CONTROL	0x01
    XU_PERIPHERALCONTROL_PANTILT_MODE_CONTROL	0x02
    XU_PERIPHERALCONTROL_ MAXIMUM_RESOLUTION_SUPPORT_FOR_PANTILT_CONTROL	0x03
    XU_PERIPHERALCONTROL_AF_MOTORCONTROL	0x04
    XU_PERIPHERALCONTROL_AF _BLOB_CONTROL	0x05
    XU_PERIPHERALCONTROL_AF_VCM_PARAMETERS	0x06
    XU_PERIPHERALCONTROL_AF_STATUS	0x07
    XU_PERIPHERALCONTROL_AF_THRESHOLDS	0x08
    XU_PERIPHERALCONTROL_LED	0x09
    XU_PERIPHERAL_CONTROL_PERIPHERAL_STATUS	0x0A
    XU_PERIPHERAL_CONTROL_SPEAKER_VOLUME	0x0B
    XU_PERIPHERAL_CONTROL_DEVICE_CODEC_STATUS	0x0C
    XU_PERIPHERALCONTROL_PANTILT_ABSOLUTE_CONTROL	0x0C
    XU_PERIPHERALCONTROL_CROPHOME_INFO_CONTROL	0x0D
    XU_PERIPHERAL_CONTROL_MODE	0x0E
    XU_AUDIO_LIBRARY_MODE_CONTROL	0x0F
    XU_PERIPHERAL_MOTOR_STEPS_CONTROL	0x10
    XU_PERIPHERAL_USB_ENUMERATION_CONTROL	0x11


    """
    x = int(pid, 16)
    y=int(address, 16)
    z=int(val, 16)
    #print (z)
    a=mydll.writepcXu(x,y,z )
    if a<0:
        #print(a)
        return -1,"fail to write"
    #print(a)
    return 0,"Done:"+hex(a)




def SN_Read(pid,address):
    x = int(pid, 16)
    y=int(address, 16)
    #print (x)
    a=mydll.readsn(x,y )
    if a<0:
        return -1,"fail to read"
    return 0,hex(a)

def checkdevice(vid,pid):
    x = int(vid, 16)
    y = int(pid, 16)
    z=mydll.pidcheck(x,y)
    size=-1
    x1=string_at(z,size)
    ch=str(x1,'utf-8')
    first_char = ch[0]
    if ch=="failed":
        return -1,-1,ch

    return 0,int(first_char)-1,ch

def checkindex(vid,pid):
    x = int(vid, 16)
    y = int(pid, 16)
    z=mydll.pidcheck(x,y)
    size=-1
    x1=string_at(z,size)
    ch=str(x1,'utf-8')
    first_char = ch[0]
    if ch=="failed":
        return -1
    return int(first_char)-1


def multi_device_check(pid):
    x = int(pid, 16)
    a=mydll.mutildevececheck(x)
    b=int(a)
    return int(b)

def inforXURead(pid,address):
    """
    XU_UNDEFINED_CONTROL	0x00
    XU_FIRMWARE_VERSION_CONTROL	0x01
    XU_FIRMWARE_CRC_CONTROL	0x02
    XU_EEPROM_VERSION_CONTROL	0x03
    XU_SENSOR_INFORMATION_CONTROL	0x04
    XU_PROCESSOR_INFORMATION_CONTROL	0x05
    XU_USB_INFORMATION_CONTROL	0x06
    XU_INFO_WEBCAM_STATUS_CONTROL	0x07
    Reserved	0x08
    XU_LENS_FOV_CONTROL	0x09
    XU_SENSOR_DIMENSION_CONTROL	0x0A
    XU_EXTENDED_FIRMWARE_VERSION_CONTROL  	0x0B


    """
    x = int(pid, 16)
    y=int(address,16)
    # Define the argument types for the readinfoXU function
    mydll.readinfoXU.argtypes = [c_int, c_int]
    mydll.readinfoXU.restype = Result
    result=mydll.readinfoXU(x,y)
    length = result.length
    if length<=0:
        return -1,"failed"
    data = result.str.decode("utf-8")
    string=str(data)
    #print("Result: length={}, data={}".format(length, data.decode("utf-8")))
    if y==1:
        return length, "FW:{}.{}.{}".format(int(string[2:4]),int(string[0:2]),int(string[6:8]+string[4:6],16))
    return length,string

def deviceXURead(pid,address):
    x = int(pid, 16)
    y=int(address,16)
    # Define the argument types for the readinfoXU function
    mydll.readinfoXU.argtypes = [c_int, c_int]
    mydll.readinfoXU.restype = Result
    result=mydll.readinfoXU(x,y)
    length = result.length
    if length<=0:
        return -1,"failed"
    data = result.str.decode("utf-8")
    string=str(data)
    return length,string




if(__name__)=="__main__":

    #aa,b,bb=checkdevice("86")
    a=multi_device_check("919")
    print(a)
    # print(inforXURead("866","a"))
    # print(TestXuRead("866", "1"))
    # print(PCXuRead("866", "a"))











