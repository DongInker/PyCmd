# -*- coding: utf-8 -*-

import re
import os.path
import time
from pylab import plot,ion,subplot,figure,grid,pause,show,close,clf
from pylab import title,xlabel,ylabel,xlim,ylim,legend
from format    import isFloatType;
from Log import Log;
from Com import ComSaveFile;

'''
# 特殊字符需要前面加\  . ^ $ * + ? { } [ ] \ | ( )
# | 多个表达式或关系
# ^ 开始 $ 结束
# ? 匹配一次或零次
# + 匹配一次或多次
# * 匹配零次或多次
# \d* 匹配零次或多次数字
# \w* 匹配零次或多次数字大小字母[A-Za-z0-9_]
# \.? 匹配一次或零次小数点
# x.x | .x | x.
'''

#buf = re.sub('\r\n', '',buf); #删除字符串buf \r\n
class cPlotRe(object):
    def __init__(self):
    
        # 调用外部包 模块

        # 连接
        self.Cnt10mS    = 0;
        self.WaveBuf    = [];

        self.ComfileSize = 0;
        
        self.PlotReStr = '';
        self.PlotReEn  = 0;
        self.PlotPosS  = 0;

        #创建波形记录文件路径
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.dirname(os.getcwd()) + '/Logs/';
        self.wave_name = path + rq + 'wave.txt';

        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.PrfClass  = int(GetConfig('PlotRe', 'PrfClass','0'));
        self.PlotReV   = int(GetConfig('PlotRe', 'PlotReV', '0'));
        self.PlotReL   =     GetConfig('PlotRe', 'PlotReL', '\(');
        self.PlotReR   =     GetConfig('PlotRe', 'PlotReR', '\)'); 

    def sPlotReSetCfg(self):
        self.SetConfig('PlotRe', 'PrfClass', str(self.PrfClass));
        self.SetConfig('PlotRe', 'PlotReV',  str(self.PlotReV));        
        self.SetConfig('PlotRe', 'PlotReL',      self.PlotReL);
        self.SetConfig('PlotRe', 'PlotReR',      self.PlotReR);
        
    def sPlotReMsg(self):
        print("LastEdit :2018/11/05");
        print("PrfClass :%d"%(self.PrfClass));
        print("Cnt10mS  :%d"%(self.Cnt10mS));
        print("PlotReEn :%d"%(self.PlotReEn));
        print("PlotReV  :(%d)%s"%(self.PlotReV,self.PlotReV and "Hex" or "Float"));
        print("PlotReL  :%s"%(self.PlotReL));
        print("PlotReR  :%s"%(self.PlotReR));
        
    def sPlotRePrf(self,PrfClass):
        self.PrfClass = PrfClass;
        self.sPlotReSetCfg();

    def sPlotReL(self,strl):
        self.PlotReL = strl;
        self.sPlotReSetCfg();
        
    def sPlotReR(self,strr):
        self.PlotReR = strr;
        self.sPlotReSetCfg();
        
    def sPlotReV(self,mode):
        self.PlotReV = mode;
        self.sPlotReSetCfg();

    def sPlotReEn(self,en):
        self.PlotReEn = en;
        if(self.PlotReEn == 0):
            close();#关闭窗口
            #写入 XXXXmbs.txt 文件
            if(len(self.WaveBuf)):
                buf = 'wave=[';
                for i in self.WaveBuf:
                    buf += "%f,"%(i);
                buf += ']\r\n';

                with open(self.wave_name,'a',encoding='utf-8') as f:
                    f.write(buf);
                #f=open(self.wave_name,'a');
                #f.write(buf);
                #f.close();
        
        if(self.PlotReEn == 1):
            #写入 XXXXmbs.txt 文件
            if(len(self.WaveBuf)):
                buf = 'wave=[';
                for i in self.WaveBuf:
                    buf += "%f,"%(i);
                buf += ']\r\n';

                with open(self.wave_name,'a',encoding='utf-8') as f:
                    f.write(buf);

            with open(ComSaveFile(),encoding='utf-8') as f:
                data = f.read();
            self.PlotPosS = len(data); 
            #print("%d"%(self.PlotPosS));
        
    def sPlotReAdd(self,val):
        self.WaveBuf.append(val);
        clf();#清除之前画的数据
        plot(self.WaveBuf);
        plot(self.WaveBuf,'r.',label='max:%f\nmin :%f'%(max(self.WaveBuf),min(self.WaveBuf)));
        grid(True);#显示网格
        legend();#显示浮动窗口
        pause(0.001);#画布停留活动时间
        
    def sPrjF_10mS_PlotRe(self):
        self.Cnt10mS += 1;
            
    def sPrjB_10mS_PlotRe(self):   
        if(self.PlotReEn == 0):
            return 0;
            
        flen = os.path.getsize(ComSaveFile())
        if(self.ComfileSize != flen):
            self.ComfileSize = flen;
            self.WaveBuf     = [];

            with open(ComSaveFile(),encoding='utf-8') as f:
                data = f.read();
            #f = open(ComSaveFile());
            #data = f.read();
            #f.close();
            #print("%d %d"%(len(data),self.PlotPosS));
            data = data[self.PlotPosS:];
            #print("%d"%(len(data)));

            if(self.PlotReV):
                self.WaveBuf   = [];
                self.PlotReStr = ".*" + self.PlotReL + "([0X]?[0-9a-fA-F]\w*)" + self.PlotReR;
                iter = re.finditer(self.PlotReStr,data);
                for i in iter:
                    # 数据接收0X 0x 一半的数据最后字符为X x不处理
                    if((i.group(1)[-1]=="x") | (i.group(1)[-1]=="X")):
                        return False;

                    self.WaveBuf.append(int(i.group(1),16));
            else:
                self.WaveBuf    = [];
                self.PlotReStr = ".*" + self.PlotReL + "([-+]?[0-9]\d*\.?[0-9]\d*|[-+]?\.?[0-9]\d*|[-+]?[0-9]\d*\.?)" + self.PlotReR;
                iter = re.finditer(self.PlotReStr,data);
                for i in iter:
                    self.WaveBuf.append(float(i.group(1)));

            if(len(self.WaveBuf)):    
                clf();#清除之前画的数据
                plot(self.WaveBuf);
                plot(self.WaveBuf,'r.',label='max:%f\nmin :%f'%(max(self.WaveBuf),min(self.WaveBuf)));
                grid(True);#显示网格
                legend();#显示浮动窗口
                pause(0.001);#画布停留活动时间
    
    def sPlotReCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .PlotRe');
            return False;

        if(cmdlist[0] == '.plotre'):
           #print("------------- .. RW ------------");
            print("  PlotReMsg   .. R- PlotRe Message");
            print("  PlotRePrf   .. -W PlotRe Printf Class <0,1>");
            print("  PlotAdd     .. -W Add Wave Data <float>");
            print("  PlotReEn    .. -W Re Plot Wave En (0close)<0,1>");
            print("  PlotReL     .. -W Re Lift  String");
            print("  PlotReR     .. -W Re Right String");
            print("  特殊字符需要前面加\  .^$*+?{}[]\|()");
            print("  PlotReV     .. -W Re Val Type 0Dec 1Hex <0,1>");
            return True;

        if(cmdlist[0] == 'plotremsg'):
            self.sPlotReMsg();
            return True;
            
        if(cmdlist[0] == 'plotreprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sPlotRePrf(int(cmdlist[1]));
                print('PlotRePrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;

        if(cmdlist[0] == 'plotadd'):
            if(len(cmdlist) == 2):
                if(isFloatType(cmdlist[1]) == True):
                    self.sPlotReAdd(float(cmdlist[1]));
                    return True;
            return False;
            
        if(cmdlist[0] == 'plotreen'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sPlotReEn(int(cmdlist[1]));
                print('PlotReEn <= {0}'.format(cmdlist[1]));
                return True;
            return False;

        # 设置正则表达式左边字符
        if(cmdlist[0] == 'plotrel'):
            if(len(cmdlist) == 1):
                self.sPlotReL('');
                print('PlotReL <= \'\'');
                return True;
            elif(len(cmdlist) >= 2):
                self.sPlotReL(incmd[len(cmdlist[0])+1:]);
                print('PlotReL <= {0}'.format(incmd[len(cmdlist[0])+1:]));
                return True;
            return False;

        # 设置正则表达式右边字符
        if(cmdlist[0] == 'plotrer'):
            if(len(cmdlist) == 1):
                self.sPlotReR('');
                print('PlotReR <= \'\'');
                return True;
            elif(len(cmdlist) >= 2):
                self.sPlotReR(incmd[len(cmdlist[0])+1:]);
                print('PlotReR <= {0}'.format(incmd[len(cmdlist[0])+1:]));
                return True;
            return False;

        if(cmdlist[0] == 'plotrev'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sPlotReV(int(cmdlist[1]));    
                print('PlotReV <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        return False;

# 实例化类
PlotRe = cPlotRe();
# 外调接口
def PlotReCmd(incmd):
    return PlotRe.sPlotReCmd(incmd);

def PrjF_10mS_PlotRe():
    PlotRe.sPrjF_10mS_PlotRe();

def PrjB_10mS_PlotRe():
    PlotRe.sPrjB_10mS_PlotRe();

########################### Test PlotRe.py
if __name__ == '__main__':

    #初始化参数
    InCmd = ".PlotRe"
    print("In Key [exit] Exit Debug!");

    #进入调试循环
    while True:
        InKey = input();

        #模拟定时任务处理
        PrjF_10mS_PlotRe();
        PrjB_10mS_PlotRe();

        #退出模块调试命令
        if(InKey == 'exit'):
            break;

        if(len(InKey.split()) != 0):#回车重复执行上次
            InCmd = InKey;
        else:
            print(InCmd);
            
        if(len(InCmd.split()) != 0):#保证输入空格不闪退
            if(PlotReCmd(InCmd) == False):
                if(InCmd.lower() != 'help'):
                    print("unknown Cmd");

        print("InCmd>>>",end="");

