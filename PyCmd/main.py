
import sys
import time

##########################################################
#Time_Thread
#使用定时器慢及时间不准

import threading

class cSystem(threading.Thread):
    def __init__(self, threadID, name, time):
        threading.Thread.__init__(self,target=self.Time10mS);
        self.threadID = threadID;
        self.name     = name;
        self.time     = time;

        self.Cnt10mS = 0;
        self.sysH    = 0;
        self.sysM    = 0;
        self.sysS    = 0;

    # 定时线程 
    def Time10mS(self):
        global PrjF10mS_FuncLst;
        
        while 1:
            time.sleep(self.time);
            
            self.Cnt10mS += 1;
            if(self.Cnt10mS >= 100):
                self.Cnt10mS = 0;
                self.sysS += 1;
                
            if(self.sysS >= 60):
                self.sysS = 0;
                self.sysM+=1;
                
            if(self.sysM >= 60):
                self.sysM=0;
                self.sysH+=1;


            for PrjF10mS in PrjF10mS_FuncLst:
                PrjF10mS();  
        
    def PrfSysTime(self):
        print("PY:%02d:%02d:%02d>"%(self.sysH,self.sysM,self.sysS),end='')
        sys.stdout.flush();#强制打印缓存数据

System = cSystem(1, "Thread-1", 0.01); # Time 10mS (当为1mS时间很卡)
#end Time_Thread
##########################################################

##########################################################
#Key In Cmd

class cKeyCmd(object):
    def __init__(self):
        self.WorkMode = 0;
        self.RxdBuf   = 'help';
        self.InCmd    = '';
        
    def SysMsg(self):
        print("LastEdit:2018/11/15");
        print('CmdMode :%d'%(self.WorkMode));

    def Version(self):
        print('Version :1.01');
        print('Auther  :Inker.Dong');
        print('Time    :2018/11/27');

    def ClearDis(self):
        import os
        os.system("cls");
        
    def sSysCmd(self,incmd):
        cmd = incmd.split();# 空格进行切割
        if(cmd[0] == 'help'):
            print('  .System');
            return False;

        if(cmd[0] == '.system'):
            print("  SysMsg      .. R- System Message");
            print("  Version     .. R- Version Message");
            #print("  UfdMode     .. -W Go To UFD Mode");    # UfdMode
            print("  PyMode      .. -W Go To Python Mode");  # PythonMode
            print("  CLS         .. -W Clear Display");
            return True;

        if(cmd[0] == 'sysmsg'):
            self.SysMsg();
            return True;

        if(cmd[0] == 'version'):
            self.Version();
            return True;

        if(cmd[0] == 'cls'):
            self.ClearDis();
            return True;    

        return False;
    
    def sProB_10mS_Key(self):    
        import msvcrt
        # 无按键输入直接返回
        if(msvcrt.kbhit() == 0):
            return 0;

        # 获取按键值
        try:
            KeyVal = msvcrt.getch().decode('utf-8');
        except Exception as e:
            Log.logger.error(e);
            return 0;
            
        # 有按键输入终止自动命令
        SetAutoTxdEn(0);
        
        if(KeyVal != '\r'):
            if(isUfdMode()== 1):#UFD模式 直接发送按键值
                UfdTxd(KeyVal,0);#将输入字符直接发送到UFD串口
            else:
                print(KeyVal,end='');
            if(KeyVal == '\b'):# 输入 BackSpace 删除最后一个字符
                self.RxdBuf = self.RxdBuf[:-1];
                sys.stdout.write(' \b');# 删除显示最后一个字符
            else:
                self.RxdBuf += KeyVal;
            sys.stdout.flush();#强制打印缓存数据    
            return 0;

        # Ufd Mode
        if(isUfdMode() == 1):
            self.RxdBuf  = self.RxdBuf.lower()#将字符统一转换为小写
            if(self.RxdBuf == 'pymode'): #进入python模式命令
                UfdSetMode(0);
                self.WorkMode = 0;
                print('\nUfd Mode Go to Python Mode!');
                self.RxdBuf = 'help';
            elif(self.RxdBuf == 'iap'): #UfdMode下IAP直接升级
                from Com import ComSend,ComYmodemTx;
                UfdTxd('');       #iap之后发送一个回车
                time.sleep(0.5);  #延时一段时间 给单片机复位进入boot系统
                ComSend('1',0);   #发送1 进入Ymodem程序下载
                ComYmodemTx(1);   #直接进入Ymodem模式升级
                self.RxdBuf = '';
            else:
                UfdTxd('');
                self.RxdBuf = '';
            return 0;
            
        # Python Mode
        if(self.WorkMode == 0):
            print();

            #回车跳过直接重复执行上次命令
            if(len(self.RxdBuf)):
                self.InCmd  = self.RxdBuf;

            if(SysHelp(self.InCmd) == False):
                print("unknown Cmd");
            System.PrfSysTime();
            self.RxdBuf = '';

