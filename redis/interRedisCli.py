#!/usr/bin/env python
# coding=utf-8
# 适用于redis集群的操作
# pip install Redis-py-cluster
import os

from rediscluster import StrictRedisCluster
import sys

###定义可用的redis分片节点
redis_nodes = [{'host': '192.168.1.113', 'port': 7005},
               {'host': '192.168.1.113', 'port': 7004},
               {'host': '192.168.1.113', 'port': 7003},
               {'host': '192.168.1.113', 'port': 7000},
               {'host': '192.168.1.113', 'port': 7001},
               {'host': '192.168.1.113', 'port': 7002}
               ]
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

}


def cmdMatch(userInput):
    cmdline = userInput.split()

    cmd = cmdline[0].lower()

    for key in cmdMatchDic.keys():
        if cmd in key.lower():
            return cmdExe(cmdMatchDic[cmd]["cmd"], cmdline)

            ###\033[1;31;40m  means red ，\033[0m means black
    return "I can not support command as \033[1;31;40m {cmd} \033[0m, /(ㄒoㄒ)/~~".format(cmd=cmd)


def cmdExe(cmd, cmdline):
    result = ""
    if cmd in ("quit", "exit"):
        sys.exit(0)

    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception, e:
        print "connect error"
        sys.exit(1)

    exeCmd = "result = redisconn.{cmd}( {cmdline} )".format(cmd=cmd, cmdline=" ,".join(
        ["'{s}'".format(s=s) for s in cmdline[1:]]))
    try:
        exec (exeCmd)
    except Exception, e:
        return "Usage:" + cmdMatchDic[cmd]["description"]

    return result
def getNodes():
    DCNodeStr = ""
    for root, dirs, files in os.walk("."):
        for file in files:
            if "DC" in file:
                with open(file,"r") as f:
                    DCNodeStr = f.read()
    for ipports in DCNodeStr.split(","):
        if ipports:
            tempDic = {}
            print ipports.split(":")
            tempDic["host"], tempDic["port"] = ipports.split(":")
            redis_nodes.append(tempDic)

if __name__ == '__main__':
    getNodes()
    while 1:
        userInput = raw_input("Your cmd />")

        print cmdMatch(userInput)
