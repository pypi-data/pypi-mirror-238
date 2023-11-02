##write dll for Lvreg by python, can be by PID

##//////////usage://///////////////
## please:    pip install xu_tde-2021.2.1-py3-none-any.whl
##import xu_tde as lv
##flag,index,value=lv.checkdevice(PID)    ## flay ,0 means find. if -1 means never find
##flag1,value1=lv.inforXURead(PID,address)
##flag2,value2=lv.TestXuRead(PID,address)
##flag3,value3=lv.TestXuWrite(PID,address,data)
##flag4,value4=lv.VideoXuRead(PID,address) 
##flag5,value5=lv.VideoXuWrite(PID,zoomaddress,zoom_data)
##flag6,value6=lv.EepromWrite(PID,address,val_to_write)
##flag7,value7=lv.EepromRead(PID,address)
##/////////////////////////////////////////
##VC_tde USE only  @ logitech , Lorry RUi
##


import xu_tde as lv

PID="0x866"     ## this can poin to PID device  and VID Hardcoded , just for logi device
address="01"
valtowrite="55"
address2="5f"
tdemode_value="8"
tdemodeaddress="a"
zoomaddress="6"
zoom_data="c8" ## zoom 200 is c8,100 is 64

if(__name__)=="__main__":

    flag,index,value=lv.checkdevice(PID)   ## flay ,0 means find. if -1 means never find   
    print("flag:{},index:{},read from USB:{} ".format(flag,index,value))
    print("\n")

    ######################## check FW version ##############################
    flag1,value1=lv.inforXURead(PID,address)   ## flay ,0 means find. if -1 means never find, address 1 is FW version    
    print("flag:{},PID:{}FW version:{} ".format(flag1,PID,value1))
    print("\n")

    ######################## TestXu  ##############################   
    flag2,value2=lv.TestXuRead(PID,tdemodeaddress)   ## flay ,0 means find. if -1 means never find, address 1 is FW version
    print("flag:{},test_xu_value:{} ".format(flag2,value2))
    flag3,value3=lv.TestXuWrite(PID,tdemodeaddress,tdemode_value)   ## flay ,0 means find. if -1 means never find, address 1 is FW version
    print("flag:{},test_xu_value:{} ".format(flag3,value3))
    print("\n")

    ######################## VideoXu ##############################
    flag4,value4=lv.VideoXuRead(PID,zoomaddress)   ## flay ,0 means find. if -1 means never find, address 1 is FW version
    print("flag:{},Video_xu_value:{} ".format(flag4,value4))
    flag5,value5=lv.VideoXuWrite(PID,zoomaddress,zoom_data)   ## flay ,0 means find. if -1 means never find, address 1 is FW version
    print("flag:{},Video_xu_value:{} ".format(flag5,value5))
    print("\n")

    ######################## PCXu ##############################
    flag8,value4=lv.PCXuRead(PID,'9')   ## flay ,0 means find. if -1 means never find, address 9 is LED
    print("flag:{},PC_xu_value:{} ".format(flag4,value4))
    flag9,value5=lv.PCXuWrite(PID,'9','0')   ## flay ,0 means find. if -1 means never find,  turn the LED off
    print("flag:{},PC_xu_value:{} ".format(flag5,value5))
    print("\n")


    
    ######################## EEprom  ##############################
    #flag6,value6=lv.EepromWrite(PID,address,valtowrite)## flay ,0 means find. if -1 means failed
    #print("flag:{},Write Hex:{}  ".format(flag6,value6))
    flag7,value7=lv.EepromRead(PID,address) ## flay ,0 means find. if -1 means failed
    print("flag:{},EErprom{}Read Hex:{}  ".format(flag7,address,value7))
    print("\n")

##    for x in range(int(address,16), int(address2,16)):
##        flag8,value8=lv.EepromRead(PID,str(x))
##        print("flag:{},{} Read Hex:{}".format(flag8,hex(x),value8))
        
        


    