# 实例化类
KeyCmd = cKeyCmd();

def SysCmd(incmd):
    return KeyCmd.sSysCmd(incmd);

def PrjB_10mS_Key():
    KeyCmd.sProB_10mS_Key();
    
# end Key In Cmd
##########################################################
#调用模块函数
from Config    import ConfigCmd;
from Log       import LogCmd,Log;
from Demo      import DemoCmd,PrjF_10mS_Demo,PrjB_10mS_Demo;
from AutoTxd   import AutoTxdCmd,SetAutoTxdEn,PrjB_10mS_AutoTxd,isAutoTxdFlag,GetAutoTxdCmd;
from Com       import ComCmd,PrjF_10mS_Com;
from Ufd       import UfdCmd,isUfdMode,UfdSetMode,UfdTxd;
from MbsRtu    import MbsRtuCmd,PrjB_10mS_MbsRtu;
from format    import FormatCmd;
from PlotRe    import PlotReCmd,PrjF_10mS_PlotRe,PrjB_10mS_PlotRe;

#命令行执行函数
Cmd_FuncLst = [
SysCmd,
ConfigCmd,
LogCmd,
DemoCmd,
AutoTxdCmd,
ComCmd,
UfdCmd,
FormatCmd,
PlotReCmd,
MbsRtuCmd];

#后台定时调用函数
PrjB10mS_FuncLst = [
PrjB_10mS_Key,
PrjB_10mS_Demo,
PrjB_10mS_AutoTxd,
PrjB_10mS_PlotRe,
PrjB_10mS_MbsRtu];

#前台定时调用函数
PrjF10mS_FuncLst = [
PrjF_10mS_Com,
PrjF_10mS_PlotRe,
PrjF_10mS_Demo]; 

##########################################################
def SysHelp(InCmd):
    global Cmd_FuncLst;
                  
    if(len(InCmd.split()) == 0):#保证输入空格不闪退
        return False;
        
    for CmdFunc in Cmd_FuncLst:
        if(CmdFunc(InCmd) == True):
           return True;

    InCmd = InCmd.lower();#统一转换小写
    if(InCmd == 'help'):
        return True;
    return False;

##########################################################
#main
if __name__ == '__main__':

    IdleMode = 0;#当命令行模式错误闪退 可置1进入IDLE运行查看哪里错误
    inkey = '';
    key   = 'help';
    
    System.start();
    print('Welcome Pythone World!');
    sys.stdout.flush();#强制打印缓存数据
    while True:
        if(IdleMode == 0):
            time.sleep(0.01); 
            for PrjB10mS in PrjB10mS_FuncLst:
                PrjB10mS();
            if(isAutoTxdFlag()):
                if(SysHelp(GetAutoTxdCmd()) == False):
                    print("unknown Cmd");
        else:
            if(inkey != ''):
                key = inkey;
            if(SysHelp(key) == False):
                print("unknown Cmd");
            System.PrfSysTime();
            inkey = input();

            
