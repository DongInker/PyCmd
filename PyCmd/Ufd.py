
import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import scrolledtext        # 导入滚动文本框的模块

from Log import Log;

class cUfd(object):
    def __init__(self,prf=0):

        # 调用外部包 模块
        from Com import ComSend,ComYmodemTx;

        # 连接内部
        self.UfdTxdFunc = ComSend;
        self.UfdIapFunc = ComYmodemTx;
        
        self.UfdModeEn = 0;

        #读取配置参数
        from Config import GetConfig,SetConfig;
        self.SetConfig = SetConfig;
        self.CfgPrfClass = int(GetConfig('Ufd', 'PrfClass', '0'));
        self.CfgGroPos   = int(GetConfig('Ufd', 'GrousPos', '0'));
        self.CfgCmdPos   = int(GetConfig('Ufd', 'CmdPos',   '0'));

    def sUfdSetCfg(self):
        self.SetConfig('Ufd', 'PrfClass', str(self.CfgPrfClass));
        self.SetConfig('Ufd', 'GrousPos', str(self.CfgGroPos));
        self.SetConfig('Ufd', 'CmdPos',   str(self.CfgCmdPos));

    def sUfdMsg(self):
        print("CfgPrfClass:%d"%(self.CfgPrfClass));
        print("CfgGroPos  :%d"%(self.CfgGroPos));
        print("CfgCmdPos  :%d"%(self.CfgCmdPos));
        
    def sUfdPrf(self,PrfClass):
        self.CfgPrfClass = PrfClass;
        self.sUfdSetCfg();

    def sSetUfdModeEn(self,en):
        self.UfdModeEn = en;
        if(en):
            print('Go to Ufd Mode!');

    def sGetUfdModeEn(self,):
        return self.UfdModeEn;
        
    def sUfdSendData(self,cmd,Enter=1):   
        self.UfdTxdFunc(cmd,Enter);
        
    def sUfdIap(self,mode=0):
        self.UfdIapFunc(mode);

    # UFD GUI
    def sindex_of_str(self,s1,s2):
        n1=len(s1)
        n2=len(s2)
        for i in range(n1-n2+1):
            if s1[i:i+n2]==s2:
                return i;
            else:
                return -1;
                
    def sUfdBtnReadCfg(self):
        #读取文件数据
        fpath = os.path.dirname(os.getcwd()) + "\\PyCmd\\ButtonBarV3.ini";
        with open(fpath,'r',encoding='utf-8') as f:
            lines = f.readlines();

        self.GrosName     = [];  # 产品组名称列表       [{组1名称},{组2名称},..]
        self.GrosCmdNum   = [];  # 每组产品下命令个数   [{组1个数},{组2个数},..]
        self.GrosCmdsMsg  = [];  # 命令内容             [{{组1命令1},{组1命令2},..},{{组2命令1},{组2命令2},..},..]
        self.GrosCmdsName = [];  # 命令的名称           [{{组1命令名1},{组1命令名2},..},{{组2命令名1},{组2命令名2},..},..]
        self.CmdPos       = 0;   # 命令位置临时变量

        CmdCnt = 0;
        for data in lines:
            pos = self.sindex_of_str(data,'Z:\"');
            if(pos == None):
                continue;
            if(pos >= 0):
                pattern = re.compile(r"Z:\"(\S+)\"=([0-9a-fA-F]\w*)");
                match = pattern.match(data);
                if match:
                    self.GrosName.append(match.group(1));
                    self.GrosCmdNum.append(CmdCnt);#存上一组命令个数
                    CmdCnt = 0;
                    #print(match.group(1),int(match.group(2), 16))

            if(pos == -1):
                #data = data.replace("\\r\\n","");#去除命令间的换行
                pattern = re.compile(" SEND,([\s\S]*?),(\S+),,,");
                match = pattern.match(data);
                if match:
                    CmdCnt += 1;
                    cmdbuf = match.group(1);
                    cmdbuf = cmdbuf.replace("\\r\\n","\r\n");# 将 \\ 替换为 \
                    cmdbuf = cmdbuf.replace("\\\\","\\");# 将 \\ 替换为 \
                    self.GrosCmdsMsg.append(cmdbuf);
                    self.GrosCmdsName.append(match.group(2));

        self.GrosCmdNum.append(CmdCnt);#最后一组
        self.GrosCmdNum = self.GrosCmdNum[1:];#删除未使用的第1个
        
    def sGroupLstBoxMsg(self,event):
        print(self.GroupLstBox.get());
        print(self.GroupLstBox.current());

        GroupPos    = self.GroupLstBox.current();
        self.CmdPos = sum(self.GrosCmdNum[0:GroupPos]);
        
        # 获取当前组下所以命令名称列表  {{组n命令名1},{组n命令名2},..}
        GroCmdsName  = self.GrosCmdsName[self.CmdPos:self.CmdPos+self.GrosCmdNum[GroupPos]];
        self.CmdNameLstBox["values"] = GroCmdsName;

        # 显示选择的命令名称
        if(GroupPos != self.CfgGroPos):
            self.CmdNameLstBox.current(0);
        else:
            self.CmdNameLstBox.current(self.CfgCmdPos);
        
        # 显示选择的命令内容
        #清除窗口数据
        self.cmdscr.delete(1.0, END);
        #写入窗口数据
        self.cmdscr.insert(END,self.GrosCmdsMsg[self.CmdPos+self.CmdNameLstBox.current()]);
        return 0;

    def sCmdNameLstBoxMsg(self,event):
        #清除窗口数据
        self.cmdscr.delete(1.0, END);
        #写入窗口数据
        self.cmdscr.insert(END,self.GrosCmdsMsg[self.CmdPos+self.CmdNameLstBox.current()]);
        return 0;
        
    def sUfdBtnSend(self):

        # 当按下发送事件 获取组,命令位置进行保存
        self.CfgGroPos  = self.GroupLstBox.current();
        self.CfgCmdPos  = self.CmdNameLstBox.current();
        self.sUfdSetCfg();

        #覆盖之前命令值
        #self.GrosCmdsMsg[self.CmdPos+self.CmdNameLstBox.current()] = self.cmdscr.get("0.0", "end");

        #获取命令内容进行发送 临时修改命令会发送 但不存储
        #sendstr = self.GrosCmdsMsg[self.CmdPos+self.CmdNameLstBox.current()];
        sendstr = self.cmdscr.get("0.0", "end");
        sendstr = sendstr.replace("\r\n","");# 将 \r\n 替换为 空
        sendstr = sendstr.replace("\\r\\n","\r");# 将 \\r\\n 替换为 \r
        sendstr = sendstr.replace("\\r","\r");# 将 \\r 替换为 \r
        self.sUfdSendData(sendstr,0);
        
    def sUfdGui(self):
        
        root = Tk();
        #root.wm_attributes('-topmost',1);#窗口顶层显示
        #root.geometry('250x150');

        root.title('UfdGui');

        self.UfdFrm = Frame(root);
        self.UfdFrm.pack();

        # 载入文件数据
        self.sUfdBtnReadCfg();
        
        #窗体对象.bind(事件类型，回调函数)
        #<Button-1>:左键单击
        #<Button-2>:中键单击
        #<Button-3>:右键单击
        #<KeyPress-A>:A键被按下，其中的A可以换成其它键位
        #<Control-V>:CTL 和V键被同时按下，V可以换成其它键位
        #<F1>：按下F1,fn系列可以随意换

        # 滚动文本框 命令内容
        scrolW = 36 # 设置文本框的长度
        scrolH = 6 # 设置文本框的高度
        self.cmdscr = scrolledtext.ScrolledText(self.UfdFrm,width=scrolW, height=scrolH);
        self.cmdscr.grid(row = 2,rowspan=3,column=0, columnspan=3);# columnspan 个人理解是将3列合并成一列
        #self.cmdscr.insert(END,"prjprf 1\\r\r\nad7606prf 1\\r\r\nautogainprf 1\\r");
        
        # Button 发送按键
        self.BtnSend = Button(self.UfdFrm,text = "发送",width=8,command = self.sUfdBtnSend);
        self.BtnSend.grid(row = 1,rowspan=1,column=2,sticky = E);
        #self.Btn1.grid_forget();#隐藏窗口
        
        #CmdNameLst 命令列表
        self.CmdNameLstBox = ttk.Combobox(self.UfdFrm,width=14);
        self.CmdNameLstBox.grid( row=1,column=1);
        #self.CmdNameLstBox.current(0);
        self.CmdNameLstBox.bind("<<ComboboxSelected>>",self.sCmdNameLstBoxMsg);
        
        #GroupLst 产品组列表
        self.GroupLstBox = ttk.Combobox(self.UfdFrm,width=10,values=self.GrosName);
        self.GroupLstBox.grid( row=1,column=0);
        self.GroupLstBox.current(self.CfgGroPos);
        self.GroupLstBox.bind("<<ComboboxSelected>>",self.sGroupLstBoxMsg);

        self.sGroupLstBoxMsg(0);

        root.mainloop();
        #root.destroy();
        
    #end Ufd Gui
    
    def sUfdCmd(self,incmd):
        # 空格进行切割
        cmdlist = incmd.split();
        cmdlist[0]  = cmdlist[0].lower();#命令字符串 转换小写
        
        if(cmdlist[0] == 'help'):
            print('  .Ufd');
            return False;

        if(cmdlist[0] == '.ufd'):
           #print("------------- .. RW ------------");
            print("  UfdMsg      .. R- Ufd Message");
            print("  UfdPrf      .. -W Ufd Printf Class <0,1>");
            print("  UfdMode     .. -W Go To UFD Mode");
            print("  UFD         .. -W Ufd Send Cmd <str>");
            print("  UfdIap      .. -W Ymodem Load Bin");
            print("  UfdIapC     .. -W Ymodem Load Bin in Rxd C");
            print("  UfdGui      .. -W UFD GUI");
            return True;

        if(cmdlist[0] == 'ufdmsg'):
            self.sUfdMsg();
            return True;
            
        if(cmdlist[0] == 'ufdprf'):
            if(len(cmdlist) == 2):
                if(cmdlist[1].isdigit() == False):#不是数字直接结束
                    return False;
                self.sUfdPrf(int(cmdlist[1]));
                print('UfdPrf <= {0}'.format(cmdlist[1]));
                return True;
            return False;
            
        if(cmdlist[0] == 'ufdmode'):
            self.sSetUfdModeEn(1);
            return True;

        # python模式直接发送命令到串口
        if(cmdlist[0] == 'ufd'):
            if(len(cmdlist) >= 2):
                self.sUfdSendData(incmd[4:]);#去掉前面 UFD 4个字符
                return True;
                
        # 升级单片机程序
        if(cmdlist[0] == 'ufdiap'):
            self.sUfdIap(0);
            return True;    

        # 已经进入ymodem模式使用升级程序
        if(cmdlist[0] == 'ufdiapc'):
            self.sUfdIap(1);
            return True;    

        if(cmdlist[0] == 'ufdgui'):
            self.sUfdGui();
            return True;
            
        return False;

# 实例化类
Ufd = cUfd(prf=0);
# 外调接口
def UfdCmd(incmd):
    return Ufd.sUfdCmd(incmd);

def isUfdMode():
    return Ufd.sGetUfdModeEn();

def UfdSetMode(en):
    Ufd.sSetUfdModeEn(en);
    
def UfdTxd(data,Enter=1):
    Ufd.sUfdSendData(data,Enter);

########################### Test Ufd.py
if __name__ == '__main__':

    #初始化参数
    InCmd = ".Ufd"
    print("In Key [exit] Exit Debug!");

    #进入调试循环
    while True:
        InKey = input();

        #模拟定时任务处理

        #退出模块调试命令
        if(InKey == 'exit'):
            break;

        if(len(InKey.split()) != 0):#回车重复执行上次
            InCmd = InKey;
        else:
            print(InCmd);
            
        if(len(InCmd.split()) != 0):#保证输入空格不闪退
            if(UfdCmd(InCmd) == False):
                if(InCmd.lower() != 'help'):
                    print("unknown Cmd");

        print("InCmd>>>",end="");

