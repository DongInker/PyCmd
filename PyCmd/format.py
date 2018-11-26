# -*- coding: utf-8 -*-
import ctypes

class cFormat(object):
    def __init__(self,prf=0):
    
        # 调用外部包 模块

        # 连接
        
        self.PrfClass = prf;
        
    def sFormatMsg(self):
        print("LastEdit:2018/11/05");
        print("PrfClass:%d"%(self.PrfClass));
        
    def sFormatPrf(self,PrfClass):
        self.PrfClass = PrfClass;
        
    #十六进制转浮点
    def h2f(self,s):
        cp = ctypes.pointer(ctypes.c_ulong(s))
        fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_float))
        return fp.contents.value
    
    #浮点转十六进制
    def f2h(self,s):
        fp = ctypes.pointer(ctypes.c_float(s))
        cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_ulong))
        return hex(cp.contents.value);
        
    def sFormatCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        
        if(cmdlist[0] == 'help'):
            print('  .Format');
            return False;

        if(cmdlist[0] == '.format'):
           #print("------------- .. RW ------------");
            print("  FormatMsg   .. R- Format Message");
            print("  FormatPrf   .. -W Format Printf Class <0,1>");
            print("  h2f         .. -W 3F800000 => 1.0");
            print("  f2h         .. -W 1.0 => 0x3F800000");
            return True;

        if(cmdlist[0] == 'formatmsg'):
            self.sFormatMsg();
            return True;
            
        if(cmdlist[0] == 'formatprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sFormatPrf(int(cmdlist[1]));
                print('FormatPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        if(cmdlist[0] == 'f2h'):
            if(len(cmdlist) == 2):
                if(isFloatType(cmdlist[1]) == True):
                    print(self.f2h(float(cmdlist[1])))
                    return True;
            return False;    

        if(cmdlist[0] == 'h2f'):
            if(len(cmdlist) == 2):
                if(isHexType(cmdlist[1]) == True):
                    print(self.h2f(int(cmdlist[1],16)));
                    return True; 
        return False;

# 实例化类
Format = cFormat(prf=0);
# 外调接口
def FormatCmd(incmd):
    return Format.sFormatCmd(incmd);


import re

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

#buf = re.sub('\r\n', '',buf); #删除字符串buf \r\n


#判读字符是否为数字(正负数 浮点数)
def isFloatType(num):
    pattern = re.compile(r'^[-+]?[0-9]\d*\.?[0-9]\d*|[-+]?\.?[0-9]\d*|[-+]?[0-9]\d*\.?$')
    result = pattern.match(num)
    if result:
        return True;
    else:
        return False;

def isUintType(num):
    pattern = re.compile(r'^[+]?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True;
    else:
        return False;
        
def isIntType(num):
    pattern = re.compile(r'^[-+]?[0-9]\d*$')
    result = pattern.match(num)
    if result:
        return True;
    else:
        return False;

def isHexType(num):
    pattern = re.compile(r'^[0-9a-fA-F]\w*$')
    result = pattern.match(num)
    if result:
        return True;
    else:
        return False;