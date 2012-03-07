import _mysql

def newsDAO(stmt):
    try:
        conn = _mysql.connect(host="localhost",user="root",passwd="zhouyuzju",db="news")
        conn.query(stmt)
        conn.close()
    except _mysql.Error,e:
        print "Error %d: %s" %(e.args[0],e.args[1])
    
if __name__ == "__main__":
    title = 'hello'
    content = 'hello world'
    date = '2011-12-07'
    stmt = 'insert into NEWS (NEWS_TITLE,NEWS_CONTENT,NEWS_PUBLISHDATE) values(\'%s\',\'%s\',\'%s\')' % (title,content,date)
    newsDAO(stmt)
