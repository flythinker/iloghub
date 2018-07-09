#coding=utf8

import time
try:
    # python 2.x
    import Tkinter as tk
except ImportError:
    # python 3.x
    import tkinter as tk

class LogView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="连接", command=self.connectLogHub)
        filemenu.add_command(label="退出", command=root.quit)
        menubar.add_cascade(label="日志", menu=filemenu)
        root.config(menu=menubar)

        fm2 = tk.Frame(self)
        self.redisAddressInfoTxt = tk.Text(fm2, height=1, width=60)
        self.redisAddressInfoTxt.pack(side=tk.LEFT)
        tk.Button(fm2, text='Left').pack(side=tk.LEFT)
        tk.Button(fm2, text='刷新', command=self.btnRefresh).pack(side=tk.LEFT)
        fm2.pack(side=tk.TOP, padx=10)

        self.text = tk.Text(self, height=6, width=40)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.add_timestamp()
    def btnRefresh(self):
        print("btnRefresh")
    def connectLogHub(self):
        print("connectLogHub")
    def appendLog(self,lineText):
        self.text.insert("end", lineText + "\n")
        self.text.see("end")
    def add_timestamp(self):
        self.appendLog(time.ctime())
        self.after(1000, self.add_timestamp)

if __name__ == "__main__":
    root =tk.Tk()
    root.title("实时日志")
    root.geometry("600x800+500+500")
    frame = LogView(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()