
class cAutoTxd(object):
    def __init__(self,prf=0):
    
        from Ufd import UfdTxd;

        # 调用外部发送函数
        self.TxdFunc   = UfdTxd;
        
        self.Cnt10mS   = 0;
        self.AutoTxdEn = 0 ;
        self.TxdCmd    = 'help';
        
        #读取配置参数
        self.sAutoTxdGetCfg();
        
    def sAutoTxdGetCfg(self):
        import os.path
        import configparser
        self.filepath = os.path.dirname(os.getcwd()) + '/bin/' + "config.ini";
        self.config   = configparser.ConfigParser();
        self.config.read(self.filepath);
        if(self.config.has_section('AutoTxd') == False):#如果不存下载默认值
            self.config.add_section('AutoTxd'); #Add Section
            self.config.set('AutoTxd', 'PrfClass',   '0');
            self.config.set('AutoTxd', 'AutoTxdTim', '100');
            self.config.write(open(self.filepath, 'w'));

        # 读取配置文件参数值
        self.PrfClass  = int(self.config['AutoTxd']['PrfClass']);
        self.Time10mS  = int(self.config['AutoTxd']['AutoTxdTim']);
        
    def sAutoTxdSetCfg(self):
        self.config.set('AutoTxd', 'PrfClass',   str(self.PrfClass));
        self.config.set('AutoTxd', 'AutoTxdTim', str(self.Time10mS));
        self.config.write(open(self.filepath, 'w'));        
        
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
            self.TxdFunc(self.TxdCmd);
            
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
            if(cmdlist[1]):
                self.sSetAutoTxdEn(1);
                self.sSetAtuoTxdCmd(incmd[len(cmdlist[0])+1:]);
                print('AutoCmd <= {0}'.format(incmd[len(cmdlist[0])+1:]));
                return True;
            return False;
            
        return False;

# 实例化类
AutoTxd = cAutoTxd(prf=0);
# 外调接口
def AutoTxdCmd(incmd):
    return AutoTxd.sAutoTxdCmd(incmd);

def SetAutoTxdEn(en):
    AutoTxd.sSetAutoTxdEn(en);
    
def PrjB_10mS_AutoTxd():
    AutoTxd.sAutoTxd_10mS();

