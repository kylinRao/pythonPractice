#coding:utf-8


import urllib2,urllib
import  json
import BeautifulSoup


tags=[]
url = "https://movie.douban.com/j/search_tags?type=movie"
response = urllib.urlopen(url)
result = json.loads(response.read(),encoding="utf-8")

print result

tags = result['tags']


for tag in tags:
    print tag