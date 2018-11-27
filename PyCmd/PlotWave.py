# -*- coding: utf-8 -*-

import re
import os.path
import time
from pylab import plot,ion,subplot,figure,grid,pause,show,close,clf
from pylab import title,xlabel,ylabel,xlim,ylim,legend
from format    import isFloatType;
from Log import Log;

class cPlotWave(object):
    def __init__(self):
    
        # 调用外部包 模块

        # 连接
        self.Cnt10mS    = 0;
        self.WaveBuf    = [];

        self.ComfileSize = 0;
        #创建波形记录文件路径
        rq = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        path = os.path.dirname(os.getcwd()) + '/Logs/';
        self.wave_name = path + rq + 'wave.txt';

        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.PrfClass  = int(GetConfig('PlotWave', 'PrfClass', '0'));
        self.PlotEn    = int(GetConfig('PlotWave', 'PlotEn', '0'));

    def sPlotWaveSetCfg(self):
        self.SetConfig('PlotWave', 'PrfClass', str(self.PrfClass));
        self.SetConfig('PlotWave', 'PlotEn',   str(self.PlotEn));
        
    def sPlotWaveMsg(self):
        print("LastEdit :2018/11/05");
        print("PrfClass :%d"%(self.PrfClass));
        print("Cnt10mS  :%d"%(self.Cnt10mS));
        print("PlotEn   :%d"%(self.PlotEn));
        
    def sPlotWavePrf(self,PrfClass):
        self.PrfClass = PrfClass;
        self.sPlotWaveSetCfg();

    def sPlotWaveClose(self):
        close();#关闭窗口
        
        #写入 XXXXmbs.txt 文件
        if(len(self.WaveBuf)):
            buf = 'wave=[';
            for i in self.WaveBuf:
                buf += "%f,"%(i);
            buf += ']\r\n';
            
            f=open(self.wave_name,'a');
            f.write(buf);
            f.close();
            self.WaveBuf    = [];

    def sPlotWaveEn(self,en):
        self.PlotEn = en;
        self.sPlotWaveSetCfg();
        
    def sPlotWaveAdd(self,val):
        self.WaveBuf.append(val);
        clf();#清除之前画的数据
        plot(self.WaveBuf);
        plot(self.WaveBuf,'r.',label='max:%f\nmin :%f'%(max(self.WaveBuf),min(self.WaveBuf)));
        grid(True);#显示网格
        legend();#显示浮动窗口
        pause(0.001);#画布停留活动时间
        
    def sPrjF_10mS_Plot(self):
        self.Cnt10mS += 1;
            
    def sPrjB_10mS_Plot(self):   
        if(self.PlotEn == 0):
            return 0;
            
        from Com import ComSaveFile;
        flen = os.path.getsize(ComSaveFile())
        if(self.ComfileSize != flen):
            self.ComfileSize = flen;
            self.WaveBuf    = [];
            f = open(ComSaveFile());
            data = f.read();
            f.close();

            '''
            pattern = re.compile(r".*电容值:([-+]?[0-9]\d*\.?[0-9]\d*|[-+]?\.?[0-9]\d*|[-+]?[0-9]\d*\.?)pF.*");# "*****[0] (0X1243)******"
            match = pattern.match(buf);
            if match:
                cmdbuf = match.group(1);
                self.sPlotWaveAdd(float(cmdbuf));
            '''
            
            iter = re.finditer(r".*\[0\] \(0X([0-9a-fA-F]\w*)\)",data);
            for i in iter:
                self.WaveBuf.append(int(i.group(1),16));
                
            if(len(self.WaveBuf)):    
                clf();#清除之前画的数据
                plot(self.WaveBuf);
                plot(self.WaveBuf,'r.',label='max:%f\nmin :%f'%(max(self.WaveBuf),min(self.WaveBuf)));
                grid(True);#显示网格
                legend();#显示浮动窗口
                pause(0.001);#画布停留活动时间
    
    def sPlotWaveCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .PlotWave');
            return False;

        if(cmdlist[0] == '.plotwave'):
           #print("------------- .. RW ------------");
            print("  PlotWaveMsg .. R- PlotWave Message");
            print("  PlotWavePrf .. -W PlotWave Printf Class <0,1>");
            print("  PlotEn      .. -W Plot Wave En <0,1>");
            print("  PlotAdd     .. -W Add Wave Data <float>");
            print("  PlotClose   .. -W Close Plot");
            return True;

        if(cmdlist[0] == 'plotwavemsg'):
            self.sPlotWaveMsg();
            return True;
            
        if(cmdlist[0] == 'plotwaveprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sPlotWavePrf(int(cmdlist[1]));
                print('PlotWavePrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;

        if(cmdlist[0] == 'plotadd'):
            if(len(cmdlist) == 2):
                if(isFloatType(cmdlist[1]) == True):
                    self.sPlotWaveAdd(float(cmdlist[1]));
                    return True;
            return False;  

        if(cmdlist[0] == 'plotclose'):
            self.sPlotWaveClose();
            return True;
            
        if(cmdlist[0] == 'ploten'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sPlotWaveEn(int(cmdlist[1]));
                print('PlotWaveEn <= {0}'.format(cmdlist[1]));
                return True;
            return False;
   
        return False;

# 实例化类
PlotWave = cPlotWave();
# 外调接口
def PlotWaveCmd(incmd):
    return PlotWave.sPlotWaveCmd(incmd);

def PrjF_10mS_Plot():
    PlotWave.sPrjF_10mS_Plot();

def PrjB_10mS_Plot():
    PlotWave.sPrjB_10mS_Plot();

