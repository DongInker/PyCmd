
import sys
import os.path
import time
import serial

from Log import Log;

ComBrtTab = {
"300"   :0X05, # #1000000_ #1500000_ #2000000_
"1200"  :0X07,
"2400"  :0X09,
"4800"  :0X0A,
"9600"  :0X0C,
"19200" :0X0D,
"38400" :0X0E,
"57600" :0X0F,
"115200":0X10,
"230400":0X11,
"460800":0X12,
"921600":0X13};

class cCom(object):
    def __init__(self,prf=0,com=3):

        # 调用外部包 模块
        import serial.tools.list_ports
        # 连接内部
        self.ComMsgFunc = serial.tools.list_ports.comports;#获取串口列表信息
        self.ser        = serial.Serial;

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
        self.BinPath   =     GetConfig('Com', 'BinPath',  r'C:\Users\Inker\Desktop');
        self.BaudRate  =     GetConfig('Com', 'Baudrate',  '115200');

        if(self.StartCon == 'open'):
            self.ComConnect();
            
    def sComSetCfg(self):
        self.SetConfig('Com', 'PrfClass',  str(self.PrfClass));
        self.SetConfig('Com', 'SerialNum', str(self.ComNum));
        self.SetConfig('Com', 'StartCon',      self.StartCon);
        self.SetConfig('Com', 'BinPath',       self.BinPath);
        self.SetConfig('Com', 'Baudrate',      self.BaudRate);
        
    def ComMsg(self):
        print("LastEdit:2018/11/20");
        print("PrfClass:%d"%(self.PrfClass));
        print("StartCon:%s"%(self.StartCon));
        print('Com Num :%d(%d)'%(self.ComNum,self.isConnected));
        print('Com Brt :%s'%(self.BaudRate));
        print('Com Cfg DataBit:%s Parity:%s StopBit:%s'%(self.DataBit,self.Parity,self.StopBit));
        
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
            self.ser.write(txd);
        
    def ComConnect(self):
        self.isConnected = False;
        try:
            self.ser = serial.Serial("com"+str(self.ComNum),int(self.BaudRate));
            self.isConnected = True;
        except Exception as e:
            print(e);
            print("打开串口失败!");
            self.ser.close();

    def ComDisconnent(self):
        if(self.isConnected == True):
            self.ser.close();
            self.isConnected = False;
        self.RxdHalfFlag = 0;
        self.RxdHalfBuf  = '';
        
    def SetComNum(self,comnum):
        # 关闭旧串口
        self.ComDisconnent();
        self.ComNum = comnum;
        # 打开新串口
        self.ComConnect();
        self.sComSetCfg();# 保存串口参数
        
    def GetComNum(self):
        return self.ComNum;
    
    def SetComBaudrate(self,baudrate):
        if baudrate in ComBrtTab:
            self.BaudRate = baudrate;
            self.ser.baudrate = int(self.BaudRate); 
            self.sComSetCfg();
            return True;
        else:
            for dict_key, dict_value in ComBrtTab.items():  
                print(dict_key);
            return False;

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
        rxdbuf = self.ser.read(self.ser.in_waiting);
        if(len(rxdbuf) <= 0):
            return 0;
        # 接收十六进制模式
        if(self.RxdMode == 1):
            self.RxdBuf = rxdbuf;
            self.RxdMode = 0;
            return 0;

        #'''
        attempts = 0;
        success  = False;
        DoneFlag = 0;
        #rxdval   = rxdbuf.value;
        rxdval   = rxdbuf;
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
            #try:
            with open(self.com_name,'a',encoding='utf-8') as f:
                f.write(rxdstr);
            #except Exception as e:
            #    Log.logger.error(e);

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
            print("  ComBR        .. -W Set Com BaudRate <9600,115200>");
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
            
        if(cmdlist[0] == 'combr'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                if(self.SetComBaudrate(cmdlist[1]) == True):
                    print('ComNum <= {0}'.format(cmdlist[1]));
                    return True;
            return False;

        if(cmdlist[0] == 'comclose'):
            self.ComDisconnent();
            print('Com{0} <= Close!'.format(self.ComNum));
            return True;
            
        if(cmdlist[0] == 'startcon'):
            if(len(cmdlist) == 2):
                self.sComStartCon(cmdlist[1]);
                print('ComStartCon <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        return False;

#选择烧写文件
import os
import tkinter,tkinter.filedialog
#选择烧写文件对话框：
def BinPath():
    # 直接使用askopenfilename 会出现一个未响应的TK窗口 解决方法:创建一个窗口 再隐藏
    root = tkinter.Tk();
    root.withdraw();
    fpos = tkinter.filedialog.askopenfilename(title=u'Open File',initialdir=(os.path.expanduser((Com.BinPath))));
    return fpos;

#####################
def getc(size):
    if(Com.ser.in_waiting != 0):#注意 发送数据后直接调用read函数会使发送数据偶尔出错 所以先判读再读
        rxd = Com.ser.read(size);
    else:
        rxd = None;
    return rxd;

def putc(data):
    return Com.ser.write(data);

def callback(FileLen,TxdLen):
    a = round(20*TxdLen/FileLen);
    b = 20-a;
    print('\r%3dkB %3dkB |%s%s| %d%%            '%(FileLen/1024,TxdLen/1024,a*'▇',b*'  ',(TxdLen/FileLen)*100),end='\r')

def ComYmodemTx(mode = 0):
    fpos = BinPath();
    if(fpos==''):#取消选择文件 直接结束下载
        return ;

    Com.BinPath = fpos;
    Com.sComSetCfg(); # 存储文件路径

    if(mode == 0):
        ComSend('ufd on'); # 回车
        time.sleep(0.5);
        ComSend('ufd on'); # 登录口令
        time.sleep(0.5);
        ComSend('iap');   # 烧写命令
        #发现单片机复位 发送管脚低电平 导致串口卡出错崩溃 复位串口卡 10MHz绕组变形板

        time.sleep(0.5);
        ComSend('1',0);   # 选择烧写程序
        time.sleep(0.5);
        #ComSend('a',0);
        #ComSend('2',0);
        Com.ser.read(Com.ser.in_waiting);

    from TxdYmodem import YMODEM
    Com.isConnected = False;#避免定时中断干扰下载过程
    stream = open(fpos,'rb');
    Ymodem = YMODEM(getc,putc);
    Ymodem.send(stream, 3, callback);
    Com.isConnected = True;
    
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
    Com.SetComNum(7);
    Com.ComConnect();
    while True:
        inkey = input();
        Com.ComTxd(inkey);
        
    
