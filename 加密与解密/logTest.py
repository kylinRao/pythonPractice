# coding=utf-8
import unittest,log
class logTest(unittest.TestCase):
    def testGssLogTest(self):
        agss = log.log()
        logStr = "logStr"
        desireStr = "desireStr"
        self.failUnless( desireStr == agss.gssLogDec(logStr=logStr) , "日志解密失败")
if __name__ == '__main__':
    unittest.main()