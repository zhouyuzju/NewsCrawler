from urllib import urlopen
from BeautifulSoup import BeautifulSoup
def sinaNewsParser(soup):
    newscontents = ''
    newstitle = ''
    pubdate = ''
    contenttitle = soup.find('h1',id='artibodyTitle')
    vediotitle = soup.find('div',id='videoTitle')
    date = soup.find('span',id='pub_date')
    if contenttitle:
        newstitle = str(contenttitle.getText().encode('utf-8'))
    elif vediotitle:
        newstitle = str(vediotitle.getText().encode('utf-8'))
    if date:
        pubdate = str(date.getText().encode('utf-8'))
    contentbody = soup.find('div',id="artibody")
    vediobody = soup.find('td',id='videoContent')
    if contentbody:
        p = contentbody.find('p')
        if not p.find('script'):
            newscontents += str(p.getText().encode('utf-8'))
        while p.findNextSibling('p'):
            p = p.findNextSibling('p')
            if not p.find('script'):
                newscontents += str(p.getText().encode('utf-8'))
    elif vediobody:
        p = vediobody.find('p')
        if not p.find('script'):
            newscontents += str(p.getText().encode('utf-8'))
        while p.findNextSibling('p'):
            p = p.findNextSibling('p')
            if not p.find('script'):
                newscontents += str(p.getText().encode('utf-8'))
    news = dict()
    news['title'] = newstitle
    news['pubdate'] = pubdate
    news['content'] = newscontents
    return news
    
if __name__ == "__main__":
    text = urlopen('http://ent.sina.com.cn/s/m/2011-12-07/10483501281.shtml').read()
    soup = BeautifulSoup(text,fromEncoding="gb18030")
    news = sinaNewsParser(soup)
    print '[NEWS]\ttitle: %s\n\t\tpublish date: %s\n\t\tcontents: %s\n' % (news['title'],news['pubdate'],news['content'])
