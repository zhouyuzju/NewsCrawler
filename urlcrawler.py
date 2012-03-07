from urllib import urlopen
from BeautifulSoup import BeautifulSoup
import re,sys,Queue,datetime,time
import threading,mutex
from sinaNewsParser import sinaNewsParser
from newsDAO import newsDAO
output = open('./url.txt','w')
#mutex
amutex = threading.Lock()
#unique url set
urlset = set()
#parser url job queue
urlqueue = Queue.Queue()

class UrlParser(threading.Thread):
    worker_count = 0
    def __init__(self):
        threading.Thread.__init__(self)
        self.id = UrlParser.worker_count
        UrlParser.worker_count += 1
        self.setDaemon(True)
        self.start()
    def run(self):
        while True:
            try:
                job = urlqueue.get()
                output.write('[INFO]\t[%s]\tworker[%d]:\t%s\n' % (time.strftime("%H:%M:%S", time.localtime()),self.id,str(job)))
                #print "worker[%d]: %s" % (self.id, str(job))
                today = datetime.date.today()
                newsurlpattern = re.compile(str(today))
                text = urlopen(job).read()
                soup = BeautifulSoup(text,fromEncoding="gb18030")
                if newsurlpattern.search(job):
                    #output.write('[PARSER]\t[%s]\tworker[%d]: %s\n' % (time.strftime("%H:%M:%S", time.localtime()),self.id,str(job)))
                    news = sinaNewsParser(soup)
                    output.write('[NEWS]\t[%s]\tworker[%d]:\t%s\n\t[title]:\t%s\n\t[publish date]:\t%s\n\t[contents]:\t%s\n' % (time.strftime("%H:%M:%S", time.localtime()),self.id,str(job),news['title'],news['pubdate'],news['content']))
                    #stmt = 'insert into NEWS (NEWS_TITLE,NEWS_CONTENT,NEWS_PUBLISHDATE,NEWS_URL) values(\'%s\',\'%s\',\'%s\',\'%s\')' % (news['title'],news['content'],news['pubdate'],str(job))
                    #newsDAO(stmt)
                for header in soup('a'):
                    #<a>label which has href attribute
                    if header.has_key('href'):
                        #strip whitespace before or after the string
                        url = header['href'].encode('utf-8').strip()
                        #if the string begins with 'http://' or 'https://'and isn't in the urlset
                        pattern = re.compile('^(https?://)')
                        amutex.acquire()
                        if pattern.match(url) and url not in urlset:
                            urlqueue.put(url)
                            urlset.add(url)
                        amutex.release()
            except Queue.Empty:   
               break
            except:
                output.write('[ERROR]\t[%s]\tworker[%d]\n' % (time.strftime("%H:%M:%S", time.localtime()),self.id))
class JobManager:
    def __init__(self, threadnumber = 10):
        self.jobs = []
        self._initThreads(threadnumber)
    def _initThreads(self, threadnumber):
       for i in range(threadnumber):
           job = UrlParser()
           self.jobs.append(job)
    def wait(self):
       # ...then, wait for each of them to terminate:
       while len(self.jobs):
           job = self.jobs.pop()
           job.join()
           if job.isAlive() and not urlqueue.empty():
               self.jobs.append(job)
       output.write("All jobs are are completed.\n")
def test():
    urlset.add('http://news.sina.com.cn/')
    urlqueue.put('http://news.sina.com.cn/')
    manager = JobManager()
    manager.wait()
if __name__ == "__main__":
    test()
