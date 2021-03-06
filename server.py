﻿import datetime
import os
import json
import ctypes  # An included library with Python install.
import re
import psycopg2 as dbapi2

from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import jsonify
from flask.helpers import url_for

from initialize_database import *

from user import *
from Authors import *
from Books import *
from Bookdetails import *
from Genres import *
from Quotes import *
from BlogPost import *
from Job import *
from FeedType import *
from Feed import *
from flask.globals import session
from Groups import *
from News import *
from Members import *
from message import *
from follow import *
from event import *
from Groupcomments import *
from Authorcomments import *
from distutils.command.check import check


app = Flask(__name__)

@app.route('/dontrunthis')
def initialize():

    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor =connection.cursor()
        try:
            dropEventTable(cursor)
            dropFollowerTable(cursor)
            dropUserMessagesTable(cursor)
            dropUserTable(cursor)
            dropUserTypeTable(cursor)
            create_usertype_table(cursor)
            create_user_table(cursor)
            create_user_message_table(cursor)
            create_user_follower_table(cursor)
            create_event_table(cursor)
            insert_usertype(cursor,'Admin')
            insert_usertype(cursor,'User')
            salt1 = createRandomSalt()
            password = '123456'
            createdHash = createHash(salt1,password)
            user1 = User(0,'benlielif',password,salt1,createdHash,'elfbnli@gmail.com','Elif','Benli',1)
            insert_siteuser(cursor,user1)
            salt2 = createRandomSalt()
            createdHash = createHash(salt2,password)
            user2 = User(0,'uyar',password,salt2,createdHash,'uyar@itu.edu.tr','Turgut','Uyar',1)
            insert_siteuser(cursor,user2)
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor =connection.cursor()
        try:
            drop_tables(cursor)
            create_genre_table(cursor)
            create_book_table(cursor)
            create_quote_table(cursor)
            create_bookdetails_table(cursor)
            create_news_table(cursor)
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor =connection.cursor()
        try:
            create_blogs_table(cursor)
            create_jobs_table(cursor)
            create_feedtypes_table(cursor)
            create_feeds_table(cursor)
        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

    dropgroupandauthortables(app.config['dsn'])
    create_groups_table(app.config['dsn'])
    insert_group(app.config['dsn'],group1)
    create_members_table(app.config['dsn'])
    create_author_table(app.config['dsn'])
    create_groupcomments_table(app.config['dsn'])
    create_authorcomments_table(app.config['dsn'])
    insertAuthor(app.config['dsn'],author1)
    insertAuthor(app.config['dsn'],author2)
    insertAuthor(app.config['dsn'],author3)
    insertAuthor(app.config['dsn'],author4)
    insertcomment(app.config['dsn'],comment1)
    insertcomment(app.config['dsn'],comment2)

    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor =connection.cursor()
        try:
            newBest = News("Best authors are voted! There is also one Turkish in top 50",2016,"Best authers")
            #insert_news(news1)

            #insert_member(1,1)


            '''Creating and inserting samples for books, genres and quotes tables'''

            '''insert_genre function returns with "not all arguments converted during string formatting"
            needs to be resolved'''
            genre1 = Genre(0, "Novel")
            insert_genre(app.config['dsn'],genre1)
            genre2 = Genre(0, "Satire")
            insert_genre(app.config['dsn'],genre2)

            book1 = Book(0, "The Sun Also Rises", 1926, 1, 1)
            book2 = Book(0, "Adventures of Hucleberry Finn", 1884, 2, 2)

            details1 = Bookdetails(None, 1, "https://upload.wikimedia.org/wikipedia/en/9/93/Hemingwaysun1.jpg", "The Sun Also Rises is a 1926 novel written by American author Ernest Hemingway about a group of American and British expatriates who travel from Paris to the Festival of San Fermín in Pamplona to watch the running of the bulls and the bullfights.")
            details2 = Bookdetails(None, 2, "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Huckleberry_Finn_book.JPG/220px-Huckleberry_Finn_book.JPG", "Adventures of Huckleberry Finn (or, in more recent editions, The Adventures of Huckleberry Finn) is a novel by Mark Twain, first published in the United Kingdom in December 1884 and in the United States in February 1885.")
            insert_book(app.config['dsn'], book1)
            insert_book(app.config['dsn'], book2)

            insert_book_details(cursor, details1)
            insert_book_details(cursor, details2)

            quote1 = Quote(0, "you can't get away from yourself by moving from one place to another.", 1, 1)
            quote2 = Quote(0, "All right, then, I'll go to hell.", 2, 2)

            insert_quote(cursor, quote1)
            insert_quote(cursor, quote2)
            feedtype=FeedType(1,'adlı kitabı beğendi')
            insert_feedtype(cursor,feedtype)
            feedtype=FeedType(2,'adlı kitabı önerdi')
            insert_feedtype(cursor,feedtype)
            feedtype=FeedType(3,'adlı kitaba yorum yaptı')
            insert_feedtype(cursor,feedtype)
            feed=Feed(1,datetime.datetime.now(),1,1,1)
            insert_feed(cursor,feed)
            feed=Feed(2,datetime.datetime.now(),1,1,2)
            insert_feed(cursor,feed)
            feed=Feed(3,datetime.datetime.now(),1,1,3)
            insert_feed(cursor,feed)


        except dbapi2.Error as e:
            print(e.pgerror)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        print(e.pgerror)
        connection.rollback()
    finally:
        connection.commit()
        connection.close()

    logout()
    return redirect(url_for('home_page'))

