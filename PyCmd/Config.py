# -*- coding: utf-8 -*-

import configparser
# 重写配置 ConfigParser配置option的大小写问题
class NewConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr
        
class cConfig(object):
    def __init__(self):

        # 调用外部包 模块
        import os.path  
        
        self.filepath = os.path.dirname(os.getcwd()) + "\config.ini";
        self.config   = NewConfigParser();
        self.config.read(self.filepath);
 
    def sConfigMsg(self):
        print("LastEdit:2018/11/27");
        print("FileDir :%s"%(self.filepath));
        Slist = self.config.sections();
        for slst in Slist:
            print("[%s]"%(slst));
            Olist = self.config.options(slst);
            for olst in Olist:
                print("%s = %s"%(olst,self.config.get(slst, olst)));
            print();
            
    def sConfigGet(self,Section,Option,DefaultVal):
        StoreFloag = 1;
        if(self.config.has_section(Section) == False):#如果不存 则添加组
            self.config.add_section(Section); # Add Section
            StoreFloag = 1;

        if(self.config.has_option(Section,Option) == False):# 如不存在 则添加并下载默认值
            self.config.set(Section,Option,DefaultVal);
            StoreFloag = 1;

        # 有修改 则保存文件修改
        if(StoreFloag):
            self.config.write(open(self.filepath, 'w'));
            
        return self.config[Section][Option];
        
    def sConfigSet(self,Section,Option,Val):
        self.config.set(Section,Option,Val);
        self.config.write(open(self.filepath, 'w'));
        
    def sConfigCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .Config');
            return False;

        if(cmdlist[0] == '.config'):
           #print("------------- .. RW ------------");
            print("  ConfigMsg   .. R- Config Message");
            print("  Config      .. R- Config [Section] [Option]");
            return True;

        if(cmdlist[0] == 'configmsg'):
            self.sConfigMsg();
            return True;

        if(cmdlist[0] == 'config'):
            if(len(cmdlist) == 1):
                print(self.config.sections());
                return True;
            if(len(cmdlist) == 2):
                if(self.config.has_section(cmdlist[1]) == False):# 不存在
                    return True;
                print(self.config.options(cmdlist[1]));
                return True;
            if(len(cmdlist) == 3):
                if(self.config.has_option(cmdlist[1],cmdlist[2]) == False):# 不存在
                    return False;
                print(self.config.get(cmdlist[1],cmdlist[2]));
                return True;
                
        return False;

# 实例化类
Config = cConfig();
# 外调接口
def ConfigCmd(incmd):
    return Config.sConfigCmd(incmd);

def GetConfig(Section,Option,DefaultVal):
    return Config.sConfigGet(Section,Option,DefaultVal);

def SetConfig(Section,Option,Val):
    Config.sConfigSet(Section,Option,Val);
    