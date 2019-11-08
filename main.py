import re #用于字符串匹配
from urllib.request import urlopen  #用于实现对目标url的访问
from bs4 import BeautifulSoup #用于从网页抓取数据

url = 'https://en.wikipedia.org/wiki/List_of_programming_languages' #父节点地址
list_P = BeautifulSoup(urlopen(url), "html.parser") #爬虫
pages = []#把爬虫的叶节点地址存到列表
for list in list_P.find_all('div',{'class':'div-col columns column-width'}): #探索div节点
    for link in list.find_all('a',href=re.compile("^(/wiki)")): #是否div子节点中存在需要的a节点
        if 'href' in link.attrs: #是否需要的属性
            if link.attrs['href'] not in pages: #是否确认重复
                pages.append(link.attrs['href']) #加到pages列表

for i in pages: #爬虫sUrl循环句
    sUrl = 'https://en.wikipedia.org' + i #子节点的地址
    print(sUrl) #确认编译位置
    bs_obj = BeautifulSoup(urlopen(sUrl),"html.parser")#爬虫子节点
    table = bs_obj.find("table", {"class": "infobox"})#找到table节点
    if table is None: #是否不需要的子节点
        with open('crawl_log.txt','a') as log:#以扩展名text保存
            log.write(i+'\n<table> not found\n')
    else:
        target_field_found = 0 # "Influenced", "Influenced by"
        text = ""
        
        for tr in table.find_all("tr"):
            th = tr.find("th")
            if th is not None:
                x = re.search("^Influenced$|^Influenced by$", th.text)
                if (x):
                    target_field_found += 1
                    text += th.text + "|"
                    atags = tr.next_sibling.find("td").find_all("a", href=re.compile("(/wiki/)"))
                    for atag in atags:

                        text += atag.text
                        if (atag is not atags[-1]):
                            text += "|"
                    text += "\n"
                    
                if (target_field_found is 2):
                    break
        if (target_field_found is 0):
            with open('crawl_log.txt', 'a') as log:
                    log.write(i + '\nInflueced, Influenced by not found\n')
        else:
            with open('output.txt', 'a', buffering=-1, encoding='utf-8') as f:
                f.write(i + '\n')
                f.write(text)
