# -*- coding: utf-8 -*-

class cConfig(object):
    def __init__(self):

        # �����ⲿ�� ģ��
        import os.path
        import configparser    
        
        self.filepath = os.path.dirname(os.getcwd()) + '/bin/' + "config.ini";
        self.config   = configparser.ConfigParser();
        self.config.read(self.filepath);
 
    def sConfigMsg(self):
        print("LastEdit:2018/11/05");
        print(self.config.sections());
        
    def sConfigGet(self,Section,Option,DefaultVal):
        StoreFloag = 1;
        if(self.config.has_section(Section) == False):#������� �������
            self.config.add_section(Section); #Add Section
            StoreFloag = 1;

        if(self.config.has_option(Section,Option) == False):# �粻���� ����Ӳ�����Ĭ��ֵ
            self.config.set(Section,Option,DefaultVal);
            StoreFloag = 1;

        # ���޸� �򱣴��ļ��޸�
        if(StoreFloag):
            self.config.write(open(self.filepath, 'w'));
            
        return self.config[Section][Option];
        
    def sConfigSet(self,Section,Option,Val):
        self.config.set(Section,Option,Val);
        self.config.write(open(self.filepath, 'w'));
        
    def sConfigCmd(self,incmd):
        # �ո�����и�
        cmdlist = incmd.split();
        
        if(cmdlist[0] == 'help'):
            print('  .Config');
            return False;

        if(cmdlist[0] == '.config'):
           #print("------------- .. RW ------------");
            print("  ConfigMsg   .. R- Config Message");
            return True;

        if(cmdlist[0] == 'configmsg'):
            self.sConfigMsg();
            return True;
  
        return False;

# ʵ������
Config = cConfig();
# ����ӿ�
def ConfigCmd(incmd):
    return Config.sConfigCmd(incmd);

def GetConfig(Section,Option,DefaultVal):
    return Config.sConfigGet(Section,Option,DefaultVal);

def SetConfig(Section,Option,Val):
    Config.sConfigSet(Section,Option,Val);
    