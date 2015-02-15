import urllib.request as urlreq
from bs4 import BeautifulSoup as soup
import time
import pymongo
import queue
import os.path

server = pymongo.MongoClient('localhost', 27017)
db = server['webcrawler']
collection = db['arxiv']

root = "http://arxiv.org"
startingurl = root + '/abs/0801.2587'
replacementString = "/find/all/1"

fname = 'queue.txt'

linksCrawled = []

q = queue.Queue()

if not os.path.isfile(fname):
    q.put(startingurl)
else:
    qFile = open(fname, 'r')
    for line in qFile:
        q.put(line)

    qFile.close()


def getPaperData(url):
    if linksCrawled.__contains__(url):
        return 0
    linksCrawled.append(url)
    try:
        data = soup(urlreq.urlopen(url).read())
    except HttpError as e:
        print('error occurred')
        return -1
    date = data.find("meta", {"name": "citation_date"})["content"]
    ID = data.find("meta", {"name": "citation_arxiv_id"})["content"]
    subjects = data.find("td", {"class": "tablecell subjects"}).text.split(";")
    authorTags = data.find("div", {"class": "authors"}).find_all("a", limit=5)

    authors = []
    names = []
    j=0;
    for tag in authorTags:
        try:
            if j >= 5:
                print(j)
            j=j+1
            link = root + replacementString + tag.get("href").split("1", 1)[1]
            name = tag.text
            names.append(name)
            authors.append((name,link))
        except IndexError as e:
            print("index out of range")

    data = {'_id':ID, 'date' : date, 'subjects' : subjects, 'authors' : names}
    collection.update({'_id':ID}, data, upsert=True)
    for author in authors:
        link = author[1]
        if linksCrawled.__contains__(link):
            continue
        linksCrawled.append(link)
        try:
            paperSite = soup(urlreq.urlopen(link).read())
        except:
            print('error occurred')
            return 0
        time.sleep(3)
        paperElements = paperSite.find_all("span", {"class": "list-identifier"}, limit=10)

        papers = []
        for paper in paperElements:
            link = root + paper.find("a", {"title": "Abstract"}).get("href")
            papers.append(link)
            if not linksCrawled.__contains__(link):
                q.put(link)

if q.empty():
    q.put(startingurl)
i=0
while not q.empty():
    url = q.get()
    try:
        getPaperData(url)
    except:
        print(url)
        print('error')

    qWrite = open(fname, 'w')
    list = []
    while not q.empty():
        tmp = q.get()
        list.append(tmp)
        qWrite.write(tmp+'\n')
    qWrite.close()

    for elem in list:
        q.put(elem)

    if i%100==0:
        print(str(i+1)+' papers read')
        print(str(q.qsize()) + ' elements queued')
    i=i+1
    time.sleep(5)




