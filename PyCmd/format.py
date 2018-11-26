# -*- coding: utf-8 -*-
import ctypes

class cFormat(object):
    def __init__(self,prf=0):
    
        # �����ⲿ�� ģ��

        # ����
        
        self.PrfClass = prf;
        
    def sFormatMsg(self):
        print("LastEdit:2018/11/05");
        print("PrfClass:%d"%(self.PrfClass));
        
    def sFormatPrf(self,PrfClass):
        self.PrfClass = PrfClass;
        
    #ʮ������ת����
    def h2f(self,s):
        cp = ctypes.pointer(ctypes.c_ulong(s))
        fp = ctypes.cast(cp, ctypes.POINTER(ctypes.c_float))
        return fp.contents.value
    
    #����תʮ������
    def f2h(self,s):
        fp = ctypes.pointer(ctypes.c_float(s))
        cp = ctypes.cast(fp, ctypes.POINTER(ctypes.c_ulong))
        return hex(cp.contents.value);
        
    def sFormatCmd(self,incmd):
        # �ո�����и�
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
                if(cmdlist[1].isdigit() == False):#��������ֱ�ӽ���
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

# ʵ������
Format = cFormat(prf=0);
# ����ӿ�
def FormatCmd(incmd):
    return Format.sFormatCmd(incmd);


import re

# �����ַ���Ҫǰ���\  . ^ $ * + ? { } [ ] \ | ( )
# | ������ʽ���ϵ
# ^ ��ʼ $ ����
# ? ƥ��һ�λ����
# + ƥ��һ�λ���
# * ƥ����λ���
# \d* ƥ����λ�������
# \w* ƥ����λ������ִ�С��ĸ[A-Za-z0-9_]
# \.? ƥ��һ�λ����С����
# x.x | .x | x.

#buf = re.sub('\r\n', '',buf); #ɾ���ַ���buf \r\n


#�ж��ַ��Ƿ�Ϊ����(������ ������)
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