import requests
import sys
from collections import defaultdict

post_url = "http://api.pullword.com/post.php"
get_url = "http://api.pullword.com/get.php"
keywordmap = dict()
kewwordrelamap = defaultdict(list)
linenum1 = [0]
linenum2 = [0]
linenum3 = [0]
linenum4 = [0]

kewwordrelamap["王婆"]=linenum1
kewwordrelamap["媒婆"]=linenum2
kewwordrelamap["牙婆"]=linenum3
kewwordrelamap["虔婆"]=linenum4

class ServerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def split_word(words):
    words = words.split()
    words_list = []
    for i in words:
        if(i.__contains__("婆")):
            words_list.append(i.split(":"))
            if keywordmap.get(i.split(":")[0]):
                keywordmap[i.split(":")[0]] = keywordmap[i.split(":")[0]] + 1
            else:
                keywordmap[i.split(":")[0]] = 1
    return words_list


def pullword_post(source="", threshold=0, debug=1):
    payload = {"source": source.encode("utf8"), "param1": threshold, "param2": debug}
    pw = requests.post(post_url, data=payload)
    ps = pw.url
    if pw.status_code != 200:
        raise ServerError("server return %s" % pw.status_code)
    return split_word(pw.content.decode())

def pullword_get(source="", threshold=0, debug=1):
    pw = requests.get("http://api.pullword.com/get.php?"+"source="+source+"&param1=0&param2=1")
    ps = pw.url
    if pw.status_code != 200:
        raise ServerError("server return %s" % pw.status_code)
    return split_word(pw.content.decode())

targetfile = open('C://Users//test//Desktop//result//关键字查找结果.txt', 'w', encoding='utf-8', errors='ignore')
resultfile = open('C://Users//test//Desktop//result//分词结果.txt', 'w', encoding='utf-8', errors='ignore')
resultfile1 = open('C://Users//test//Desktop//result//分词概率结果.txt', 'w', encoding='utf-8', errors='ignore')
resultfile2 = open('C://Users//test//Desktop//result//关联分析结果.txt', 'w', encoding='utf-8', errors='ignore')
linecontent = "";
with open('C://Users//test//Desktop//三言二拍全.txt', 'r', encoding='utf-8', errors='ignore') as sourcefile:
    a = sourcefile.read()
    contentArray = a.split("，")
    occur = 0
    linenumber = 0
    for content in contentArray:
        linenumber = linenumber + 1
        if(content.__contains__("王婆")):
            linenum1.append(linenumber)
        elif(content.__contains__("媒婆")):
            linenum2.append(linenumber)
        elif(content.__contains__("牙婆")):
            linenum3.append(linenumber)
        elif(content.__contains__("虔婆")):
            linenum4.append(linenumber)
        else:
            pass
        if(content.__contains__("婆")):
            if(occur < 20):
                linecontent = linecontent + content + "，"
                occur = occur + 1
            else:
                targetfile.write(linecontent.replace("\n","") + "\n")
                linecontent = ""
                occur = 0
    targetfile.write(linecontent.replace("\n", "") + "\n")
targetfile.close()
with open('C://Users//test//Desktop//result//关键字查找结果.txt', 'r', encoding='utf-8', errors='ignore') as f:
    a = f.readlines()
    for keywordcontent in a:
        resultfile1.write(''.join(["%s is %s \n" %(k,v) for k,v in pullword_get(keywordcontent)]))
resultfile1.close()
resultfile.write(''.join(["%s \t %s \n" %(k,v) for k,v in keywordmap.items()]))
resultfile.close()
resultfile2.write(''.join(["%s \t %s \n" %(k,v) for k,v in kewwordrelamap.items()]))
resultfile2.close()