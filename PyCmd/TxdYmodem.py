# -*- coding: utf-8 -*-
#
# Original code by:
#    Inker.Dong <dongmaowan99@163.com>
#    Copyright 2019 Inker.Dong
#
# Subsequent changes:

'''
import serial
from TxdYmodem import YMODEM

def getc(size):
    #注意 发送数据后直接调用read函数会使发送数据偶尔出错 所以先判读再读
    if(ser.in_waiting != 0):
        rxd = ser.read(size);
    else:
        rxd = None;
    return rxd;

def putc(data):
    return ser.write(data);

def callback(FileLen,TxdLen):
    a = round(20*TxdLen/FileLen);
    b = 20-a;
    print('\r%3dkB %3dkB |%s%s| %d%%            '%(FileLen/1024,TxdLen/1024,a*'▇',b*'  ',(TxdLen/FileLen)*100),end='\r')

stream = open('E:\\pytest\\test.txt','rb');
ser = serial.Serial("com1",115200);
Ymodem = YMODEM(getc,putc);
Ymodem.send(stream, 3, callback);

'''

__version__ = "1.0.0"

'''
Rxd <<<  C
Txd >>>  SOH 00 FF Name_00 Len_00 NULL(0) crcH crcL
Rxd <<<  ACK
Rxd <<<  C
Txd >>>  STX 01 FE data[1024] crcH crcL
Rxd <<<  ACK
Txd >>>  STX 02 FD data[1024] crcH crcL
Rxd <<<  ACK
Txd >>>  STX 03 FC data[1024] crcH crcL
Rxd <<<  ACK
Txd >>>  STX 04 FB data[1024] crcH crcL
Rxd <<<  ACK
Txd >>>  SOH 05 FA data[100]  1A[28] crcH crcL
Rxd <<<  ACK
Txd >>>  EOT
Rxd <<<  NAK
Txd >>>  EOT
Rxd <<<  ACK
Rxd <<<  C
Txd >>>  SOH 00 FF NUL[128] crcH crcL
Rxd <<<  ACK
'''

# Protocol bytes
SOH = b'\x01'
STX = b'\x02'
EOT = b'\x04'
ACK = b'\x06'
DLE = b'\x10'
NAK = b'\x15'
CAN = b'\x18'
CRC = b'C'


import logging
import time
import os

