#!/usr/bin/env python
# coding=utf-8
# 适用于redis集群的操作
#pip install Redis-py-cluster
from rediscluster import StrictRedisCluster
import sys
cmdMatchDic = {
    "del":"delete({args})",
    "get":"get({args})",
    "hgetall":"hgetall({args})",



}
def cmdMatch(userInput):

    cmdline = userInput.split()

    cmd = cmdline[0].lower()

    for key in cmdMatchDic.keys():
        if cmd in key.lower():
            return cmdExe(cmdMatchDic[cmd],cmdline)

###\033[1;31;40m  means red ，\033[0m means black
    return  "I can not support command as \033[1;31;40m {cmd} \033[0m, /(ㄒoㄒ)/~~".format(cmd=cmd)


def cmdExe(cmd,cmdline):
    exec("")

    return cmd




if __name__ == '__main__':
    while 1:
        userInput = raw_input("Your cmd />")

        print cmdMatch(userInput)
