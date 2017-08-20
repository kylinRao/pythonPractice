# coding=utf-8
import unittest
from interRedisCli import *
class helloWorldTest(unittest.TestCase):
    def testGssLogTest(self):
        cmdline = "hello world"
        cmd = "hello"
        reslut = "I can not support command as \033[1;31;40m {cmd} \033[0m, /(ㄒoㄒ)/~~".format(cmd=cmd)

        self.failUnless( reslut == cmdMatch(cmdline) , "hello world应该是不支持的命令才对")
class delTest(unittest.TestCase):
    def testGssLogTest(self):
        cmdline = "del key"
        cmd = "hello"
        reslut = "I can not support command as \033[1;31;40m {cmd} \033[0m, /(ㄒoㄒ)/~~".format(cmd=cmd)

        self.failUnless( reslut != cmdMatch(cmdline) , "del应该是支持的命令才对")
if __name__ == '__main__':
    unittest.main()