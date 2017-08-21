# coding=utf-8
import unittest
from interRedisCli import *


##test set and get method###
class setTest(unittest.TestCase):
    def testGssLogTest(self):
        cmdline = "set a a"
        reslut = True
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "set 成功返回True,but realResult is {realResult}".format(realResult=realResult))


class getNoneTest(unittest.TestCase):
    def testGssLogTest(self):
        cmdline = "get nothing"
        reslut = None
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "get一个不存在的key应该返回None,but realResult is {realResult}".format(realResult=realResult))


class getTest(unittest.TestCase):
    def setUp(self):
        cmdMatch("set a a")

    def testGssLogTest(self):
        cmdline = "get a"
        reslut = "a"
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "get一个a,因为有预制，所以返回a,but realResult is {realResult}".format(realResult=realResult))

    def tearDown(self):
        cmdMatch("del a")


#####test hset and hgetAll method#######
class hsetExistTest(unittest.TestCase):
    def setUp(self):
        cmdMatch("hset myname kk vv")

    def testGssLogTest(self):
        cmdline = "hset myname kk vv"
        reslut = 0
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

    def tearDown(self):
        cmdMatch("myname")


class hsetNoExistTest(unittest.TestCase):
    def setUp(self):
        cmdMatch("del myname")

    def testGssLogTest(self):
        cmdline = "hset myname kk vv"
        reslut = 1
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

        def tearDown(self):
            cmdMatch("del myname")

class hgetAllExistTest(unittest.TestCase):
    def setUp(self):
        cmdline = "hset myname kk vv"

    def testGssLogTest(self):
        cmdline = "hgetall myname "
        reslut = {'kk': 'vv'}
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

        def tearDown(self):
            cmdMatch("del myname")

class hgetAllNoExistTest(unittest.TestCase):
    def setUp(self):
        cmdMatch("del myname")

    def testGssLogTest(self):
        cmdline = "hgetall myname "
        reslut = {}
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

        def tearDown(self):
            cmdMatch("del myname")
#####zadd and zrange method test#########
class zaddAllNoExistTest(unittest.TestCase):
    def setUp(self):
        cmdMatch("del zset01")

    def testGssLogTest(self):
        cmdline = "zadd zset01 1 myname "
        reslut = 1
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

        def tearDown(self):
            cmdMatch("del zset01")

class zrangeExistTest(unittest.TestCase):
    def setUp(self):
        cmdMatch("zadd zset01 1 myname 2 myname2")

    def testGssLogTest(self):
        cmdline = "zrange zset01 0 -1 "
        reslut = ["myname","myname2"]
        realResult = cmdMatch(cmdline)
        self.failUnless(reslut == realResult,
                        "realResult is {realResult}".format(realResult=realResult))

        def tearDown(self):
            cmdMatch("del zset01")




###test not suport method like hello###
class helloWorldTest(unittest.TestCase):
    def testGssLogTest(self):
        cmdline = "hello world"
        cmd = "hello"
        reslut = "I can not support command as \033[1;31;40m {cmd} \033[0m, /(ㄒoㄒ)/~~".format(cmd=cmd)

        self.failUnless(reslut == cmdMatch(cmdline), "hello world应该是不支持的命令才对")


###test del method#####
class delNoneTest(unittest.TestCase):
    def testGssLogTest(self):
        cmdline = "del nothing"
        reslut = 0

        self.failUnless(reslut == cmdMatch(cmdline), "删除一个不存在的key应该返回0")


if __name__ == '__main__':
    unittest.main()
