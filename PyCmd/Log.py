
# -*- coding: utf-8 -*-

import logging  # 引入logging模块
import os
import time

def ClearNullFile(path):
    files = os.listdir(path);  # 获取路径下的子文件(夹)列表    
    for file in files: 
        if os.path.isfile(path+file):  # 如果是文件 
            if os.path.getsize(path+file) == 0:  # 文件大小为0     
                os.remove(path+file)  # 删除这个文件    

class cLog(object):
    def __init__(self,prf=0):
    
        # 调用外部包 模块

        # 连接

        # 日志输出-文件
        # 第一步，创建一个logger
        self.logger = logging.getLogger();
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        log_path = os.path.dirname(os.getcwd()) + '/Logs/';

        # 判断logs文件夹是否存在，不存在则创建
        if not os.path.exists(log_path):
            os.makedirs(log_path);
            
        # 清除空日志文件
        ClearNullFile(log_path);
        
        log_name = log_path + rq + '.log'
        logfile = log_name
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)12s[line:%(lineno)5d] - %(levelname)8s: %(message)s")
        fh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
        
        #日志输出-控制台
        self.Console = 0;
        self.Level   = 0;
        self.sLogLevel(self.Level);

        
        
    def sLogMsg(self):
        print("LastEdit:2018/11/08");
        if(self.Console == 0):
            print("ConsoleLog:Close");
        else:    
            print("ConsoleLog:Open Level:%d"%(self.Level));

        
    def sLogLevel(self,level):
        self.Level = level;
        if(self.Level == 0):
            self.logger.removeHandler(self.Console);
            self.Console = 0;
            return 0;

        if(self.Console == 0):
            self.Console = logging.StreamHandler();
            formatter = logging.Formatter("%(filename)s[%(lineno)d]-%(levelname)s:%(message)s")
            self.Console.setFormatter(formatter);
            self.logger.addHandler(self.Console);
            
        if(self.Level == 1):
            self.Console.setLevel(logging.CRITICAL);# 输出到console的log等级的开关
        if(self.Level == 2):
            self.Console.setLevel(logging.ERROR);
        if(self.Level == 3):
            self.Console.setLevel(logging.WARNING);
        if(self.Level == 4):
            self.Console.setLevel(logging.INFO);
        if(self.Level == 5):
            self.Console.setLevel(logging.DEBUG);      
        
    def sLogCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .Log');
            return False;

        if(cmdlist[0] == '.log'):
           #print("------------- .. RW ------------");
            print("  LogMsg     .. R- Log Message");
            print("  LogLevel   .. -W Log Level 0close 1C 2E 3W 4I 5D <0~5>");
            return True;

        if(cmdlist[0] == 'logmsg'):
            self.sLogMsg();
            return True;

        if(cmdlist[0] == 'loglevel'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sLogLevel(int(cmdlist[1]));
                print('LogLevel <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        return False;

# 实例化类
Log = cLog(prf=0);
# Log.logger.debug();
# Log.logger.info();
# Log.logger.warning();
# Log.logger.error(e,exc_info=True);
# Log.logger.critical();

# 外调接口
def LogCmd(incmd):
    return Log.sLogCmd(incmd);
    