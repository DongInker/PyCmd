
import sys
import os.path
import time
import datetime
import serial
import struct

'''
struct.pack(fmt,v1,v2,.....)
struct.unpack(fmt,string)     a1, a2 = struct.unpack("ii", str) 
------------------------------
|Format | c Type          | Python |
|   x   | pad byte        | no value
|   c   | char            | string of length 1
|   b   | signedchar      | integer
|   B   | unsignedchar    | integer
|   ?   | _Bool           | bool
|   h   | short           | integer
|   H   | unsignedshort   | integer
|   i   | int             | integer
|   I   | unsignedint     | integer or long
|   l   | long            | integer
|   L   | unsignedlong    | long
|   q   | longlong        | long
|   Q   | unsignedlonglong| long
|   f   | float           | float
|   d   | double          | float
|   s   | char[]          | string
|   p   | char[]          | string
|   P   | void*           | long
'''

def swap_bytes(word_val):
    """swap lsb and msb of a word"""
    msb = (word_val >> 8) & 0xFF
    lsb = word_val & 0xFF
    return (lsb << 8) + msb


def calculate_crc(data):
    """Calculate the CRC16 of a datagram"""
    crc = 0xFFFF
    for i in data:
        crc = crc ^ i
        for j in range(8):
            tmp = crc & 1
            crc = crc >> 1
            if tmp:
                crc = crc ^ 0xA001
    #return swap_bytes(crc)
    return crc;

from format    import isFloatType,isUintType;

