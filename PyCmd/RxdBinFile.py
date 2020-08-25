# -*- coding: utf-8 -*-
#
# Original code by:
#    Inker.Dong <dongmaowan99@163.com>
#    Copyright 2019 Inker.Dong
#
# Subsequent changes:

__version__ = "1.0.0"

class cRxdBin(object):
    def __init__(self):
    
        # 调用外部包 模块

        # 连接

        self.PrjFCnt10mS = 0;
        self.PrjBCnt10mS = 0;

        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.CfgPrfClass = int(GetConfig('RxdBin', 'PrfClass', '0'));

    def sRxdBinSetCfg(self):
        self.SetConfig('RxdBin', 'PrfClass', str(self.CfgPrfClass));
        
    def sRxdBinMsg(self):
        print("LastEdit:2019/04/24");
        print("CfgPrfClass :%d"%(self.CfgPrfClass));
        print("PrjFCnt10mS :%d"%(self.PrjFCnt10mS));
        print("PrjBCnt10mS :%d"%(self.PrjBCnt10mS));
        print("PrjF - PrjB =%d"%(self.PrjFCnt10mS-self.PrjBCnt10mS));
        
    def sRxdBinPrf(self,PrfClass):
        self.CfgPrfClass = PrfClass;
        self.sRxdBinSetCfg();
        
    def sPrjF_10mS_RxdBin(self):
        self.PrjFCnt10mS += 1;
        
    def sPrjB_10mS_RxdBin(self):
        self.PrjBCnt10mS += 1;

    def sRxdBinCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .RxdBin');
            return False;

        if(cmdlist[0] == '.rxdbin'):
           #print("------------- .. RW ------------");
            print("  RxdBinMsg     .. R- RxdBin Message");
            print("  RxdBinPrf     .. -W RxdBin Printf Class <0,1>");
            return True;

        if(cmdlist[0] == 'rxdbinmsg'):
            self.sRxdBinMsg();
            return True;
            
        if(cmdlist[0] == 'rxdbinprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sRxdBinPrf(int(cmdlist[1]));
                print('RxdBinPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        return False;

# 实例化类
RxdBin = cRxdBin();
# 外调接口
def RxdBinCmd(incmd):
    return RxdBin.sRxdBinCmd(incmd);

def PrjF_10mS_RxdBin():
    RxdBin.sPrjF_10mS_RxdBin();
    
def PrjB_10mS_RxdBin():
    RxdBin.sPrjB_10mS_RxdBin();
    
########################### Test RxdBin.py
if __name__ == '__main__':

    #初始化参数
    InCmd = ".RxdBin"
    print("In Key [exit] Exit Debug!");

    #进入调试循环
    while True:
        InKey = input();

        #模拟定时任务处理
        PrjF_10mS_RxdBin();
        PrjB_10mS_RxdBin();

        #退出模块调试命令
        if(InKey == 'exit'):
            break;

        if(len(InKey.split()) != 0):#回车重复执行上次
            InCmd = InKey;
        else:
            print(InCmd);
            
        if(len(InCmd.split()) != 0):#保证输入空格不闪退
            if(RxdBinCmd(InCmd) == False):
                if(InCmd.lower() != 'help'):
                    print("unknown Cmd");

        print("InCmd>>>",end="");