#Ridvan's Part
##############

#Elif's Part
@app.route('/login',methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                error = None
                if "login-submit" in request.form:
                    username = request.form['username']
                    getUser(cursor, username)
                    if cursor.rowcount > 0:
                        ((userid,salt,hash,usertypeid),) =  cursor.fetchall()
                    else:
                        return render_template('login.html', isAlert = True, alertMessage = 'Username or password is invalid.')
                    password = request.form['password']
                    createdHash = createHash(salt,password)
                    if hash == createdHash:
                        session['logged_in'] = True
                        session['userId'] = userid
                        session['username'] = username
                        if usertypeid == 1:
                            session['isAdmin'] = True
                        else:
                            session['isAdmin'] = False
                        return redirect(url_for('home_page'))
                    else:
                        return render_template('login.html', isAlert = True, alertMessage = 'Username or password is invalid.')

                elif "register-submit" in request.form:
                    salt = createRandomSalt()
                    getUserType(cursor,'User')
                    ((typeid),) = cursor.fetchall()
                    if request.form['password'] == request.form['confirm-password']:
                        insert_siteuser(cursor,User(0,request.form['username'], request.form['password'], salt, createHash(salt,request.form['password']),request.form['email'],request.form['name'],request.form['surname'],typeid))
                        return redirect(url_for('home_page'))
                    else:
                        return render_template('login.html', isAlert = True, alertMessage = 'Passwords mismatched.')
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    elif 'logged_in' in session and session['logged_in'] == True:
        return redirect(url_for('home_page'))
    else:
        return render_template('login.html',isAlert = False, alertMessage = '')

@app.route('/logout')
def logout_page():
    if 'logged_in' in session and session['logged_in'] == True:
        session['logged_in'] = False
        session['isAdmin'] = False
        session['username'] = ''
        session['userId'] = 0
    return redirect(url_for('home_page'))

@app.route('/profile', methods=['GET', 'POST'])
def profile_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                userId = request.args.get('userid', 0, type=int)
                if userId == 0:
                    userId = session['userId']
                    mIsFollowing = False
                elif userId != 0 and userId != session['userId']:
                    isFollowing(cursor,session['userId'],userId)
                    if cursor.rowcount > 0:
                        mIsFollowing = True
                    else:
                        mIsFollowing = False
                else:
                    mIsFollowing = False
                getUserById(cursor,userId)
                mUser = cursor.fetchone()
                getUserFollowings(cursor,userId)
                mFollowingCount = cursor.rowcount
                mFollowings = cursor.fetchall()
                getUserFollowers(cursor,userId)
                mFollowerCount = cursor.rowcount
                mFollowers = cursor.fetchall()
                if cursor.rowcount > 0:
                   for i in range(0,len(mFollowers)):
                        isFollowing(cursor,session['userId'],mFollowers[i][0])
                        if cursor.rowcount > 0:
                            mFollowers[i] = mFollowers[i] + (True,)
                        else:
                            mFollowers[i] = mFollowers[i] + (False,)
                return render_template('profile.html',user = mUser, followingCount = mFollowingCount, followerCount = mFollowerCount, followers = mFollowers,  followings = mFollowings, isFollowed = mIsFollowing)
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect(url_for('about_page'))

@app.route('/events', methods=['GET'])
def events_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                getAllEventsWithStrMonth(cursor)
                mEvents = cursor.fetchall()
                return render_template('events.html',events = mEvents)
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect('home_page')
@app.route('/admin/events', methods=['GET', 'POST'])
def adminevents_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'POST' and 'delete' in request.form:
                    deleteEvent(cursor,request.form['deleteid'])
                getAllEvents(cursor)
                mEvents = cursor.fetchall()
                return render_template('adminevents.html',events = mEvents)
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect(url_for('home_page'))

@app.route('/admin/eventadd',methods=['GET', 'POST'])
def eventAdd_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'POST':
                    if "add" in request.form:
                        event= Event(0,request.form['date'],request.form['name'],request.form['organizer'])
                        insertEvent(cursor,event)
                        return redirect(url_for('adminevents_page'))
                else:
                    return render_template('eventadd.html')
            except dbapi2.Error as e:
                    print(e.pgerror)
            finally:
                    cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return render_template('eventadd.html')
    else:
        return redirect(url_for('home_page'))

@app.route('/admin/eventupdate',methods=['GET', 'POST'])
def eventUpdate_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    eventid = request.args.get('id',0,int)
                    if eventid == 0:
                        return redirect(url_for('adminevents_page'))
                    getEventById(cursor,eventid)
                    ((id,name,date,organizer),) = cursor.fetchall()
                    mEvent = Event(id,name,date,organizer)
                    return render_template('eventupdate.html',event = mEvent)
                elif request.method == 'POST':
                    if 'update' in request.form:
                        event = Event(request.form['eventid'],request.form['date'],request.form['name'],request.form['organizer'])
                        updateEvent(cursor,event)
                    return redirect(url_for('adminevents_page'))
            except dbapi2.Error as e:
                    print(e.pgerror)
            finally:
                    cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return render_template('eventupdate.html')
    else:
        return redirect(url_for('about_page'))


@app.route('/_follow')
def followPage():
    followid = request.args.get('followid', 0, type=int)
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor =connection.cursor()
        try:
            follow(cursor,session['userId'],followid)
            return jsonify(result=True)
        except dbapi2.Error as e:
            print(e.pgerror)
            return jsonify(result=False)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        return jsonify(result=False)
    finally:
        connection.commit()
        connection.close()
    return jsonify(result=False)
@app.route('/_unfollow')
def unfollowPage():
    followid = request.args.get('followid', 0, type=int)
    connection = dbapi2.connect(app.config['dsn'])
    try:
        cursor =connection.cursor()
        try:
            unfollow(cursor,session['userId'],followid)
            return jsonify(result=True)
        except dbapi2.Error as e:
            print(e.pgerror)
            return jsonify(result=False)
        finally:
            cursor.close()
    except dbapi2.Error as e:
        return jsonify(result=False)
    finally:
        connection.commit()
        connection.close()
    return jsonify(result=False)
@app.route('/admin/users',methods=['GET', 'POST'])
def users_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'POST':
                    if "edit" in request.form:
                        userid = request.form['editid']

                    elif "delete" in request.form:
                        userid = request.form['deleteid']
                        deleteUser(cursor,str(userid))
                    getAllUsers(cursor)
                    mUsers = cursor.fetchall()
                    return render_template('users.html',users=mUsers)
                else:
                    if 'q' in request.args:
                        searchUsers(cursor,request.args['q'])
                        mUsers = cursor.fetchall()
                    else:
                        getAllUsers(cursor)
                        mUsers = cursor.fetchall()
                    return render_template('users.html',users=mUsers)
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect(url_for('about_page'))

@app.route('/admin/useradd',methods=['GET', 'POST'])
def userAdd_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'POST':
                    if "add" in request.form:
                        salt = createRandomSalt()
                        hash = createHash(salt,request.form['password'])
                        user = User(0,request.form['username'],request.form['password'],salt,hash,request.form['email'],request.form['name'],request.form['surname'],request.form['usertypeid'])
                        insert_siteuser(cursor,user)
                        return redirect(url_for('users_page'))
                else:
                    getAllUserTypes(cursor)
                    mUserTypes = cursor.fetchall()
                    return render_template('useradd.html',userTypes = mUserTypes)
            except dbapi2.Error as e:
                    print(e.pgerror)
            finally:
                    cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect(url_for('about_page'))

@app.route('/admin/userupdate',methods=['GET', 'POST'])
def userUpdate_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    userid = request.args.get('id')
                    getUserById(cursor,userid)
                    ((id,username,salt,hash,email,name,surname,usertypeid),) = cursor.fetchall()
                    mUser = User(id,username,"",salt,hash,email,name,surname,usertypeid)
                    getAllUserTypes(cursor)
                    mUserTypes = cursor.fetchall()
                    return render_template('userupdate.html',user = mUser, userTypes = mUserTypes)
                elif request.method == 'POST':
                    if 'update' in request.form:
                        user = User(request.form['userid'],request.form['username'],request.form['password'],request.form['salt'],createHash(request.form['salt'],request.form['password']), request.form['email'],request.form['name'],request.form['surname'],request.form['usertypeid'])
                        updateUser(cursor,user)
                    return redirect(url_for('users_page'))
            except dbapi2.Error as e:
                    print(e.pgerror)
            finally:
                    cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return render_template('userupdate.html')
    else:
        return redirect(url_for('about_page'))

@app.route('/messages',methods=['GET', 'POST'])
@app.route('/messages/<int:messageId>', methods=['GET','POST'])
def messages_page(messageId = 0):
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'GET':
            if messageId != 0:
                connection = dbapi2.connect(app.config['dsn'])
                try:
                    cursor =connection.cursor()
                    try:
                        comingFromSent = request.args.get('fromSent',False,bool)
                        if comingFromSent == False:
                          changeMessageReadStatus(cursor,messageId,True)
                        getMessage(cursor,messageId)
                        mMessage = cursor.fetchone()
                        return render_template('messagedetail.html',isAlert = False, alertMessage = '',message = mMessage)
                    except dbapi2.Error as e:
                            print(e.pgerror)
                    finally:
                            cursor.close()
                except dbapi2.Error as e:
                    print(e.pgerror)
                    connection.rollback()
                finally:
                    connection.commit()
                    connection.close()
            else:
                connection = dbapi2.connect(app.config['dsn'])
                try:
                    cursor =connection.cursor()
                    try:
                        getReceivedMessages(cursor,session['userId'])
                        mReceivedMessages = cursor.fetchall()
                        mUnreadMessageCount = 0
                        for message in mReceivedMessages:
                            if message[4] == False:
                                mUnreadMessageCount = mUnreadMessageCount + 1
                        getSentMessages(cursor,session['userId'])
                        mSentMessages = cursor.fetchall()
                        return render_template('messages.html',isAlert = False, alertMessage = '',receivedMessages = mReceivedMessages, sentMessages = mSentMessages)
                    except dbapi2.Error as e:
                            print(e.pgerror)
                    finally:
                            cursor.close()
                except dbapi2.Error as e:
                    print(e.pgerror)
                    connection.rollback()
                finally:
                    connection.commit()
                    connection.close()
        elif 'sendMessage' in request.form:
            connection = dbapi2.connect(app.config['dsn'])
            try:
                cursor =connection.cursor()
                try:
                    getUser(cursor,request.form['receiverUserName'])
                    if cursor.rowcount > 0:
                        ((receiver),) = cursor.fetchall()
                        message = Message(0,session['userId'],receiver[0],request.form['message'],False)
                        insertUserMessage(cursor,message)
                        getReceivedMessages(cursor,session['userId'])
                        mReceivedMessages = cursor.fetchall()
                        mUnreadMessageCount = 0
                        for message in mReceivedMessages:
                           if message[4] == False:
                               mUnreadMessageCount = mUnreadMessageCount + 1
                        getSentMessages(cursor,session['userId'])
                        mSentMessages = cursor.fetchall()
                        return render_template('messages.html',isAlert = False, alertMessage = '',receivedMessages = mReceivedMessages, sentMessages = mSentMessages)
                    else:
                        getReceivedMessages(cursor,session['userId'])
                        mReceivedMessages = cursor.fetchall()
                        mUnreadMessageCount = 0
                        for message in mReceivedMessages:
                           if message[4] == False:
                                mUnreadMessageCount = mUnreadMessageCount + 1
                        getSentMessages(cursor,session['userId'])
                        mSentMessages = cursor.fetchall()
                        return render_template('messages.html', isAlert = True, alertMessage = 'Could not find specified user.',receivedMessages = mReceivedMessages, sentMessages = mSentMessages)
                except dbapi2.Error as e:
                        print(e.pgerror)
                finally:
                        cursor.close()
            except dbapi2.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
            return render_template('messages.html')
        elif 'delete' in request.form:
            connection = dbapi2.connect(app.config['dsn'])
            try:
                cursor =connection.cursor()
                try:
                    messageId = request.form['mid']

                    deleteUserMessage(cursor,messageId)

                    getReceivedMessages(cursor,session['userId'])
                    mReceivedMessages = cursor.fetchall()

                    getSentMessages(cursor,session['userId'])
                    mSentMessages = cursor.fetchall()
                    return render_template('messages.html', isAlert = False, alertMessage = '',receivedMessages = mReceivedMessages, sentMessages = mSentMessages)
                except dbapi2.Error as e:
                        print(e.pgerror)
                finally:
                        cursor.close()
            except dbapi2.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
            return render_template('messages.html')

    else:
        return redirect(url_for('about_page'))

##############
@app.route('/', methods=['GET', 'POST'])
def home_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    get_all_feeds(cursor)
                    return render_template('home.html', feed = cursor)
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return render_template('home.html')
    else:
        return render_template('aboutus.html')
@app.route('/about')
def about_page():
        return render_template('aboutus.html')
@app.route('/jobs', methods=['GET', 'POST'])
def jobs_page():
    if 'logged_in' in session and session['logged_in'] == True:
        if session['isAdmin'] == True:
            connection = dbapi2.connect(app.config['dsn'])
            try:
                cursor =connection.cursor()
                try:
                    if request.method == 'GET':
                        getAllJobs(cursor)
                        return render_template('jobsadmin.html', jobs = cursor)
                    if request.method == 'POST':
                        if "delete" in request.form:
                            id = request.form['deleteid']
                            deleteJob(cursor,id)
                            return redirect(url_for('jobs_page'))
                except dbapi2.Error as e:
                    print(e.pgerror)
                finally:
                    cursor.close()
            except dbapi2.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
            return render_template('jobsadmin.html')
        else:
            connection = dbapi2.connect(app.config['dsn'])
            try:
                cursor =connection.cursor()
                try:
                    if request.method == 'GET':
                        getAllJobs(cursor)
                        return render_template('jobs.html', jobs = cursor)
                except dbapi2.Error as e:
                    print(e.pgerror)
                finally:
                    cursor.close()
            except dbapi2.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
            return render_template('jobs.html')

    else:
        return redirect(url_for('about_page'))
@app.route('/describeJob', methods=['GET', 'POST'])
def describe_job_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        if request.method == 'POST':
            if "submit" in request.form:
                userId=session['userId']
                date=datetime.datetime.now()
                header=request.form['header']
                description = request.form['description']
                job = Job(0,userId,datetime.date.today(),header,description);
                connection = dbapi2.connect(app.config['dsn'])
                try:
                    cursor =connection.cursor()
                    try:
                      insertJob(cursor,job)
                    except dbapi2.Error as e:
                        print(e.pgerror)
                    finally:
                        cursor.close()
                except dbapi2.Error as e:
                    print(e.pgerror)
                    connection.rollback()
                finally:
                    connection.commit()
                    connection.close()
                return redirect(url_for('jobs_page'))
        return render_template('describeJob.html')
    else:
        return redirect(url_for('about_page'))
@app.route('/updateJob', methods=['GET', 'POST'])
def update_job_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    userid = request.args.get('userid')
                    statement = """SELECT ID, HEADER,DESCRIPTION FROM JOBS WHERE (ID=%(userid)s)"""
                    cursor.execute(statement,{'userid':userid})
                    return render_template('updateJob.html',job=cursor)
                if request.method == 'POST':
                    updateJob(cursor,request.form['header'],request.form['description'],request.form['userid'],datetime.datetime.now())
                    return redirect(url_for('jobs_page'))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()

        return render_template('updateJob.html')
    else:
        redirect(url_for('about_page'))

@app.route('/updatePost', methods=['GET', 'POST'])
def update_post_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    userid = request.args.get('userid')
                    if session['userId']==int(userid):
                        id = request.args.get('id')
                        statement = """SELECT ID, HEADER,TEXT FROM BLOGS WHERE (ID=%(id)s)"""
                        cursor.execute(statement,{'id':id})
                        return render_template('updatePost.html',post=cursor)
                    else:
                        return redirect(url_for('blogs_page'))
                if request.method == 'POST':
                    updatePost(cursor,request.form['text'],request.form['userid'],datetime.datetime.now())
                    return redirect(url_for('blogs_page'))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()

        return render_template('updatePost.html')
    else:
        redirect(url_for('about_page'))

@app.route('/blogs', methods=['GET', 'POST'])
def blogs_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    getAllPosts(cursor)
                    return render_template('blogs.html', blogs = cursor)
                if request.method == 'POST':
                    if "delete" in request.form:
                        id = request.form['deleteid']
                        userid = request.form['userid']
                        if session['userId']==int(userid):
                            deletePost(cursor,id)
                            return redirect(url_for('blogs_page'))
                        else:
                            return redirect(url_for('blogs_page'))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return render_template('blogs.html')
    else:
        return redirect(url_for('about_page'))

@app.route('/writepost', methods=['GET', 'POST'])
def write_post_page():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'POST':
            if "submit" in request.form:

                userId=session['userId']
                date=datetime.datetime.now()
                header="header"
                text = request.form['text']
                blogPost = BlogPost(0,userId,datetime.date.today(),header,text);
                connection = dbapi2.connect(app.config['dsn'])
                try:
                    cursor =connection.cursor()
                    try:
                      insert_blogPost(cursor,blogPost)
                    except dbapi2.Error as e:
                        print(e.pgerror)
                    finally:
                        cursor.close()
                except dbapi2.Error as e:
                    print(e.pgerror)
                    connection.rollback()
                finally:
                    connection.commit()
                    connection.close()
                return redirect(url_for('blogs_page'))
        return render_template('writePost.html')
    else:
        return redirect(url_for('about_page'))
##########ADMIN PAGES##########

@app.route('/admin')
def admin_index():
    ##bu admin sayfasi oldugu icin kullanici admin mi diye kontrol etmek lazim
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        return render_template('admin_index.html')
    else:
        return redirect(url_for('about_page'))
###############################




@app.route('/admin/authors',methods=['GET', 'POST'])
def authoradmin_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        if request.method == 'GET':
            return render_template('authoradmin.html',authors = selectAuthor(app.config['dsn']))
        else:
            if 'Delete' in request.form:
                deleteid = request.form['deleteid']
                deleteAuthor(app.config['dsn'],deleteid)
                return redirect(url_for('authoradmin_page'))
            if  'Update' in request.form:
                updateid = request.form['updateid']
                return render_template('authorupdate.html')

    else:
        return redirect(url_for('about_page'))



@app.route('/admin/authorsAdd',methods=['GET', 'POST'])
def authorAdd_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        if request.method == 'GET':
            return render_template('authoradd.html')
        else:
            if 'Add' in request.form:
                name = request.form['name']
                lastname = request.form['lastname']
                birthyear = request.form['birthyear']
                nationality = request.form['nationality']
                penname = request.form['penname']
                description = request.form['description']
                picture = request.form['picture']
                newauthor = Author(None,name,lastname,birthyear,nationality,penname,description, picture)
                insertAuthor(app.config['dsn'],newauthor)
                return redirect(url_for('authoradmin_page'))
        return render_template('authoradd.html')
    else:
        return redirect(url_for('about_page'))



@app.route('/admin/authorsUpdate',methods=['GET', 'POST'])
def authorupdate_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        if request.method == 'GET':
            updateid = request.args.get('updateid')
            return render_template('authorupdate.html',updateauthor = selectAuthorbyId(app.config['dsn'],updateid))
        else:
            if 'Update' in request.form:
                updateid = request.form['updateid']
                name = request.form['name']
                lastname = request.form['lastname']
                birthyear = request.form['birthyear']
                nationality = request.form['nationality']
                penname = request.form['penname']
                description = request.form['description']
                picture = request.form['picture']
                updateauthor = Author(None,name,lastname,birthyear,nationality,penname,description,picture)
                updateAuthor(app.config['dsn'],updateid,updateauthor)
                return redirect(url_for('authoradmin_page'))
            return render_template('authorupdate.html',updateauthor = selectAuthorbyId(app.config['dsn'],updateid))
    else:
        return redirect(url_for('about_page'))

@app.route('/news',methods=['GET', 'POST'])
def news_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    select_newsdate(cursor)
                    return render_template('news.html', news = cursor)
                if request.method == 'POST':
                    if "delete" in request.form:
                        id = request.form['deleteid']
                        delete_news(cursor,id)
                        return redirect(url_for('news_page'))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
        return render_template('news.html')
    else:
        return redirect(url_for('about_page'))
@app.route('/newsAdd',methods=['GET', 'POST'])
def newsadd_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        if request.method == 'GET':
            return render_template('newsadd.html')
        else:
            if 'Add' in request.form:
                newsheadline = request.form['headline']
                newstext = request.form['text']
                newsdate = request.form['date']
                newnews = News(newstext,newsdate,newsheadline)
                insert_news(app.config['dsn'],newnews)
                return redirect(url_for('newsadmin_page'))
        return render_template('newsadd.html')
    else:
        return redirect(url_for('about_page'))

@app.route('/updatenews', methods=['GET', 'POST'])
def update_news_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    newsdate = request.args.get('newsheadline')
                    statement = """SELECT * FROM NEWS WHERE (newsdate=%(newsdate)s)"""
                    cursor.execute(statement,{'newsheadline':newsheadline})
                    return render_template('updatenews.html',news=cursor)
                if request.method == 'POST':
                    return redirect(url_for('jobs_page'))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()

        return render_template('updateJob.html')
    else:
        return redirect(url_for('about_page'))



@app.route('/authors',methods=['GET', 'POST'])
def authors_page():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('authors.html', authors = selectAuthor(app.config['dsn']))
    else:
        return redirect(url_for('about_page'))

@app.route('/authorpage',methods=['GET', 'POST'])
def authorpage_page():
    if 'logged_in' in session and session['logged_in'] == True:
        authorid = request.args.get('id')
        if request.method == 'GET':
            id = request.args.get('id')
            return render_template('authorpage.html', author = selectAuthorbyId(app.config['dsn'],authorid),comments = selectauthorcomments(app.config['dsn'],authorid))
        else:
            if 'Add' in request.form:
                text=request.form["comment"]
                userid = session['userId']
                print(authorid)
                newcomment = AuthorComment(userid,authorid,text)
                insertauthorcomment(app.config['dsn'],newcomment)
            if 'Delete' in request.form:
                userid =session["userId"]
                commentid = request.form["commentid"]
                ownerid = getauthorcommenterbycommentid(app.config['dsn'],commentid)
                print (userid)
                print (ownerid[0])
                if userid == (ownerid[0]):
                    deleteauthorcommentbyid(app.config['dsn'],commentid)
        return render_template('authorpage.html', author = selectAuthorbyId(app.config['dsn'],authorid),comments = selectauthorcomments(app.config['dsn'],authorid))
    else:
        return redirect(url_for('about_page'))


@app.route('/groups',methods=['GET', 'POST'])
def groups_page():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('groups.html',groups = selectGroup(app.config['dsn']))
        else:
            if 'Add' in request.form:
                name = request.form['groupname']
                group = Group(None,name)
                insert_group(app.config['dsn'],group)
                return render_template('groups.html',groups = selectGroup(app.config['dsn']))
            if 'Delete' in request.form:
                id=request.form['id']
                deleteGroup(app.config['dsn'],id)
                return render_template('groups.html',groups = selectGroup(app.config['dsn']))
            if 'Update' in request.form:
                id=request.form['id']
                newname = request.form['newname']
                newgroup = Group(id,newname)
                updateGroup(app.config['dsn'],id,newgroup)
                return render_template('groups.html',groups = selectGroup(app.config['dsn']))
            if 'Join' in request.form:
                groupid=request.form['id']
                memberid = session['userId']
                members = selectMember(app.config['dsn'],memberid,groupid)
                if members is None:
                    insert_member(app.config['dsn'],memberid,groupid)
                return render_template('groups.html',groups = selectGroup(app.config['dsn']))
            if 'Visit' in request.form:
                groupid=request.form['id']
                session["group"] = groupid
                return redirect(url_for('grouppage_page'));

    else:
        return redirect(url_for('about_page'))

@app.route('/grouppage',methods=['GET', 'POST'])
def grouppage_page():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'GET':
            groupid = session["group"];
            return render_template('grouppage.html',comments = selectcomments(app.config['dsn'],groupid),membernames = getmembersbyjoin(app.config['dsn'],groupid))

        else:
            if 'Add' in request.form:
                comment=request.form["comment"]
                userid =session["userId"]
                groupid = session["group"];
                newcomment = Comment(userid,groupid,comment)
                insertcomment(app.config['dsn'],newcomment)
            if 'Delete' in request.form:
                userid =session["userId"]
                commentid = request.form["commentid"]
                ownerid = getcommenterbycommentid(app.config['dsn'],commentid)
                print (userid)
                print (ownerid[0])
                if userid == (ownerid[0]):
                    deletecommentbyid(app.config['dsn'],commentid)
            groupid = session["group"];
            return render_template('grouppage.html',comments = selectcomments(app.config['dsn'],groupid),membernames = getmembersbyjoin(app.config['dsn'],groupid))
    else:
        return redirect(url_for('about_page'))



@app.route('/genres',methods=['GET', 'POST'])
def genres_page():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('genres.html',genres  = selectGenre(app.config['dsn']))
        else:
            if 'Add' in request.form:
                name = request.form['genrename']
                genre = Genre(None,name)
                insert_genre(app.config['dsn'],genre)
                return render_template('genres.html',genres = selectGenre(app.config['dsn']))
            if 'Delete' in request.form:
                id=request.form['id']
                deleteGenre(app.config['dsn'],id)
                return render_template('genres.html',genres = selectGenre(app.config['dsn']))
            if 'Update' in request.form:
                id=request.form['id']
                newname = request.form['newname']
                newgenre = Genre(id,newname)
                updateGenre(app.config['dsn'],id,newgenre)
                return render_template('genres.html',genres = selectGenre(app.config['dsn']))
    else:
        return redirect(url_for('about_page'))



@app.route('/bookpage', methods=['GET', 'POST'])
def book_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    return render_template('bookpage.html',books = selectBookwithJoin(app.config['dsn']))
                else:
                    if 'Book' in request.form:
                        gobookid = request.form['id']
                        details = get_book_fulldetails_byId(cursor, gobookid)
                        return render_template('book.html',details = get_book_fulldetails_byId(cursor, gobookid), title = details[0][1])
                    if 'Like' in request.form:
                        feed=Feed(None,datetime.datetime.now(),int(session['userId']),int(request.form['id']),1)
                        checkfeeded = check_if_feeded(cursor, feed)
                        if checkfeeded[0] != 0:
                            insert_feed(cursor, feed)
                        return render_template('bookpage.html',books = selectBookwithJoin(app.config['dsn']))
                    if 'Suggest' in request.form:
                        feed=Feed(None,datetime.datetime.now(),int(session['userId']),int(request.form['id']),2)
                        checkfeeded = check_if_feeded(cursor, feed)
                        if checkfeeded[0] != 0:
                            insert_feed(cursor, feed)
                        return render_template('bookpage.html',books = selectBookwithJoin(app.config['dsn']))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect(url_for('about_page'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        cursor =connection.cursor()
        if request.method == 'GET':
            return render_template('book.html',details = get_book_fulldetails(cursor))
        else:
            if 'Book' in request.form:
                gobookid = request.form['id']
                return render_template('book.html',details = get_book_fulldetails_byId(cursor, gobookid))

    else:
        return redirect(url_for('about_page'))


@app.route('/admin/books',methods=['GET', 'POST'])
def books_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        cursor =connection.cursor()
        if request.method == 'GET':
            return render_template('bookadmin.html', books = selectBookwithJoin(app.config['dsn']))
        else:
            if 'Delete' in request.form:
                deleteid = request.form['deleteid']
                deleteBook(app.config['dsn'],deleteid)
                return redirect(url_for('books_page'))
            if 'Update' in request.form:
                updateid = request.form['updateid']
                return render_template('bookupdate.html')
            if 'Details' in request.form:
                detailid = request.form['detailid']
                return render_template('bookdetails.html')



    else:
        return redirect(url_for('about_page'))

@app.route('/admin/bookadd',methods=['GET', 'POST'])
def bookAdd_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        cursor =connection.cursor()
        if request.method == 'GET':
            return render_template('bookadd.html', authorlist = selectAuthor(app.config['dsn']), genrelist = selectGenre(app.config['dsn']))
        else:
            try:
                try:
                    if request.method == 'GET':
                        return render_template('bookadd.html')
                    else:
                        if "Add" in request.form:
                            title = request.form['title']
                            year = request.form['year']
                            author_text = request.form['author_id']
                            author = author_text.split()
                            author_count = len(author)
                            author_name = ""
                            for x in range (0, author_count-1):
                                author_name = author_name + author[x] + ' '
                            genre_text = request.form['genre_id']
                            statement = """SELECT ID FROM GENRES WHERE NAME = %s"""
                            cursor.execute(statement,(genre_text,))
                            genre_id = cursor.fetchall()

                            statement = """SELECT ID FROM AUTHORS WHERE NAME = %s AND LASTNAME = %s"""
                            cursor.execute(statement,(author[0],author[author_count-1]))
                            author_id = cursor.fetchall()
                            book = Book(None, title, year, author_id[0], genre_id[0])
                            insert_book(app.config['dsn'],book)

                            bookid = selectBookbyTitle(app.config['dsn'], title)
                            bookDetail = Bookdetails(None, bookid[0][0], "http://publications.iarc.fr/uploads/media/default/0001/02/thumb_1240_default_publication.jpeg", "Not available")
                            insert_book_details(cursor, bookDetail)
                            return redirect(url_for('books_page'))
                except dbapi2.Error as e:
                        print(e.pgerror)
            except dbapi2.Error as e:
                print(e.pgerror)
                connection.rollback()
            finally:
                connection.commit()
                connection.close()
            return render_template('bookadd.html')
    else:
        return redirect(url_for('about_page'))

@app.route('/admin/bookdetails',methods=['GET', 'POST'])
def bookDetails_page():
    if 'logged_in' in session and session['logged_in'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        try:
            cursor =connection.cursor()
            try:
                if request.method == 'GET':
                    detailid = request.args.get('detailid')
                    return render_template('bookdetails.html',detailbook = get_book_alldetails_byId(cursor,detailid))

                else:
                    if 'Update' in request.form:
                        detailid = request.form['detailid']
                        bookid = request.form['bookid']
                        imgurl = request.form['imgurl']
                        details = request.form['details']
                        updateDetail = Bookdetails(None, bookid, imgurl, details)
                        update_book_details(cursor, bookid, updateDetail)
                        return redirect(url_for('books_page'))
                    else:
                        return redirect(url_for('books_page'))
                    return render_template('bookdetails.html',detailbook = get_book_alldetails_byId(cursor,detailid))
            except dbapi2.Error as e:
                print(e.pgerror)
            finally:
                cursor.close()
        except dbapi2.Error as e:
            print(e.pgerror)
            connection.rollback()
        finally:
            connection.commit()
            connection.close()
    else:
        return redirect(url_for('about_page'))

@app.route('/admin/bookupdate',methods=['GET', 'POST'])
def bookUpdate_page():
    if 'logged_in' in session and session['logged_in'] == True and session['isAdmin'] == True:
        connection = dbapi2.connect(app.config['dsn'])
        cursor =connection.cursor()
        if request.method == 'GET':
            updateid = request.args.get('updateid')
            return render_template('bookupdate.html',updatebook = selectBookbyIDwithJoin(app.config['dsn'],updateid))

        else:
            if 'Update' in request.form:
                updateid = request.form['updateid']
                title = request.form['title']
                year = request.form['year']
                author_text = request.form['author_id']
                author = author_text.split()
                author_count = len(author)
                author_name = ""
                for x in range (0, author_count-1):
                    author_name = author_name + author[x] + ' '
                genre_text = request.form['genre_id']
                statement = """SELECT ID FROM GENRES WHERE NAME = %s"""
                cursor.execute(statement,(genre_text,))
                genre_id = cursor.fetchall()

                statement = """SELECT ID FROM AUTHORS WHERE NAME = %s AND LASTNAME = %s"""
                cursor.execute(statement,(author[0],author[author_count-1]))
                author_id = cursor.fetchall()
                updatebook = Book(None, title, year, author_id[0], genre_id[0])
                updateBook(app.config['dsn'], updateid, updatebook)
                return redirect(url_for('books_page'))
            else:
                return redirect(url_for('books_page'))
            return render_template('bookupdate.html',updatebook = selectBookbyIDwithJoin(app.config['dsn'],updateid))

    else:
        return redirect(url_for('about_page'))

def logout():
    session['logged_in'] = False;
    session['username'] = "";
    session['isAdmin'] = False;

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

# set the secret key.  keep this really secret:
app.secret_key = '+_9o$w9+9xro!-y(wvuv+vvyc!$x(@ak(!oh@ih0ul%+6cf=$f'

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    #This part is logins the infos
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)
