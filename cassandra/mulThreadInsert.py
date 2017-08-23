from cassandra.cluster import Cluster
from multiprocessing.dummy import Pool as ThreadPool
import os
import datetime

cluster = Cluster(["192.168.1.113"])
session = cluster.connect('mykeyspace')
def exeCql(session,cql):
    session.execute(cql)
def insertRoleInfo(accountid,packageName="com.huawei.zhifu6.com"):
    cql = """  insert into users (user_id , fname , lname) values ({accountid},'{packageName}','ladjslf')  """.format(accountid=accountid,packageName=packageName)
    exeCql(session,cql)
def cqlMoreArgs(accountidRange,needMorePackageName=0):
    if needMorePackageName == 0:
        for accountid in accountidRange:
            insertRoleInfo(accountid)
    else:
        for accountid in accountidRange:
            for packIndex in xrange(0,2000):
                insertRoleInfo(accountid=accountid,packageName="com.huawei.zhifu{packIndex}.com".format(packIndex=packIndex))


    et = datetime.datetime.now()
if __name__ == '__main__':
    bt = datetime.datetime.now()
    print bt

    pool = ThreadPool(110)
    pool.map(insertRoleInfo, xrange(0,100000))
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