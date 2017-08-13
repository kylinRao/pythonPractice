#coding=utf-8

import urllib
import urllib2
import json



##post请求样例
url ="http://shuju.wdzj.com/plat-info-target.html"

data =  urllib.urlencode({"wdzjPlatId":'52',"type":'2',"target1":'1',"target2":'0'})
request = urllib2.Request(url)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)
response = opener.open(url,data)
print response.read()