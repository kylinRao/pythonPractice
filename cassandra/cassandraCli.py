#!/usr/bin/env python
# coding=utf-8
#源码包下载地址：

#https://pypi.python.org/pypi/cql/

import cql

print(help(cql.connect))
# connection = cql.connect(host, port, keyspace)
# cursor = connection.cursor()
# cursor.execute("CQL QUERY", dict(kw='Foo', kw2='Bar'))
# for row in cursor:  # Iteration is equivalent to lots of fetchone() calls
#     doRowMagic(row)
#
# cursor.close()
# connection.close()