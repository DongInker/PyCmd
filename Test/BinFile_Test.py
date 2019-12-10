# -*- coding: utf-8 -*-

import sys
import time
import serial
import struct

def DemoMsg():
    print("LastEdit:2019/11/07");

BinFmt = {
        "le2be"       :'<',
        "magic"       :'H', # 2
        "Crc"         :'H', # 2
        "Major"       :"B", # 1
        "Minor"       :"B", # 1
        "Patch"       :"B", # 1
        "Seconds"     :"B", # 1
        "Minutes"     :"B", # 1
        "Hours"       :"B", # 1
        "Day"         :"B", # 1
        "Month"       :"B", # 1
        "Year"        :"H", # 2
        "DataBytes"   :"H", # 4
        "DataLen"     :"L", # 4
        };

CfgFmt = {
        "Mode"        :'H', # 2
        "Voltage"     :'f', # 4
        "SignFreq"    :'f', # 4 50.0Hz
        "SmpFreq"     :'L', # 4 18000Hz
        };

ch1 = [0,1,2,3,2,1,0]; # 'H'
ch2 = [1,2,3,4,3,2,1]; # 'H'
ch3 = [2,3,4,5,4,3,2]; # 'H'

def BinWfm():

    '''
    #文件头 (0) + 128
    BinData  = struct.pack(BinFmt['le2be']+BinFmt['magic'        ],0X0FF0);
    BinData += struct.pack(BinFmt['le2be']+BinFmt['Crc'          ],0X0102);
    BinData += struct.pack(BinFmt['le2be']+BinFmt['Major'        ],0);
    BinData += struct.pack(BinFmt['le2be']+BinFmt['Minor'        ],1);
    BinData += struct.pack(BinFmt['le2be']+BinFmt['Patch'        ],2);
    BinData += struct.pack(BinFmt['le2be']+BinFmt["Seconds"      ],30);
    BinData += struct.pack(BinFmt['le2be']+BinFmt["Minutes"      ],45);
    BinData += struct.pack(BinFmt['le2be']+BinFmt["Hours"        ],22);
    BinData += struct.pack(BinFmt['le2be']+BinFmt["Day"          ],7);
    BinData += struct.pack(BinFmt['le2be']+BinFmt["Month"        ],11);
    BinData += struct.pack(BinFmt['le2be']+BinFmt["Year"         ],2019);
    BinData += struct.pack(BinFmt['le2be']+BinFmt['DataBytes'    ],2);
    BinData += struct.pack(BinFmt['le2be']+BinFmt['DataLen'      ],len(wavedata));
    BinData = BinData.ljust(128, b'\x00');

    #测试参数 (128) + 128
    BinData += struct.pack(BinFmt['le2be']+CfgFmt['Mode'         ],0X0000);
    BinData += struct.pack(BinFmt['le2be']+CfgFmt['Voltage'      ],800.0);
    BinData += struct.pack(BinFmt['le2be']+CfgFmt['SignFreq'     ],50.0);
    BinData += struct.pack(BinFmt['le2be']+CfgFmt['SmpFreq'      ],18000);
    BinData = BinData.ljust(256, b'\x00');

    #测试结论 (128+128) + 256
    BinData = BinData.ljust(512, b'\x00');

    #波形数据 (128+128+256) + DataLen * DataBytes
    for i in wavedata:
        BinData += struct.pack(BinFmt['le2be']+'H',i);

    print(BinData);

    print(BinFmt);
    print(CfgFmt);
    '''

    chs = 1;
    BinData  = struct.pack(BinFmt['le2be']+'L',len(ch1)*2*chs+10); # BinByteLen
    BinData += struct.pack(BinFmt['le2be']+'H',chs);                    # chs
    BinData += struct.pack(BinFmt['le2be']+'L',len(ch1)*2);        # DataByteLen
    if(chs > 0):
        for i in ch1:
            BinData += struct.pack(BinFmt['le2be']+'H',i);

    if(chs > 1):
        for i in ch2:
            BinData += struct.pack(BinFmt['le2be']+'H',i);

    if(chs > 2):
        for i in ch3:
            BinData += struct.pack(BinFmt['le2be']+'H',i);

    print(BinData);
    return BinData;

###########################
if __name__ == '__main__':

    print("One Py Debug!");
    '''
    BinWfm();

    '''
    try:
        ser = serial.Serial("com7",115200);
    except Exception as e:
        print(e);

    rxdcmd = '';
    #进入调试循环
    while True:
        time.sleep(0.01); 
        try:#当usb重新拔插时 USB转串口必须重新连接
            ser.in_waiting;
            rxdbuf = ser.read(ser.in_waiting);
            #if(len(rxdbuf) > 0):
            #    print(rxdbuf);
        except Exception as e:
            print(e);

        if(len(rxdbuf) > 0):
            ser.write(rxdbuf);
            rxdstr = rxdbuf.decode('gb18030');
            print(rxdstr,end='');
            rxdstr  = rxdstr.lower()#将字符统一转换为小写
            rxdcmd += rxdstr;

            if(rxdcmd.find("help\r") != -1):
               #print("------------- .. RW ------------");
                print("  DemoMsg     .. R- Demo Message");
                print("  BinWfm      .. R- Bin File WFM");
                rxdcmd = '';

            if(rxdcmd.find("demomsg\r") != -1):
                rxdcmd = '';
                DemoMsg();

            if(rxdcmd.find("binfile") != -1):
                rxdcmd = '';
                time.sleep(0.5); 
                ser.write(BinWfm());

        sys.stdout.flush();#强制打印缓存数据
    #'''
