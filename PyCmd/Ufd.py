
import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter import scrolledtext        # 导入滚动文本框的模块

from Log import Log;

class cUfd(object):
    def __init__(self,prf=0):

        # 调用外部包 模块
        import sys
        import serial;
        from Com import ComSend,ComYmodemTx;

        # 连接内部
        self.PrfDis     = sys.stdout.flush;# 强制打印缓存数据
        self.Serial     = serial.Serial;
        self.UfdTxdFunc = ComSend;
        self.UfdIapFunc = ComYmodemTx;
        
        self.PrfClass  = prf;
        self.UfdModeEn = 0;

        self.BtnTxtLines = 0;
        self.BtnTxdFlag  = 0;
        #self.UfdFrm = 0;

        #Cmd
        self.CmdPrj  = [];
        self.CmdNum  = [];
        self.CmdBuf  = [];
        self.CmdName = [];
        self.PrjPos  = 0;
        self.CmdPos  = 0;
        self.PrjCmd  = [];
        
    def sUfdMsg(self):
        print("PrfClass:%d"%(self.PrfClass));
        
    def sUfdPrf(self,PrfClass):
        self.PrfClass = PrfClass;

    def sSetUfdModeEn(self,en):
        self.UfdModeEn = en;
        if(en):
            print('Go to Ufd Mode!');
    def sGetUfdModeEn(self,):
        return self.UfdModeEn;
        
    def sUfdSendData(self,cmd,Enter=1):   
        self.UfdTxdFunc(cmd,Enter);
        
    def sUfdIap(self):
        self.UfdIapFunc();

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
        f=open(fpath,'r',encoding='utf-8');
        lines = f.readlines();
        f.close();

        self.CmdPrj  = [];
        self.CmdNum  = [];
        self.CmdBuf  = [];
        self.CmdName = [];

        num = 0;
        for data in lines:
            pos = self.sindex_of_str(data,'Z:\"');
            if(pos == None):
                continue;
            if(pos >= 0):
                pattern = re.compile(r"Z:\"(\S+)\"=([0-9a-fA-F]\w*)");
                match = pattern.match(data);
                if match:
                    self.CmdPrj.append(match.group(1));
                    self.CmdNum.append(num);#存上一组命令个数
                    num = 0;
                    #print(match.group(1),int(match.group(2), 16))

            if(pos == -1):
                #data = data.replace("\\r\\n","");#去除命令间的换行
                pattern = re.compile(" SEND,([\s\S]*?),(\S+),,,");
                match = pattern.match(data);
                if match:
                    num += 1;
                    cmdbuf = match.group(1);
                    cmdbuf = cmdbuf.replace("\\r\\n","\r\n");# 将 \\ 替换为 \
                    cmdbuf = cmdbuf.replace("\\\\","\\");# 将 \\ 替换为 \
                    self.CmdBuf.append(cmdbuf);
                    self.CmdName.append(match.group(2));
        self.CmdNum.append(num);#最后一组
        
    def sUfdButtonCfg(self):
        try:
            f=open(os.getcwd()+"\\ButtonBarV3.ini",'r',encoding='utf-8');
            self.BtnTxtLines = '';
            self.BtnTxtLines = f.readlines();
            f.close();
            self.BtnTxdFlag = 1;
            print(self.BtnTxtLines[0],end='');
            print(self.BtnTxtLines[1],end='');
            print(self.BtnTxtLines[2],end='');
            print(self.BtnTxtLines[3],end='');
            print(self.BtnTxtLines[4],end='');
            print(self.BtnTxtLines[5],end='');
        except Exception as e:
            Log.logger.error(e);
            
    def sGroupLstBoxMsg(self,event):
        print(self.GroupLstBox.get());
        print(self.GroupLstBox.current());

        self.PrjPos  = self.GroupLstBox.current();
        self.CmdPos  = sum(self.CmdNum[0:self.PrjPos+1]);
        
        self.PrjCmd  = self.CmdName[self.CmdPos:self.CmdPos+self.CmdNum[self.PrjPos+1]];
        self.CmdNameLstBox["values"] = self.PrjCmd;
        self.CmdNameLstBox.current(0);
        
        self.cmdscr.delete(1.0, END) # 使用 delete
        self.cmdscr.insert(END,self.CmdBuf[self.CmdPos+self.CmdNameLstBox.current()]);
        return 0;

    def sCmdNameLstBoxMsg(self,event):
        self.cmdscr.delete(1.0, END) # 使用 delete
        self.cmdscr.insert(END,self.CmdBuf[self.CmdPos+self.CmdNameLstBox.current()]);
        return 0;
        
    def sUfdBtnSend(self):
        #print("sUfdBtnSend");
        #print(self.cmdscr.get("0.0", "end"));
        #self.cmdscr.delete(1.0, END) # 使用 delete 全部
        #self.cmdscr.insert(END,self.CmdBuf[self.CmdPos+self.CmdNameLstBox.current()]);
        
        #覆盖之前命令值
        #self.CmdBuf[self.CmdPos+self.CmdNameLstBox.current()] = self.cmdscr.get("0.0", "end").strip();
        self.CmdBuf[self.CmdPos+self.CmdNameLstBox.current()] = self.cmdscr.get("0.0", "end");
        sendstr = self.CmdBuf[self.CmdPos+self.CmdNameLstBox.current()];
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

        self.sUfdBtnReadCfg();
        
        
        #窗体对象.bind(事件类型，回调函数)
        #<Button-1>:左键单击
        #<Button-2>:中键单击
        #<Button-3>:右键单击
        #<KeyPress-A>:A键被按下，其中的A可以换成其它键位
        #<Control-V>:CTL 和V键被同时按下，V可以换成其它键位
        #<F1>：按下F1,fn系列可以随意换

        # 滚动文本框
        scrolW = 36 # 设置文本框的长度
        scrolH = 6 # 设置文本框的高度
        self.cmdscr = scrolledtext.ScrolledText(self.UfdFrm,width=scrolW, height=scrolH);
        self.cmdscr.grid(row = 2,rowspan=3,column=0, columnspan=3);# columnspan 个人理解是将3列合并成一列
        #self.cmdscr.insert(END,"prjprf 1\\r\r\nad7606prf 1\\r\r\nautogainprf 1\\r");
        
        # Button
        self.BtnSend = Button(self.UfdFrm,text = "发送",width=8,command = self.sUfdBtnSend);
        self.BtnSend.grid(row = 1,rowspan=1,column=2,sticky = E);
        #self.Btn1.grid_forget();#隐藏窗口
        
        #CmdNameLst
        self.CmdNameLstBox = ttk.Combobox(self.UfdFrm,width=14);
        self.CmdNameLstBox.grid( row=1,column=1);
        #self.CmdNameLstBox.current(0);
        self.CmdNameLstBox.bind("<<ComboboxSelected>>",self.sCmdNameLstBoxMsg);
        
        #GroupLst
        self.GroupLstBox = ttk.Combobox(self.UfdFrm,width=10,values=self.CmdPrj);
        self.GroupLstBox.grid( row=1,column=0);
        self.GroupLstBox.current(0);
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
            self.sUfdIap();
            return True;    

        if(cmdlist[0] == 'ufdgui'):
            #self.sUfdButtonCfg();
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

