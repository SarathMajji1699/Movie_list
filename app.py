from flask import request, Flask, render_template, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import io
import time
import psycopg2
import datetime

msg=''

app = Flask(__name__)
app.secret_key = "abc"

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/depressiondata'
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://enrxzrvkxwalhw:e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004@ec2-34-194-123-31.compute-1.amazonaws.com:5432/d5cqorf0129ro1'

    # "dbname=d5cqorf0129ro1 host=ec2-34-194-123-31.compute-1.amazonaws.com port=5432 user=enrxzrvkxwalhw password=e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004 sslmode=require"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Movies(db.Model):
    __tablename__ = 'movies'
    movie = db.Column(db.Text(), primary_key=True)
    mcheck = db.Column(db.Boolean())
    mstrike = db.Column(db.Boolean())
    ts = db.Column(db.DateTime)


    def __init__(self, movie,mcheck,mstrike,ts):
        self.movie = movie
        self.mcheck = mcheck
        self.mstrike = mstrike
        self.ts = ts

class Mcheck(db.Model):
    __tablename__ = 'mcheck'
    movie = db.Column(db.Text(), primary_key=True)


    def __init__(self, movie):
        self.movie = movie


def movielist():
    try:
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("SELECT movie,mcheck,mstrike,ts FROM Movies ORDER BY ts")
        movielist=cursor.fetchall()
        cnt=1
        mlist={}
        for m,c,s,t in movielist:
            mlist[cnt]=(m,c,s,t)
            # print(mlist[cnt])
            cnt+=1
        # print(movielist)
        return mlist

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")


def mdelete(mdname):
    try:
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Movies WHERE movie=%s",(mdname,))
        connection.commit()
        return "Movie deleted successfully from the list !"
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")

def madd(maname):
    try:
        x= maname.lower()
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("SELECT movie FROM Movies WHERE LOWER(movie)=%s",(x,))
        check = cursor.fetchone()
        if check:
            return "Movie name already exists in the list !"
        else:
            # cursor.execute("INSERT INTO Movies (movie) VALUES (%s)" ,(maname,))
            cursor.execute("INSERT INTO Movies (movie,mcheck,mstrike,ts) VALUES (%s,%s,%s,%s)" ,(maname,'0','0',datetime.datetime.now()))
            connection.commit()
            # print("Added")
            return "Movie added successfully to the list !"
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")

def checkstatus(cmovie):
    try:
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("SELECT mcheck FROM Movies WHERE movie=%s",(cmovie,))
        s=cursor.fetchone()
        # print(s[0],'*******')
        if s[0]:
            cursor.execute("UPDATE Movies SET mcheck = %s WHERE  movie=%s",('0',cmovie))
        else:
            cursor.execute("UPDATE Movies SET mcheck = %s WHERE  movie=%s",('1',cmovie))

        return

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")


def strikestatus(smovie):
    try:
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("SELECT mstrike FROM Movies WHERE movie=%s",(smovie,))
        s=cursor.fetchone()
        # print(s[0],'*******')
        if s[0]:
            cursor.execute("UPDATE Movies SET mstrike = %s WHERE  movie=%s",('0',smovie))
        else:
            cursor.execute("UPDATE Movies SET mstrike = %s WHERE  movie=%s",('1',smovie))

        return

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")



def cmovielist():
    try:
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("SELECT movie FROM Mcheck")
        movielist=cursor.fetchall()
        cnt=1
        mlist={}
        for m in movielist:
            mlist[cnt]=(m)
            # print(mlist[cnt])
            cnt+=1
        # print(movielist)
        return mlist

    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")


def cmdelete(mdname):
    try:
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Mcheck WHERE movie=%s",(mdname,))
        connection.commit()
        return "Movie deleted successfully from the list !"
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")

def cmadd(maname):
    try:
        x = maname.lower()
        connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
        cursor = connection.cursor()
        cursor.execute("SELECT movie FROM Mcheck WHERE LOWER(movie)=%s",(x,))
        check = cursor.fetchone()
        if check:
            return "Movie name already exists in the list !"
        else:
            cursor.execute("INSERT INTO Mcheck (movie) VALUES (%s)" ,(maname,))
            connection.commit()
            # print("Added")
            return "Movie added successfully to the list !"
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")



@app.route('/')
def main():
    x = movielist()
    return render_template('index.html', mlist=x)

@app.route('/home')
def home():
    x = movielist()
    global msg
    m=msg
    msg=''
    return render_template('index.html', mlist=x,msg=m)

@app.route('/check')
def check():
    x = cmovielist()
    global msg
    m=msg
    msg=''
    return render_template('check.html', mlist=x,msg=m)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/mldelete/<dname>')
def mldelete(dname):
    global msg
    msg = mdelete(dname)
    return redirect(url_for('home'))


@app.route('/mladd/<aname>')
def mladd(aname):
    global msg
    msg = madd(aname)
    return redirect(url_for('home'))

@app.route('/cmldelete/<dname>')
def cmldelete(dname):
    global msg
    msg = cmdelete(dname)
    return redirect(url_for('check'))


@app.route('/cmladd/<aname>')
def cmladd(aname):
    global msg
    msg = cmadd(aname)
    return redirect(url_for('check'))

@app.route('/moviecheck/<cmovie>')
def moviecheck(cmovie):
    checkstatus(cmovie)
    global msg
    msg=''
    return redirect(url_for('home'))


@app.route('/moviestrike/<smovie>')
def moviestrike(smovie):
    strikestatus(smovie)
    global msg
    msg=''
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run()
