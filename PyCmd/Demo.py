# -*- coding: utf-8 -*-

class cDemo(object):
    def __init__(self):
    
        # 调用外部包 模块

        # 连接

        self.PrjFCnt10mS = 0;
        self.PrjBCnt10mS = 0;

        #读取配置参数
        self.sDemoGetCfg();
        
    def sDemoGetCfg(self):
        #配置文件
        import os.path
        import configparser
        self.filepath = os.path.dirname(os.getcwd()) + '/bin/' + "config.ini";
        self.config   = configparser.ConfigParser();
        self.config.read(self.filepath);
        if(self.config.has_section('Demo') == False):#如果不存下载默认值
            self.config.add_section('Demo'); #Add Section
            self.config.set('Demo', 'PrfClass', '0');
            self.config.write(open(self.filepath, 'w'));
            
        self.PrfClass  = int(self.config['Demo']['PrfClass']);
        
    def sDemoSetCfg(self):
        self.config.set('Demo', 'PrfClass', str(self.PrfClass));
        self.config.write(open(self.filepath, 'w'));
        
    def sDemoMsg(self):
        print("LastEdit:2018/11/05");
        print("PrfClass:%d"%(self.PrfClass));
        print("PrjFCnt10mS :%d"%(self.PrjFCnt10mS));
        print("PrjBCnt10mS :%d"%(self.PrjBCnt10mS));
        print("PrjF - PrjB =%d"%(self.PrjFCnt10mS-self.PrjBCnt10mS));
        
    def sDemoPrf(self,PrfClass):
        self.PrfClass = PrfClass;
        self.sDemoSetCfg();
        
    def sPrjF_10mS_Demo(self):
        self.PrjFCnt10mS += 1;
        
    def sPrjB_10mS_Demo(self):
        self.PrjBCnt10mS += 1;

    def sDemoCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        
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
                self.sDemoPrf(int(cmdlist[1]));
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
    