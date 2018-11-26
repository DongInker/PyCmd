fpath = "E:\\InkerSys\\SoftwareCfg\\Python\\Project\\PyCmd\\PyCmd\\ButtonBarV3.ini";
f=open(fpath,'r',encoding='utf-8');
lines = f.readlines();
f.close();


def GetG(lines):
    strs = 'Z:\"';
    stre = '\"';
    Gnum = 0;
    for data in lines:
        try:
            spos  = data.index(strs);#搜索strs字符坐标
            spos += len(strs);       #获取strs字符字后的坐标

            data  = data[spos:];      #截取strs字后的字符串
            epos  = data.index(stre); #搜索stre字符坐标
            GName = data[0:epos];
            
            GNum  = int(data[epos+2:],16);
            print(GName,GNum);
        except:
            print(data,end='');


def index_of_str(s1, s2):
    n1=len(s1)
    n2=len(s2)
    for i in range(n1-n2+1):
        if s1[i:i+n2]==s2:
            return i;
        else:
            return -1;

import re
def GetG1(lines):
    for data in lines:
        pos = index_of_str(data,'Z:\"');
        if(pos == None):
            continue;
        if(pos >= 0):
            pattern = re.compile(r"Z:\"(\S+)\"=([0-9a-fA-F]\w*)");
            match = pattern.match(data);
            if match:
                #print(match.groups())
                print(match.group(1),int(match.group(2), 16))

        if(pos == -1):
            #data = data.replace("\\r\\n","");#去除命令间的换行
            pattern = re.compile(r" SEND,([\s\S]*?),(\S+),,,");
            match = pattern.match(data);
            if match:
                cmdbuf = match.group(1);
                #cmdbuf = cmdbuf.replace("\\\\","\\");# 将 \\ 替换为 \
                print(cmdbuf);
                cmdname = match.group(2);
                
a=[1,2,3,4,5,6,7];      
#GetG1(lines[0:30])
#GetG1(lines)                
