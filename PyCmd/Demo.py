# -*- coding: utf-8 -*-
#
# Original code by:
#    Inker.Dong <dongmaowan99@163.com>
#    Copyright 2019 Inker.Dong
#
# Subsequent changes:

__version__ = "1.0.0"

class cDemo(object):
    def __init__(self):
    
        # 调用外部包 模块

        # 连接

        self.PrjFCnt10mS  = 0;
        self.PrjBCnt10mS  = 0;

        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.CfgPrfClass = int(GetConfig('Demo', 'PrfClass', '0'));

    def sDemoSetCfg(self):
        self.SetConfig('Demo', 'PrfClass', str(self.CfgPrfClass));
        
    def sDemoMsg(self):
        print("LastEdit:2019/04/24");
        print("CfgPrfClass :%d"%(self.CfgPrfClass));
        print("PrjFCnt10mS :%d"%(self.PrjFCnt10mS));
        print("PrjBCnt10mS :%d"%(self.PrjBCnt10mS));
        print("PrjF - PrjB =%d"%(self.PrjFCnt10mS-self.PrjBCnt10mS));
        
    def sDemoSetPrf(self,PrfClass):
        self.CfgPrfClass = PrfClass;
        self.sDemoSetCfg();
        
    def sDemoPrfStr(self,prfnum,str):
        if(self.CfgPrfClass >= prfnum):
            print("Demo",prfnum,str);
    
    def sPrjF_10mS_Demo(self):
        self.PrjFCnt10mS += 1;
        
    def sPrjB_10mS_Demo(self):
        self.PrjBCnt10mS += 1;
        self.sDemoPrfStr(1,"PrjBCnt10mS: %2d"%(self.PrjBCnt10mS));
        self.sDemoPrfStr(2,"PrjBCnt10mS:%#2X"%(self.PrjBCnt10mS));

    def sDemoCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .Demo');
            return False;

        if(cmdlist[0] == '.demo'):
           #print("------------- .. RW ------------");
            print("  DemoMsg     .. R- Demo Message");
            print("  DemoPrf     .. -W Demo Printf Class <0,1>");
            return True;

        if(cmdlist[0] == 'demomsg'):
            self.sDemoMsg();
            return True;
            
        if(cmdlist[0] == 'demoprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sDemoSetPrf(int(cmdlist[1]));
                print('DemoPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        return False;

# 实例化类
Demo = cDemo();
# 外调接口
def DemoCmd(incmd):
    return Demo.sDemoCmd(incmd);

def PrjF_10mS_Demo():
    Demo.sPrjF_10mS_Demo();
    
def PrjB_10mS_Demo():
    Demo.sPrjB_10mS_Demo();
    
########################### Test Demo.py
if __name__ == '__main__':

    #初始化参数
    InCmd = ".Demo"
    print("In Key [exit] Exit Debug!");

    #进入调试循环
    while True:
        InKey = input();

        #模拟定时任务处理
        PrjF_10mS_Demo();
        PrjB_10mS_Demo();

        #退出模块调试命令
        if(InKey == 'exit'):
            break;

        if(len(InKey.split()) != 0):#回车重复执行上次
            InCmd = InKey;
        else:
            print(InCmd);
            
        if(len(InCmd.split()) != 0):#保证输入空格不闪退
            if(DemoCmd(InCmd) == False):
                if(InCmd.lower() != 'help'):
                    print("unknown Cmd");

        print("InCmd>>>",end="");