class YMODEM(object):
    # crctab calculated by Mark G. Mendel, Network Systems Corporation
    crctable = [
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,
        0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,
        0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,
        0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,
        0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,
        0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,
        0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,
        0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,
        0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,
        0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,
        0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,
        0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,
        0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,
        0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,
        0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,
        0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,
        0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,
        0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,
        0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,
        0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,
        0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,
        0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,
        0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,
        0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0,
    ]

    def __init__(self, getc, putc, mode='xmodem', pad=b'\x1a'):
        self.getc = getc
        self.putc = putc
        self.mode = mode
        self.pad  = pad
        self.log = logging.getLogger('xmodem.XMODEM')

    def calc_crc(self, data, crc=0):
        for char in bytearray(data):
            crctbl_idx = ((crc >> 8) ^ char) & 0xff
            crc = ((crc << 8) ^ self.crctable[crctbl_idx]) & 0xffff
        return crc & 0xffff

    def _make_send_checksum(self, data):
        _bytes = []
        crc = self.calc_crc(data)
        _bytes.extend([crc >> 8, crc & 0xff])
        return bytearray(_bytes)

    def _make_send_header(self, packet_size, sequence):
        assert packet_size in (128, 1024), packet_size
        _bytes = []
        if packet_size == 128:
            _bytes.append(ord(SOH))
        elif packet_size == 1024:
            _bytes.append(ord(STX))
        _bytes.extend([sequence, 0xff - sequence])
        return bytearray(_bytes)

    def send(self, stream, timeout=3, callback=None):
        TimeOutMs = timeout*1000;# S > mS
        TimeMsCnt = 0;

        # Wait Rxd 'C'
        while True:
            char = self.getc(1);
            if char == CRC:
                TimeMsCnt = 0;
                break;

            time.sleep(0.001);
            TimeMsCnt += 1;
            if TimeMsCnt > TimeOutMs:
                print("TimeOut Wait Rxd C")
                return False;

        # Txd:SOH Name Len  Rxd:ACK
        FileName = os.path.basename(stream.name);
        FileLen  = len(stream.read());
        stream.seek(0);
        FileLens = str(FileLen);
        data = FileName.encode('utf-8') + b'\x00' + FileLens.encode('utf-8');
        
        header = self._make_send_header(128, 0)
        data = data.ljust(128, b'\x00')
        checksum = self._make_send_checksum(data)
        self.putc(header + data + checksum)

        # An ACK should be returned
        while True:
            char = self.getc(1);
            if char == ACK:
                TimeMsCnt = 0;
                break
            else:
                time.sleep(0.001);
                TimeMsCnt += 1;
                if TimeMsCnt > TimeOutMs:
                    print("TimeOut sSOH Wait Rxd Ack")
                    return False;

        # Wait Rxd 'C'
        while True:
            char = self.getc(1);
            if char == CRC:
                TimeMsCnt = 0;
                break;

            time.sleep(0.001);
            TimeMsCnt += 1;
            if TimeMsCnt > TimeOutMs:
                print("TimeOut sSOH Wait Rxd C")
                return False;

        # send data
        stime = time.clock();
        packet_size = 1024;
        sequence = 1;
        TxdLen = 0;
        while True:
            data = stream.read(packet_size)
            TxdLen += len(data);
            if not data:
                break; # go to Send EOT
            if(len(data) > 128):
                packet_size = 1024;
            else:
                packet_size = 128;

            header = self._make_send_header(packet_size, sequence)
            data = data.ljust(packet_size, self.pad)
            checksum = self._make_send_checksum(data)
            self.putc(header + data + checksum)

            sequence = (sequence + 1) % 0x100
            if callable(callback):
                callback(FileLen,TxdLen);
            
            while True:
                char = self.getc(1)
                if char == ACK:
                    TimeMsCnt = 0;
                    break;

                time.sleep(0.001);
                TimeMsCnt += 1;
                if TimeMsCnt > TimeOutMs:
                    print("TimeOut STX Wait Rxd ACK")
                    return False;

        etime = time.clock();
        print("\nTime:%0.3fS %0.1fkB/S"%(etime-stime,TxdLen/(etime-stime)/1024));
        # Txd:EOT  Rxd:NAK
        self.putc(EOT)
        while True:
            char = self.getc(1)
            if char == NAK or char == ACK: # 升级应答为 ACK 为什么不是NAK ???
                TimeMsCnt = 0;
                break
            else:
                time.sleep(0.001);
                TimeMsCnt += 1;
                if TimeMsCnt > TimeOutMs:
                    print("TimeOut EOT 1 Wait Rxd NAK")
                    return False;

        # Txd:EOT  Rxd:ACK
        self.putc(EOT);
        while True:
            char = self.getc(1)
            if char == ACK:
                TimeMsCnt = 0;
                break
            else:
                time.sleep(0.001);
                TimeMsCnt += 1;
                if TimeMsCnt > TimeOutMs:
                    print("TimeOut EOT 2 Wait Rxd ACK")
                    return False;

        # Wait Rxd 'C'
        while True:
            char = self.getc(1);
            if char == CRC:
                TimeMsCnt = 0;
                break;

            time.sleep(0.001);
            TimeMsCnt += 1;
            if TimeMsCnt > TimeOutMs:
                print("TimeOut eSOH Wait Rxd C")
                return False;

        # Txd:SOH  Rxd:ACK
        data = bytearray(b'\x00'*128);
        header = self._make_send_header(128, 0)
        checksum = self._make_send_checksum(data)
        self.putc(header + data + checksum)

        while True:
            char = self.getc(1)
            if char == ACK:
                break
            else:
                time.sleep(0.001);
                TimeMsCnt += 1;
                if TimeMsCnt > TimeOutMs:
                    print("TimeOut eSOH Wait Rxd ACK")
                    return False;

        return True

