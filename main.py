import re
from urllib.request import urlopen
from bs4 import  BeautifulSoup
import sys
url = 'https://en.wikipedia.org/wiki/List_of_programming_languages'
list_P = BeautifulSoup(urlopen(url), "html.parser")
pages = []

for list in list_P.find_all('div',{'class':'div-col columns column-width'}):
    for link in list.find_all('a',href=re.compile("^(/wiki)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                pages.append(link.attrs['href'])
                # with open('list_PL.txt', 'a') as l:
                #     l.write(link.attrs['href'] + '\n')

#  "url\nInflueced, Influenced by not found\n"
for i in pages: #surl파싱
    sUrl = 'https://en.wikipedia.org' + i
    print(sUrl)
    bs_obj = BeautifulSoup(urlopen(sUrl),"html.parser")
    # print(i+"parsing 1")
    table = bs_obj.find("table", {"class": "infobox"})
    if table is None:
        with open('crawl_log.txt','a') as log:
            log.write(i+'\n<table> not found\n')
    else:
        target_field_found = 0 # "Influenced", "Influenced by"
        text = ""
        
        for tr in table.find_all("tr"):
            # Optimize : Backtrack
            # (tr#i-1 -> tr#i -> tr#i -> tr#i+1) to (tr#i-1 -> tr#i -> tr#i+1)
            # if visited(i) -> skip tr#i
            th = tr.find("th")
            
            # if th is not None and not th.isspace():
            if th is not None:
                x = re.search("^Influenced$|^Influenced by$", th.text)
                #print(x)
                if (x):
                    target_field_found += 1
                    text += th.text + "|"

                    # for td in tr.find_all('td'):
                        # if td is not None and not td.isspace():
                        # if td is not None:
                            # print(td.text)
                            # text += td.text+"|"

                    # next <tr>'s <td>'s <a>(s)
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
