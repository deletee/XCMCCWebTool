# -*- coding: utf-8 -*-
#coding=utf-8
loginInfo='''
################################################################################
# XToolRunner Script to register and login ZJ-CMCC Web Portal Automatically    #
# (Tested with Python 2.7)                                                     #
#                                                                              #
# @author: JingJ XI                                                            #
#                                                                              #
# @NetIP="www.baidu.com"       # use to test Internet:www.baidu.com            #
# @LoginIP="10.78.200.15"      # use to test ZJ-CMCC Web Portal:10.78.200.15   #
#                                                                              #
#              Before Run It,Please Modify IP                                  #
#                                                                              #
# @Example: python XToolRunner.py -r # start run                               #
# @Example: python XToolRunner.py -c # clear lock                              #
# @Example: python XToolRunner.py -t # terminal Thread                         #
#                                                                              #
################################################################################
'''


import urllib
import urllib2
import re
import cookielib
import time
import random
import json
import threading
import os
import sys
"""cookie"""


cookie = cookielib.CookieJar()
chandle = urllib2.HTTPCookieProcessor(cookie)
NetIP = "www.baidu.com"        # 上网的域名或者IP:www.baidu.com
LoginIP = "10.78.200.15"    # 拨号的域名或者IP:10.78.200.15

def get(url):
        r = urllib2.Request(url)
        opener = urllib2.build_opener(chandle)
        u = opener.open(r,timeout=3)
        data = u.read()
        return data

def post(url, data):
        data = urllib.urlencode(data)
        data = data.decode('utf-8')
        r = urllib2.Request(url,data)
        opener = urllib2.build_opener(chandle)
        u = opener.open(r,timeout=3)
        data = json.load(u,encoding="utf-8")
        return data

def genRandomUserName():
    tup = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    username = ''.join(random.sample(tup, 7))
    username = username+ str(time.time()).split('.')[0]
    return username

def readFile(path):
    time.sleep(1)
    try:
        fp = open(path)
    except IOError:
        time.sleep(1)
        return ""
    else:
        content = fp.read()
        fp.close()
    return content

def writeFile(path,content):
    try:
        fp = open(path,'w')
        fp.write(content)
    except IOError:
        fp.close()

def lock(path,content):
    try:
        fp = open(path,'w')
        fp.write(content)
    except IOError:
        fp.close()

def ckLock(path):
    try:
        fp = open(path)
    except IOError:
        return ""
    else:
        content = fp.read()
        fp.close()
    return content

def releaseLock(path):
    os.popen ("del "+path)
    print "====>Lock is Released<===="

def isLinked(ip):
    if ip==NetIP:
        print time.ctime(),"[INFO]:->Test Internet,Try to connect %s"%ip
    else:
        print time.ctime(),"[INFO]:->Test ZJ-CMCC Portal,Try to connect %s"%ip
    tmp = os.popen ("ping -n 2 "+ip).read()                   # 执行本地命令   os.popen 可以返回结果
    reObj1 = re.compile(u"\dms")
    igot = reObj1.findall(tmp)
    if len(igot)==0:
        if ip==NetIP:
            print time.ctime(),"[FAIL]:->[OffLine], Cannot Visit %s"%ip
        else:
            print time.ctime(),"[FAIL]:->Cannot Visit ZJ-CMCC Portal"
        time.sleep(1)
        return False
    else:
        if ip==NetIP:
            print time.ctime(),"[SUCC]:->[OnLine],Visit %s Successfully"%ip
        else:
            print time.ctime(),"[SUCC]:->Visit ZJ-CMCC Successfully"
        time.sleep(1)
        return True
    return False
 