class cMbsRtu(object):
    def __init__(self):
        # 调用外部包 模块
        from Com import ComSendHex,ComRxdMode,isComRxdMode,ComRxdBuf;

        # 连接
        self.MbsTxdFunc    = ComSendHex;
        self.RxdModeFunc   = ComRxdMode;
        self.isRxdModeFunc = isComRxdMode;
        self.RxdBufFunc    = ComRxdBuf;
        
        self.AckCnt    = 0;

        #创建串口通信记录文件路径
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.dirname(os.getcwd()) + '/Logs/';
        self.mbs_name = path + rq + 'mbs.txt';

        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.PrfClass  = int(GetConfig('MbsRtu', 'PrfClass',   '0'));
        self.SlaveID   = int(GetConfig('MbsRtu', 'SlaveID',    '1'));
        self.AckWaitmS = int(GetConfig('MbsRtu', 'AckWait10mS','50'));

    def sMbsRtuSetCfg(self):
        self.SetConfig('MbsRtu', 'PrfClass', str(self.PrfClass));
        self.SetConfig('MbsRtu', 'PrfClass', str(self.SlaveID));
        self.SetConfig('MbsRtu', 'PrfClass', str(self.AckWaitmS));
        
    def MbsRtuMsg(self):
        print("LastEdit:2018/11/08");
        print("PrfClass :%d"%(self.PrfClass));
        print("SlaveID  :%d"%(self.SlaveID));
        print("AckWait  :%dmS"%(self.AckWaitmS*10));
        
    def MbsRtuPrf(self,PrfClass):
        self.PrfClass = PrfClass;
        self.sMbsRtuSetCfg();
        
    def MbsSlaveID(self,id):
        self.SlaveID = id;
        self.sMbsRtuSetCfg();
        
    def sMbsAckWaitmS(self,ackwait):
        self.AckWaitmS = ackwait;
        self.sMbsRtuSetCfg();
        
    def MbsSend(self,data):
        crc = struct.pack("<H",calculate_crc(data))# <:little-endian
        data += crc;

        txd = '[%s]-Txd>>:'%(datetime.datetime.now().strftime('%H:%M:%S.%f'));
        for i in data:
            txd += '%02X '%(i);
        print(txd);
        #写入 XXXXmbs.txt 文件
        f=open(self.mbs_name,'a');
        f.write(txd+'\r\n');
        f.close();
        
        self.MbsTxdFunc(data);
        self.RxdModeFunc(1);
        self.AckCnt = self.AckWaitmS;
        
    def Mbs0x03(self,s_addr,num):
        data = struct.pack('>BBHH',self.SlaveID,3,s_addr,num);# >:big-endian
        self.MbsSend(data);

    def Mbs0x06(self,addr,val):
        data = struct.pack('>BBHH',self.SlaveID,6,addr,val);
        self.MbsSend(data);
        
    def sMbsRtu_10mS(self):
        if(self.AckCnt == 0):
            return 0;
            
        self.AckCnt -= 1;
        if(self.AckCnt == 0):#应答超时
            self.RxdModeFunc(0);
            print('Ack Over Time %dmS!'%(self.AckWaitmS));
            #写入 XXXXmbs.txt 文件
            rxd = '[%s]-Rxd<<:'%(datetime.datetime.now().strftime('%H:%M:%S.%f'));
            rxd += 'Ack Over Time!';
            f=open(self.mbs_name,'a');
            f.write(rxd+'\r\n');
            f.close();
            
        if(self.isRxdModeFunc()==0):#应答成功
            self.AckCnt = 0;
            rxdbytes = self.RxdBufFunc();#获取串口接收数据
            #print(struct.unpack(">BBHHH",rxdbytes));
            rxdstr   = [ord(i) for i in rxdbytes];#bytes数组转字符数据
            if(len(rxdstr)):
                rxd = '[%s]-Rxd<<:'%(datetime.datetime.now().strftime('%H:%M:%S.%f'));
                for i in rxdstr:
                    rxd += '%02X '%(i);
                print(rxd);
                #写入 XXXXmbs.txt 文件
                f=open(self.mbs_name,'a');
                f.write(rxd+'\r\n');
                f.close();
                
    def sMbsRtuCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .MbsRtu');
            return False;

        if(cmdlist[0] == '.mbsrtu'):
           #print("------------- .. RW ------------");
            print("  MbsRtuMsg   .. R- MbsRtu Message");
            print("  MbsRtuPrf   .. -W MbsRtu Printf Class <0,1>");
            print("  MbsRtuID    .. -W Modbus ID <1,255>");
            print("  MbsAckWait  .. -W Ack Over Time 10mS <1~5000>");
            print("  Mbs03       .. -W Modbus Func 0X03 <addr,num>");
            print("  Mbs06       .. -W Modbus Func 0X06 <addr,val>");
            print("  Mbsf        .. -W Modbus float <addr> [val]");
            return True;

        if(cmdlist[0] == 'mbsrtumsg'):
            self.MbsRtuMsg();
            return True;
            
        if(cmdlist[0] == 'mbsrtuprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                        return False;
                self.MbsRtuPrf(int(cmdlist[1]));
                print('MbsRtuPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;        

        if(cmdlist[0] == 'mbsrtuid'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.MbsSlaveID(int(cmdlist[1]));
                print('MbsSlaveID <= {0}'.format(cmdlist[1]));
                return True;
            return False;

        if(cmdlist[0] == 'mbsackwait'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sMbsAckWaitmS(int(cmdlist[1]));
                print('MbsAckWaitTime <= %smS'%(cmdlist[1]));
                return True;
            return False;        
                
        if(cmdlist[0] == 'mbs03'):
            if(len(cmdlist) == 3):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                if(cmdlist[2].isdigit() == False):#不是数字直接结束
                    return False;
                self.Mbs0x03(int(cmdlist[1]),int(cmdlist[2]));
                return True;
            return False;

        if(cmdlist[0] == 'mbs06'):
            if(len(cmdlist) == 3):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                if(cmdlist[2].isdigit() == False):#不是数字直接结束
                    return False;  
                self.Mbs0x06(int(cmdlist[1]),int(cmdlist[2]));
                return True;
            return False;
            
        if(cmdlist[0] == 'mbsf'):
            if(len(cmdlist) == 2):#读浮点寄存器值
                if(isUintType(cmdlist[1])  == False):
                    return False;
                data = struct.pack('>BBHH',self.SlaveID,0X03,int(cmdlist[1]),0X02);
                self.MbsSend(data);
                return True;
                
            if(len(cmdlist) == 3):#写浮点寄存器值
                if(isUintType(cmdlist[1])  == False):
                    return False;
                if(isFloatType(cmdlist[2]) == False):
                    return False;
                data = struct.pack('>BBHHBf',self.SlaveID,0X10,int(cmdlist[1]),2,4,float(cmdlist[2]));
                self.MbsSend(data);
                return True;
            return False;
            
        return False;

# 实例化类
MbsRtu = cMbsRtu();
# 外调接口
def MbsRtuCmd(incmd):
    return MbsRtu.sMbsRtuCmd(incmd);

def PrjB_10mS_MbsRtu():
    MbsRtu.sMbsRtu_10mS();
    