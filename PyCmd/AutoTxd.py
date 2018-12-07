
class cAutoTxd(object):
    def __init__(self):
    
        from Ufd import UfdTxd;

        # 调用外部发送函数
        self.TxdFunc   = UfdTxd;
        
        self.Cnt10mS   = 0;
        self.AutoTxdEn = 0 ;
        self.TxdCmd    = 'help';
        self.TxdFlag   = 0; 
        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.PrfClass = int(GetConfig('AutoTxd', 'PrfClass',   '0'));
        self.Time10mS = int(GetConfig('AutoTxd', 'AutoTxdTim', '100'));
        
    def sAutoTxdSetCfg(self):
        self.SetConfig('AutoTxd', 'PrfClass',   str(self.PrfClass));
        self.SetConfig('AutoTxd', 'AutoTxdTim', str(self.Time10mS));      
        
    def sAutoTxdMsg(self):
        print("PrfClass   :%d"%(self.PrfClass));
        print("AutoTim1ms :%dmS"%(self.Time10mS*10));
        print("AutoTxdCmd :%s"%(self.TxdCmd));

    def sAutoTxdPrf(self,PrfClass):
        self.PrfClass = PrfClass;
        self.sAutoTxdSetCfg();
        
    def sAutoTxd_10mS(self):
        if(self.AutoTxdEn == 0):
            return False;
            
        self.Cnt10mS += 1;
        if(self.Cnt10mS >= self.Time10mS):
            self.Cnt10mS = 0;
            self.TxdFlag = 1; 
            #self.TxdFunc(self.TxdCmd);
            
    def SetAutoTime(self,time10ms):
        self.Time10mS = time10ms;
        self.sAutoTxdSetCfg();
        
    def sSetAutoTxdEn(self,en):
        self.Cnt10mS = 0;
        self.AutoTxdEn = en;

    def sSetAtuoTxdCmd(self,TxdCmd):
        self.TxdCmd = TxdCmd;
        
    def sAutoTxdCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .AutoTxd');
            return False;

        if(cmdlist[0] == '.autotxd'):
           #print("------------- .. RW ------------");
            print("  AutoTxdMsg  .. R- AutoTxd Message");
            print("  AutoTxdPrf  .. -W AutoTxd Printf Class <0,1>");
            print("  AutoTxdTim  .. -W AutoTxd Time 10mS <1,1000>");
            print("  AutoTxdCmd  .. -W AutoTxd Cmd <str>");
            
            return True;

        if(cmdlist[0] == 'autotxdmsg'):
            self.sAutoTxdMsg();
            return True;
            
        if(cmdlist[0] == 'autotxdprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sAutoTxdPrf(int(cmdlist[1]));
                print('AutoTxdPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        # 设置自动命令执行时间
        if(cmdlist[0] == 'autotxdtim'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.SetAutoTime(int(cmdlist[1]));
                print('AutoTxdTim <= {0}'.format(cmdlist[1]));
                return True;
            return False;

        # 设置自动命令
        if(cmdlist[0] == 'autotxdcmd'):
            if(len(cmdlist) >= 2):
                self.sSetAutoTxdEn(1);
                self.sSetAtuoTxdCmd(incmd[len(cmdlist[0])+1:]);
                print('AutoCmd <= {0}'.format(incmd[len(cmdlist[0])+1:]));
                return True;
            return False;
            
        return False;

# 实例化类
AutoTxd = cAutoTxd();
# 外调接口
def AutoTxdCmd(incmd):
    return AutoTxd.sAutoTxdCmd(incmd);

def SetAutoTxdEn(en):
    AutoTxd.sSetAutoTxdEn(en);
    
def isAutoTxdFlag():
    flag = AutoTxd.TxdFlag;
    AutoTxd.TxdFlag = 0;
    return flag;

def GetAutoTxdCmd():
    return AutoTxd.TxdCmd;

def PrjB_10mS_AutoTxd():
    AutoTxd.sAutoTxd_10mS();

