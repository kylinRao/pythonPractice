#!/usr/bin/env python
# coding=utf-8
# 适用于redis集群的操作
#pip install redis
# pip install Redis-py-cluster
#打包python为exe文件工具https://sourceforge.net/projects/cx-freeze/files/4.3.3/cx_Freeze-4.3.3.win-amd64-py2.7.msi/download
#http://blog.csdn.net/wuxiaobingandbob/article/details/45196485
import os
import platform
from rediscluster import StrictRedisCluster
import sys
import path
import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='run.log',
                filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
###定义可用的redis分片节点
redis_nodes = []

###定义各种支持的操作符和可使用的格式
cmdMatchDic = {
    "set": {"cmd": "set", "description": " set name value | Set the value at key name to value"},
    "get": {"cmd": "get", "description": "get name | Return the value at key name, or None if the key does not  exist"},
    "hset": {"cmd": "hset",
             "description": " hset name, key, value |  Set ``key`` to ``value`` within hash ``name``, Returns 1 if HSET created a new field, otherwise 0"},
    "hgetall": {"cmd": "hgetall",
                "description": "hgetall  name |  Return a Python dict of the hash's name/value pairs"},
    "zadd": {"cmd": "zadd", "description": "zadd name, *args | zadd  my-key  1.1   name1  2.2   name2"},
    "zrange":{"cmd":"zrange","description":"zrange name start end | for example zrange zset01 0 -1 "},
    "ttl":{"cmd":"ttl","description":"ttl name | for example ttl zset01"},
    "type":{"cmd":"type","description":"type key | for example ttl zset01"},
    "expire":{"cmd":"expire","description":"expire name time | for example expire zset01 100"},
    "del": {"cmd": "delete", "description": "delete *names | Delete one or more keys specified by names"},
    "exit": {"cmd": "exit", "description": "exit"},
    "quit": {"cmd": "quit", "description": "quit"},
    "help":{"cmd":"help","description":"help"},


}


def cmdMatch(userInput):
    cmdline = userInput.split()
    cmd = cmdline[0].lower()
    for key in cmdMatchDic.keys():
        if cmd in key.lower():
            return cmdExe(cmdMatchDic[cmd]["cmd"], cmdline)
            ###\033[1;31;40m  means red ，\033[0m means black
    if 'Windows' in platform.system():
        return "I can not support command like  [[ {cmd} ]]".format(cmd=cmd)
    else:
        return "I can not support command like \033[1;31;40m {cmd} \033[0m, /(ㄒoㄒ)/~~".format(cmd=cmd)




def cmdExe(cmd, cmdline):
    result = ""
    if cmd in ("quit", "exit"):
        sys.exit(0)
    if cmd in ("help"):
        for value in cmdMatchDic.values():
            # print value
            print "{cmd}__{description}{linesep}".format(cmd=value['cmd'],description=value["description"],linesep=os.linesep)

    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
        # print help(redisconn)
    except Exception, e:
        logging.error("connect error")
        sys.exit(1)

    if cmd == "zrange":
        exeCmd = "result = redisconn.{cmd}( {cmdline} ".format(cmd=cmd, cmdline=" ,".join(
        ["'{s}'".format(s=s) for s in cmdline[1:]]))+",withscores=True )"
        logging.debug(exeCmd)
    else:
        exeCmd = "result = redisconn.{cmd}( {cmdline} )".format(cmd=cmd, cmdline=" ,".join(
        ["'{s}'".format(s=s) for s in cmdline[1:]]))
    try:
        logging.debug(exeCmd)
        exec (exeCmd)

    except Exception, e:
        logging.error(e)
        return "Usage:" + cmdMatchDic[cmd]["description"]
    return result
# 只有一个配置文件的话，将节点信息放入redis_nodes中，多个配置文件的话根据用户的选择来
def getNodes():
    DCNodeStr = ""
    conFileList = []
    show2User = ''
    passWord = "default"
    index =0
    # 获取最大的文件数量，来决定是否需要用户选择链接到哪个文件
    for dirpath, dirs, files in os.walk("conf"):
        # print index
        # index = index +1
        # print "dirpath is {dirpath},dirs is {dirs},files is {files}".format(dirpath=dirpath,dirs=dirs,files=files)
        for file in files:
            conFileList.append(os.path.join(dirpath,file))
            logging.debug("found config files {conFileList}".format(conFileList=conFileList) )
            # print "conFileList and len: ",conFileList,len(conFileList)
    if len(conFileList) > 1:
        for index, aConFile in enumerate(conFileList):
            show2User = show2User + "input {index} to use {aConFile} \r".format(index=index,aConFile=aConFile);
            logging.debug("message to show to user:{show2User}".format(show2User=show2User))
            print show2User
        ConFileIndex =  raw_input("input you selection />")
        while 1:
            try :
                int(ConFileIndex)
                break
            except:
                ConFileIndex =  raw_input("error index,input again />")

        while (int(ConFileIndex)<0) or (int(ConFileIndex)>=len(conFileList)):
            ConFileIndex =  raw_input("error index,input again />")
        with open(conFileList[int(ConFileIndex)],"r") as f:
            DCNodeStr = f.readline().strip()
            print "DCNodeStr is: ",DCNodeStr
            passWord = f.readline()
            print "passWord is :",passWord
            if  passWord:
                pass
            else:
                passWord = "default"
    else:
        ConFileIndex = 0
        # print conFileList
        for file  in conFileList:
            with open(file,"r") as f:

                DCNodeStr = f.readline().strip()
                print "DCNodeStr is: ",DCNodeStr
                passWord = f.readline()
                print "passWord is :",passWord
                if  passWord:
                    pass
                else:
                    passWord = "default"
    for ipports in DCNodeStr.split(","):
        logging.debug("reading host and post :{ipports}".format(ipports=ipports))
        if ipports:
            tempDic = {}
            logging.debug(ipports.split(":"))
            print ipports.split(":")
            tempDic["host"], tempDic["port"]= ipports.split(":")
            tempDic["passWord"] = passWord
            redis_nodes.append(tempDic)
    return conFileList[int(ConFileIndex)]

if __name__ == '__main__':
    os.path
    while 1:
        conFileStr = getNodes()
        # logging.debug("redis_nodes is:",redis_nodes)
        for node in redis_nodes:
            logging.debug("ip port passWord is:{ip} {port} {passWord}".format(ip=node["host"],port=node["port"],passWord=node["passWord"]))
            logging.debug("======starting a redic-cli.exe======")
            str = "".join(["start ",os.path.join(os.getcwd(),"redis-cli.exe")," -h ",node["host"]," -p ",node["port"]," -a ",node["passWord"]])
            # str = r"".join(["redis-cli.exe"," -h ",node["host"]," -p ",node["port"]])
            logging.debug(str)
            os.system(str)
            print "a redis-cli is poped , and ni keyi zai dakai yige o"
            break;
        #
        #
        # userInput = raw_input("{conFileStr} />".format(conFileStr=conFileStr))
        # print cmdMatch(userInput)
