#!/usr/bin/env python
# coding=utf-8
from cassandra.auth import *
from cassandra.cluster import Cluster
from multiprocessing.dummy import Pool as ThreadPool
import os
import datetime
# sudo pip install Cython==0.25.2
# ###cassandra-driver最好直接下载tar包来安装https://pypi.python.org/pypi/cassandra-driver/3.11.0
# sudo pip install cassandra-driver
# 安装大概5min
class cqlControl():

    auth_provider = PlainTextAuthProvider( username='cassandra', password='cassandra')
    cluster = Cluster(["192.168.1.113"],auth_provider=auth_provider)
    session = cluster.connect('mykeyspace')
    def exeCql(self,session,cql):
        session.execute(cql)
    def insertRoleInfo(self,accountid,packageName="com.huawei.zhifu6.com"):
        cql = """  insert into users (user_id , fname , lname) values ({accountid},'{packageName}','ladjslf')  """.format(accountid=accountid,packageName=packageName)
        self.exeCql(self.session,cql)
    def cqlMoreArgs(self,accountidRange,needMorePackageName=0):
        if needMorePackageName == 0:
            for accountid in accountidRange:
                self.insertRoleInfo(accountid)
        else:
            for accountid in accountidRange:
                for packIndex in xrange(0,2000):
                    self.insertRoleInfo(accountid=accountid,packageName="com.huawei.zhifu{packIndex}.com".format(packIndex=packIndex))



if __name__ == '__main__':
    bt = datetime.datetime.now()
    print bt
    cqlobj = cqlControl()

    pool = ThreadPool(110)
    pool.map(cqlobj.insertRoleInfo, xrange(0,100))
    pool.close()
    pool.join()


    # for i in xrange(0,10000):
    #     insertRoleInfo(accountid=i)

    et = datetime.datetime.now()
    print et
    print et - bt



    # pool = Pool()
    # pool.map(fun, xrange(0,199))
    # pool.close()
    # pool.join()