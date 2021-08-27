from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import ssl
import os


try:
     _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


    
def get_page_content(url):
    try:
        html_response_text=urlopen(url).read()
        page_content=html_response_text.decode('utf-8')
        return page_content
    except Exception as e:
        return None

def get_urls(soup):
    links=soup.find_all('a')
    urls=[]
    for link in links:
        urls.append(link.get('href'))
    return urls

def is_url_valid(url):
     if url is None:
          return False
     if re.search(':', url):
          return False
     if re.search('File:', url):
          return False 
     if re.search('#', url):
          return False
     match = re.search('^/wiki/', url)
     if match:
          return True
     else:
          return False


def reformat_url(url):
    match=re.search('^/wiki/', url)
    if match:
        return "https://en.wikipedia.org"+url
    else:
        return url

def save(text,path):
    f=open(path,'w', encoding = 'utf-8', errors = 'ignore')
    f.write(text)
    f.close()

def clean_title(title):
        invalid_characters= ['<', '>', ':', '"', '/', '\\','|', '?', '*']
        for c in invalid_characters:
                title=title.replace(c,' ')
        return title
    
def FocusedCrawler():

    queue = []
    visitedUrlList = []
    pageCounter = 0
    savedUrlList= []
    relatedterms=['covid', 'coronavirus', 'pandemic','death', 'trump', '2020','election', 'biden', 'cases','vaccine']
    SeedUrls=['https://en.wikipedia.org/wiki/2020_in_the_United_States', 'https://en.wikipedia.org/wiki/COVID-19_pandemic']


    for url in SeedUrls:
        queue.append(url)
        visitedUrlList.append(url)
   

    while len(queue)>0:
        url = queue.pop(0)
        page_content = get_page_content(url)    
        if page_content is None:
            continue
        termCounter=0
        soup = BeautifulSoup(page_content, 'html.parser')
        page_text= soup.get_text()
        
    
        for term in relatedterms:
            if re.search(term, page_text, re.I):
                termCounter = termCounter+1
                if termCounter >= 2:
                    title= soup.title.string
                    title=clean_title(title)
                    save(title, '/Users/rmerendino/Desktop/Crawler/crawledpages/' + title +'.html')
                    save(page_content, '/Users/rmerendino/Desktop/Crawler/crawledpages/'+title+'.html')
                    savedUrlList.append(url)
                    pageCounter= pageCounter + 1
                    print("page count: "+ str(pageCounter) + ", term counter " + str(termCounter) + ", url: " + url)
                    break

        if pageCounter > 500:
            break
     

        urls = get_urls(soup)
        for url in urls:
            #url=reformat_url(str(url))
            if is_url_valid(url):
                 url=reformat_url(url)
                 if url not in visitedUrlList:
                      queue.append(url)
                      visitedUrlList.append(url)


  #  save(savedUrlList, '/Users/rmerendino/Desktop/Crawler/crawled pages')
    f=open("saved_urls.txt","w")
    i=1
    for url in savedUrlList:
         f.write(str(i)+ ': ' + url +'\n')
         i+=1
    f.close()

FocusedCrawler()


