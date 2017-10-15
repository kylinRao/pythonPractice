#!/usr/bin/env python
# coding=utf-8
# 适用于redis集群的操作
#pip install redis
#pip install Redis-py-cluster
from rediscluster import StrictRedisCluster
import sys


def redis_cluster():
    redis_nodes = [{'host': '192.168.1.113', 'port': 6379},

                   ]
    try:
        redisconn = StrictRedisCluster(startup_nodes=redis_nodes)
    except Exception, e:
        print e
        print "connect error"
        sys.exit(1)

    redisconn.set('name', 'kk')
    print "name is", redisconn.get('name')
    exec("print(redisconn.get('name'))")
    print(help(redisconn))

redis_cluster()
