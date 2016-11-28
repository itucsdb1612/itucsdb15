import psycopg2 as dbapi2
 
 
class Comment:
    def __init__(self,commenter,groupcommented,text):
        self.commenter = commenter
        self.groupcommented=groupcommented
        self.text= text
        
        
comment1=Comment(1,1,"test")
comment2=Comment(2,1,"add")

def selectcomments(dsn,groupcommented):
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        statement = """ SELECT USERNAME,COMMENT FROM GROUPCOMMENTS,SITEUSER WHERE (GROUPCOMMENTS.COMMENTER = SITEUSER.USERID) AND (GROUPCOMMENTED = %s)"""
        cursor.execute(statement,(groupcommented))
        comments = cursor.fetchall()
        return comments
        cursor.close()

def insertcomment(dsn,comment):
    with dbapi2.connect(dsn) as connection:
        cursor = connection.cursor()
        statement = """ INSERT INTO GROUPCOMMENTS (COMMENTER,GROUPCOMMENTED,COMMENT) VALUES(%s,%s,%s)"""
        cursor.execute(statement,(comment.commenter,comment.groupcommented,comment.text))
        cursor.close()
    