class XToolRunner:
    '''
    #------------------------------------------------------
    # 成员变量
    #------------------------------------------------------
    '''
    userName    = "XToolRunner"                 #成员变量
    password    = "111111"                      #密码
    certification = "111111111111111111"        #身份证  
    validTime = "365"                           #有效时间
    regUrl  ="http://10.78.200.15:8080/ZheJiangCmccPortalAuthProject/GuestUserRegisterFunc?"  #注册网址
    loginUrl="http://10.78.200.15:8080/ZheJiangCmccPortalAuthProject/UserPortalAuthFunc?"     #登录网址
    
    '''
    #------------------------------------------------------
    # 构造方法
    #------------------------------------------------------
    '''
    
    def __init__(self):                         
        self.login()

    def TestCMCC(self):
        print time.ctime(),"[INFO]:->Before Login or Register Check ZJ-CMCC Portal"
        exitFlag = isLinked(LoginIP)
        while exitFlag==False:       #可联通则继续，否则2mins之后，再次测试
            print "-----------------------------------------------------------"
            print "[Suggest]:->Waiting 2 mins(Try to check Route or Net line)"
            print "-----------------------------------------------------------"
            time.sleep(2*60)
            exitFlag = isLinked(LoginIP)
    '''
    #------------------------------------------------------
    # 注册函数
    #------------------------------------------------------
    '''
    def register(self):
                    
        '''
        #------------------------------------------------------
        # 开始注册，生成随即用户名:
        #------------------------------------------------------
        '''
        
        self.userName = genRandomUserName()    
        print time.ctime(),"[INFO]:====###>Start to Register<###===="
        rpar = {
                'fullName'       : self.userName,
                'userName'       : self.userName,
                'password'       : self.password,
                'certification'  : self.certification,
                'validTime'      : self.validTime
                }
        
        '''
        #------------------------------------------------------
        # 注册之前，检测ZMCC网端IP是否联通，否则等待2分钟后，再次检测
        #------------------------------------------------------
        '''
        self.TestCMCC()
        
        '''
        #------------------------------------------------------
        #开始注册:
        #------------------------------------------------------
        '''
        r = post(self.regUrl,rpar)
        
        '''
        #------------------------------------------------------
        #检查注册是否成功,若失败，则再次注册:
        #------------------------------------------------------
        '''
        
        if r['errorNumber']=='0':
            print time.ctime(),"[INFO]:->Register Success!"
        else:
            print time.ctime(),"[FAIL]:->Register Failed,User has already exists,Try to Register Again!"
            self.register()
            
        '''
        #------------------------------------------------------
        #注册成功后，写入用户配置文件
        #------------------------------------------------------
        '''

        path=os.environ["TEMP"]+'\\XToolRunner.cfg'
        
        writeFile(path,self.userName)

        
    def login(self):                        #//登录
        print time.ctime(),"[INFO]:====###>Start to Login<###===="
        '''
        #------------------------------------------------------
        #读取用户配置文件，若为空，则需要重新注册:
        #------------------------------------------------------
        '''
        path=os.environ["TEMP"]+'\\XToolRunner.cfg'
        userName=readFile(path)
        if userName=='':
            print time.ctime(),"[ERRO]:->No User CFG File ,Cannot get User info"
            self.register()
        else:
            self.userName=userName
        lpar = {
                'userName'                    : self.userName,
                'password'                    : self.password
            }
        
        '''
        #------------------------------------------------------
        # 登录之前，检测ZMCC网端IP是否联通，否则等待2分钟后，再次检测
        #------------------------------------------------------
        '''
        
        self.TestCMCC()
        
        '''
        #------------------------------------------------------
        #获取用户名后，开始登录
        #------------------------------------------------------
        ''' 
            
        r=post(self.loginUrl,lpar)
        if r['errorNumber']=='1':
            if r['e_d'].split(':')[0]=='E63011':                   #user dose not exists
                print time.ctime(),"[ERRO]:====###>User dose not exists,Try it Register<###===="
                self.register()
            else:
                print time.ctime(),"[FAIL]:->Login Failed,Try it again"
                time.sleep(1)
                self.login()
        else:
            print time.ctime(),"[INFO]:====####>Login Success<####===="
            
class XThread (threading.Thread):
    def __init__(self, threadID,name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print loginInfo
        while [True]:
            if isLinked(NetIP)<>True: 
                XToolRunner()
            print "-----------------------------------------------------------"
            print "---->###(Waiting 2 mins)###<----"
            print "-----------------------------------------------------------" 
            time.sleep(60*2)
def run():
    '''
    ------------------------------------------------------
    #开启线程进入死循环，循环检测
    #------------------------------------------------------
    '''
    xthread = XThread("xRun", "XMonitor")
    path=os.environ["TEMP"]+'.\\XToolRunner.lck'
    ckLck=ckLock(path)
    if ckLck=='' or ckLck is None:
        lock(path,path) 
        xthread.start()
    else:
        print time.ctime(),"[ERRO]:->There has an another Instance Running"
        exit(-1)
    if xthread.isAlive()<>True:
        releaseLock(path)

if __name__ == '__main__':
    path=os.environ["TEMP"]+'.\\XToolRunner.lck'
    if len(sys.argv)<2:
        print "\nHELP:"
        print loginInfo
    else:
        para = sys.argv[1]
        if para=='-r':
            run()
        elif para=='-c':
            releaseLock(path)
        elif para=='-t':
            print 
        else:
            print loginInfo
