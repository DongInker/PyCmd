
import sys
import os.path
import time

from Log import Log;

class cCom(object):
    def __init__(self,prf=0,com=6):

        # 调用外部包 模块
        import serial.tools.list_ports
        
        
        # 连接内部
        self.ComMsgFunc = serial.tools.list_ports.comports;#获取串口信息
        self.ComDll     = windll.LoadLibrary("PCOMM.DLL");
        
        self.BaudRate = '115200'; # 9600 38400 115200
        self.DataBit  = '8';      # 5 6 7 8
        self.Parity   = 'None';   # None Even Odd Mark Space
        self.StopBit  = '1';      # 1 1.5 2
        self.isConnected = False;
        self.RxdMode  = 0; #0:str 1:Hex
        self.RxdBuf   = 0;

        self.RxdHalfBuf   = '';#接受一半数据缓存
        self.RxdHalfFlag  = 0; #接受一半数据标记
        #self.ComConnect();

        #创建串口通信记录文件路径
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.dirname(os.getcwd()) + '\\Logs\\';
        self.com_name = path + rq + 'com.txt';
        
        f=open(self.com_name,'a');
        f.close();
            
        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.PrfClass  = int(GetConfig('Com', 'PrfClass',  '0'));
        self.ComNum    = int(GetConfig('Com', 'SerialNum', '1'));
        self.StartCon  =     GetConfig('Com', 'StartCon',  'open');

        if(self.StartCon == 'open'):
            self.ComConnect();
            
    def sComSetCfg(self):
        self.SetConfig('Com', 'PrfClass',  str(self.PrfClass));
        self.SetConfig('Com', 'SerialNum', str(self.ComNum));
        self.SetConfig('Com', 'StartCon',      self.StartCon);
        
    def ComMsg(self):
        print("LastEdit:2018/11/20");
        print("PrfClass:%d"%(self.PrfClass));
        print("StartCon:%s"%(self.StartCon));
        print('Com Num :%d(%d)'%(self.ComNum,self.isConnected));
        print('Com Cfg BaudRat:%s DataBit:%s Parity:%s StopBit:%s'%(self.BaudRate,self.DataBit,self.Parity,self.StopBit));
        
    def ComPrf(self,PrfClass):
        self.PrfClass = PrfClass;
        self.sComSetCfg();# 保存串口参数

    def sComStartCon(self,cmd):
        self.StartCon = cmd;
        self.sComSetCfg();
        
    def ComList(self):
        plist = list(self.ComMsgFunc())
        if(len(plist) <= 0):
            print ("The Serial port can't find!")
        else:
            for i in range(0,len(plist)):
                plist_0 =list(plist[i]);
                print('{0:6s}:{1:s}'.format(plist_0[0],plist_0[1]));

    def ComTxd(self,txd):
        # 发送数据时 串口未打开 尝试打开串口
        if(self.isConnected == False):
            self.ComConnect();    
        if(self.isConnected == True):
            #self.ComTxt.write(txd);
            self.ComDll.sio_write(self.ComNum,txd,len(txd));
        
    def ComConnect(self):
        ret = self.ComDll.sio_open(self.ComNum);
        if(ret != 0):
            print("Open <Com%d> Error %d!"%(self.ComNum,ret));
            self.isConnected = False;
            return ret;

        # 115200, 无校验，8位数据位，1位停止位
        ret = self.ComDll.sio_ioctl(self.ComNum, 16, 0x00 | 0x03 | 0x00);
        if(ret != 0):
            print("Config <Com%d> Param Error %d!"%(self.ComNum,ret));
            return 0;
            
        #self.ComDll.sio_cnt_irq(self.ComNum,RxdFunc, 1);
        self.isConnected = True;
        
    def ComDisconnent(self):
        self.ComDll.sio_close(self.ComNum);
        self.RxdHalfFlag = 0;
        self.RxdHalfBuf  = '';
        self.isConnected = False;
        
    def SetComNum(self,comnum):
        # 关闭旧串口
        self.ComDisconnent(); # 开启self.ComDll.sio_cnt_irq(self.ComNum,RxdFunc, 1); 执行关闭程序异常
        self.ComNum = comnum;
        # 打开新串口
        self.ComConnect();
        self.sComSetCfg();# 保存串口参数
        
    def GetComNum(self):
        return self.ComNum;
        
    def sSetRxdMode(self,mode):
        self.RxdMode = mode;
        if(mode == 1):
            self.RxdBuf  = '';
    def sGetRxdMode(self):
        return self.RxdMode;

    def sGetRxdBuf(self):
        return self.RxdBuf;

    def sPrjF_10mS_Com(self):
        if(self.isConnected == False):
            return 0;
        
        status = self.ComDll.sio_data_status(self.ComNum);
        if(status):
            Log.logger.error("Com State Error:%X"%(status));
            #print("******************%X"%(status));
            self.ComDisconnent();
            return 0;
            
        num = self.ComDll.sio_iqueue(self.ComNum);
        if(num <= 0):
            return 0;
            
        rxdbuf = create_string_buffer(num);
        self.ComDll.sio_read(self.ComNum,rxdbuf, num);

        # 接收十六进制模式
        if(self.RxdMode == 1):
            self.RxdBuf = rxdbuf;
            self.RxdMode = 0;
            return 0;

        #'''
        attempts = 0;
        success  = False;
        DoneFlag = 0;
        rxdval   = rxdbuf.value;
        rxd      = rxdval;
        #while attempts < 3 and DoneFlag == 0:
        while DoneFlag == 0:    
            try:
                rxdstr   = rxd.decode('gb18030');
                success  = True;
                DoneFlag = 1;
                if(attempts <= 1):
                    self.RxdHalfFlag = 0;
                    self.RxdHalfBuf  = '';
                if(attempts == 2):# Last RxdBuf
                    self.RxdHalfFlag = 1;
                    self.RxdHalfBuf  = rxdval[len(rxdval)-1];
            except Exception as e:
                attempts += 1;
                if(attempts == 1):
                    if(self.RxdHalfFlag):# last + rxd
                        rxd = bytes([self.RxdHalfBuf]) + rxdval;
                    else:
                        rxd = rxdval;
                        
                if(attempts == 2):
                    if(self.RxdHalfFlag):# last + rxd[0:n-1];
                        rxd = bytes([self.RxdHalfBuf]) + rxdval[0:len(rxdval)-1];
                    else:
                        rxd = rxdval[0:len(rxdval)-1];
                        
                if(attempts >= 3):# Rxd Err
                    Log.logger.error(e);
                    self.RxdHalfFlag = 0;
                    self.RxdHalfBuf  = '';
                    DoneFlag = 1;
        
        if(success == True):
            # 输出控制台
            sys.stdout.write(rxdstr);
            sys.stdout.flush();
            
            # 写入 XXXXcom.txt 文件
            with open(self.com_name,'a') as f:
                f.write(rxdstr);
            #f=open(self.com_name,'a');
            #f.write(rxdstr);
            #f.close();
            
    def sComSaveFile(self):
        return self.com_name;
        
    def sComCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .Com');
            return False;

        if(cmdlist[0] == '.com'):
            #print("------------- .. RW ------------");
            print("  ComMsg       .. R- Com Message");
            print("  ComPrf       .. -W Com Printf Class <0,1>");
            print("  ComList      .. R- Com List");
            print("  ComNum       .. -W Set Com Num <1~255>");
            print("  ComClose     .. -W Close Com");
            #print("  ComBR        .. -W Set Com BaudRate <9600,115200>");
            #print("  ComDataBit   .. -W Set Com DataBit  <5,6,7,8>");
            #print("  ComParity    .. -W Set Com Parity   <None,Even,Odd>");
            #print("  ComStopBit   .. -W Set Com StopBit  <1,2>");
            print("  StartCon     .. -W Start Com Con <open,close>");
            return True;

        if(cmdlist[0] == 'commsg'):
            self.ComMsg();
            return True;
            
        if(cmdlist[0] == 'comprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.ComPrf(int(cmdlist[1]));
                print('ComPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;

        if(cmdlist[0] == 'comlist'):
            self.ComList();
            return True;
            
        if(cmdlist[0] == 'comnum'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.SetComNum(int(cmdlist[1]));
                print('ComNum <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        if(cmdlist[0] == 'comclose'):
            self.ComDisconnent();
            return True;
            
        if(cmdlist[0] == 'startcon'):
            if(len(cmdlist) == 2):
                self.sComStartCon(cmdlist[1]);
                print('ComStartCon <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        return False;

##################################
from ctypes import *
import time

def RxdComData(port=1):
    time.sleep(0.01);# 时间不足会导致获取数据分段 导致解码出错
    
    num = Com.ComDll.sio_iqueue(Com.GetComNum());
    rxdbuf = create_string_buffer(num);
    Com.ComDll.sio_read(Com.GetComNum(),rxdbuf, num);
    
    if(Com.sGetRxdMode() == 1):
        Com.RxdBuf = rxdbuf;
        Com.sSetRxdMode(0);
        return Com.GetComNum();
        
    rxd = rxdbuf.value;    
    #rxd = rxd.decode('gb18030');
    #rxd = rxd.decode('ascii');
    #rxd = rxd.decode('gb2312');
    rxd = rxd.decode('gbk');
    sys.stdout.write(rxd);
    sys.stdout.flush();
    return Com.GetComNum();

CALLBACK = WINFUNCTYPE(c_int);
RxdFunc = CALLBACK(RxdComData);
#########################
def cb(xmitlen, buflen, pbuf, flen):
    #print(xmitlen, flen,end='\r');
    if(flen):
        a = round(20*xmitlen/flen);
        b = 20-a;
        print('%3dkB %3dkB |%s%s| %d%%'%(flen/1024,xmitlen/1024,a*'▇',b*'  ',(xmitlen/flen)*100),end='\r')
    return xmitlen

CALLBACK = WINFUNCTYPE(c_int, c_long, c_int, POINTER(c_char), c_long)
ccb = CALLBACK(cb)

#选择烧写文件
import os
import tkinter,tkinter.filedialog
#选择烧写文件对话框：
default_dir=r"C:\Users\Inker\Desktop";#r表示后面是一个原始字符串
def BinPath():
    # 直接使用askopenfilename 会出现一个未响应的TK窗口 解决方法:创建一个窗口 再隐藏
    root = tkinter.Tk();
    root.withdraw();
    fpos = tkinter.filedialog.askopenfilename(title=u'Open File',initialdir=(os.path.expanduser((default_dir))));
    return fpos;

def ComYmodemTx():
    fpos = BinPath();
    if(fpos==''):#取消选择文件 直接结束下载
        return ;

    ComSend('inker'); # 回车
    time.sleep(0.5);
    ComSend('inker'); # 登录口令
    time.sleep(0.5);
    ComSend('iap');   # 烧写命令
    time.sleep(0.5);
    ComSend('1',0);   # 选择烧写程序
    time.sleep(0.5);
    #ComSend('a',0);
    #ComSend('2',0);
    
    Com.ComDll.sio_FtYmodemTx(Com.GetComNum(),fpos.encode('ascii'), ccb, 27);
    print();
    
#####################
Com = cCom(prf=0,com=4);

def ComCmd(incmd):
    return Com.sComCmd(incmd);

def ComSend(txd,Enter=1):
    # 命令是否要追加回车
    if(Enter):    
        txd = txd + '\r';
    txd = txd.encode('utf-8');
    Com.ComTxd(txd);

def ComSendHex(txd):
    Com.ComTxd(txd);

def ComRxdMode(mode):
    Com.sSetRxdMode(mode);
def isComRxdMode():
    return Com.sGetRxdMode();
    
def ComRxdBuf():
    return Com.sGetRxdBuf();

def ComSaveFile():
    return Com.sComSaveFile();
    
def PrjF_10mS_Com():
    Com.sPrjF_10mS_Com();    
    
########################### Test Com.py
if __name__ == '__main__':
    Com.SetComNum(6);
    Com.ComConnect();
    while True:
        inkey = input();
        Com.ComTxd(inkey);
        
    
