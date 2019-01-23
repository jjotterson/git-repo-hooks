#!/python

import sys
import os
import subprocess 

print("\n", "****** Pre-Commit Hook ******")

print( str(sys.argv))
#print( os.path.abspath(__file__) )

#v = sys.stdin.read().split()
#proc = subprocess.Popen(["git", "rev-list", "--oneline","--first-parent" , "%s..%s" %(old, new)], stdout=subprocess.PIPE)
#commitMessage=str(proc.stdout.readlines()[0])  

#sys.stdin = open("CON", "r")
#rr = input('enter something: ')
##proc = Popen(h, stdin=sys.stdin)
#
#
#lintit = input('Commit anyway? [N/y] ')
#
#print(lintit)
#
#print('end of pre-commit')


#from tkinter import *
# 
#window = Tk()
# 
#window.title("Welcome to LikeGeeks app")
# 
#window.mainloop()

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.fontsel = "Times"
        self.Appconfigs()
        #self.create_widgets()
        self.MainContainers()
        self.TopFrame()
        self.SummaryFrame()
        self.TestFrame()
        self.DiffFrame()
     
    def Appconfigs(self,title="Repo Pre-Commit Policy"):
        self.master.title(title)
        #self.master.option_add('*Font','Times')
        #root.geometry('{}x{}'.format(950, 600))
     
    def MainContainers(self):
        #Main containers
        self.frametop  = tk.Frame(root,width=400, height=50, pady=3,padx = 1, bd=2, relief=tk.RIDGE)
        self.framesum  = tk.Frame(root,width=400, height=50, pady=3,padx = 1, bd=2, relief=tk.RIDGE)
        self.frametest = tk.Frame(root,width=400, height=50, pady=3,padx = 1, bd=2, relief=tk.RIDGE)
        self.framediff = tk.Frame(root,width=400, height=50, pady=3,padx = 1, bd=2, relief=tk.RIDGE)
        
        #layout of the main containers
        #root.grid_rowconfigure(1, weight=1)
        #root.grid_columnconfigure(0, weight=1)
        self.frametop.grid(row=0, sticky ="ew")
        self.framesum.grid(row=1, sticky ="ew")
        self.frametest.grid(row=2, sticky="ew")
        self.framediff.grid(row=3, sticky="ew")
     
    def TopFrame(self):
        #top frame widgets
        #
        #Geometry
        self.top_left  = tk.Frame(self.frametop,  width=550, height=190)
        self.top_right = tk.Frame(self.frametop,  width=550, height=190, padx=50, pady=3)
        
        self.top_left.grid(row=0, column=0, sticky="ns")
        self.top_right.grid(row=0, column=1, sticky="ns")
        #
        #Content
        tk.Label(self.top_left, text="Pre-Commit Summary", font=(self.fontsel, 20), anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=0, sticky='e')
        
        tk.Button(self.top_right, text="Exit").grid(row=0, column=1, sticky=tk.E)
        tk.Button(self.top_right, text="Commit").grid(row=0, column=2, sticky=tk.E, padx = 20, pady = 10)
        tk.Button(self.top_right, text="Commit & Push").grid(row=0, column=3, sticky=tk.E) 
      
    def SummaryFrame(self,localPath="",RemotePath="",Author="",AuthorEmail = "",CommFiles ="",Notify="",Request=""):
        #Summary frame widgets
        #Geometry
        self.sum_left  = tk.Frame(self.framesum)
        self.sum_right = tk.Frame(self.framesum, padx=50, pady=3)
        #        
        self.sum_left.grid(row=0, column=0, sticky="ns")
        self.sum_right.grid(row=0, column=1, sticky="ns")
        #left panel
        tk.Label(self.sum_left, text="Author:  ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=0, sticky='w')
        tk.Label(self.sum_left, text= Author + " <" +AuthorEmail +">",  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=1, sticky='w')
        #
        tk.Label(self.sum_left, text="Notify to: " ,  anchor = tk.W, justify = tk.LEFT, ).grid(row=1,  column=0, sticky='w')
        mailLog = tk.Entry(self.sum_left)
        mailLog.insert(0,  Notify)
        mailLog.grid(row=1,column=1,sticky='w')
        #
        tk.Label(self.sum_left, text="Request approval to: " ,  anchor = tk.W, justify = tk.LEFT, ).grid(row=2,  column=0, sticky='w')
        approvalLog = tk.Entry(self.sum_left)
        approvalLog.insert(0,  Request)
        approvalLog.grid(row=2,column=1,sticky='w')
        #
        #right panel
        tk.Label(self.sum_right, text="Remote Repo: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=0, sticky='w')
        tk.Label(self.sum_right, text= remotePath,  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=1, sticky='w')
        tk.Label(self.sum_right, text="Local Repo: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=1,  column=0, sticky='w')
        tk.Label(self.sum_right, text= localPath,  anchor = tk.W, justify = tk.LEFT, ).grid(row=1,  column=1, sticky='w')
        #botton code       
        tk.Label(self.framesum, text="Files Being Commited: " + CommFiles,  anchor = tk.W, justify = tk.LEFT ).grid(row=1,  column=0, sticky='w')
        tk.Label(self.framesum, text="Commit Message: ",  anchor = tk.W, justify = tk.LEFT ).grid(row=2,  column=0, sticky='w')
        tk.Label(self.framesum, text="Email Message: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=3,  column=0, sticky='w')
        tk.Text(self.framesum, height=3, width=70).grid(row=4, columnspan = 4) 
        
    def TestFrame(self):    
        #Testing window
        self.test_left  = tk.Frame(self.frametest)
        self.test_right = tk.Frame(self.frametest, padx=50, pady=3)
        self.test_left.columnconfigure(0, weight=1)
        self.test_right.columnconfigure(0, weight=1)
        self.test_left.grid(row=0, column=0, sticky="ns")
        self.test_right.grid(row=0, column=1, sticky="ns")
        
        tk.Label(self.test_left, text="Code Complexity: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=0, sticky='e')
        tk.Label(self.test_left, text="Run Linter: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=1,  column=0, sticky='e')
        tk.Button(self.test_left, text="OK").grid(row=1, column=1, sticky='w')
        tk.Label(self.test_left, text="Run Scenario Tools: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=2,  column=0, sticky='e')
        tk.Button(self.test_left, text="OK").grid(row=2, column=1, sticky='w')
        tk.Label(self.test_left, text="Update Doc: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=3,  column=0, sticky='e')
        tk.Button(self.test_left, text="OK").grid(row=3, column=1, sticky='w')
        
        tk.Label(self.test_right, text="Run Tests: ",  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=0, sticky='e')
        tk.Button(self.test_right, text="OK").grid(row=0, column=1, sticky='w')
    
    def DiffFrame(self,diffLog=""):    
        #Diff window
        tk.Label(self.framediff, text="Code Diff: \n \n" + diffLog,  anchor = tk.W, justify = tk.LEFT, ).grid(row=0,  column=0, sticky='e')  


#get information:
localPath = os.getcwd()
vv = subprocess.Popen('git config --get remote.origin.url', stdout = subprocess.PIPE)
remotePath = vv.stdout.read().decode('utf-8', 'replace').strip()

vv = subprocess.Popen('git config user.name', stdout = subprocess.PIPE)
Author = vv.stdout.read().decode('utf-8', 'replace').strip()

vv = subprocess.Popen('git config user.email', stdout = subprocess.PIPE)
AuthorEmail = vv.stdout.read().decode('utf-8', 'replace').strip()

##note, diff --cached because code has being staged (added) at this point.
vv = subprocess.Popen('git diff --cached --name-only', stdout = subprocess.PIPE)
CommFiles = vv.stdout.read().decode('utf-8', 'replace').strip()
CommFiles = CommFiles.replace("\n",", ")

vv = subprocess.Popen('git diff --cached', stdout = subprocess.PIPE)  
diffLog = vv.stdout.read().decode('utf-8', 'replace').strip()

#try to read the mailing list and request list - else create them (w+)
with open('.git/hooks/hooks.mailinglist','a+') as maillist, open('.git/hooks/hooks.approvallist','a+') as approvallist:
    maillist.seek(0)
    approvallist.seek(0)
    Notify = maillist.read()
    Request = approvallist.read()

#start GUI
root = tk.Tk()
app = Application(master=root)
app.SummaryFrame(localPath,remotePath,Author,AuthorEmail,CommFiles,Notify,Request)
app.DiffFrame(diffLog)

app.mainloop()





print("****** End of Pre-Commit Hook ******","\n")