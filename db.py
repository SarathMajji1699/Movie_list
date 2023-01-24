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


try:
    connection = psycopg2.connect(user="enrxzrvkxwalhw", password="e316f339af8c34c695acc713942919c488d559a150f81b2a3972abc1e83df004", host="ec2-34-194-123-31.compute-1.amazonaws.com", port="5432", database="d5cqorf0129ro1")
    cursor = connection.cursor()
    # cursor.execute("DROP Table Movies")
    # cursor.execute("INSERT INTO Movies (movie,mcheck,mstrike,ts) VALUES (%s,%s,%s,%s)" ,("WAR3",'0','0',datetime.datetime.now()))
    # cursor.execute("UPDATE Movies SET mcheck = %s WHERE  movie=%s",('0',"WAR"))
    cursor.execute("SELECT movie,mcheck,mstrike,ts FROM Movies ORDER BY ts")
    movielist=cursor.fetchall()
    # print(movielist)
    cnt=1
    mlist={}
    for m,c,s,t in movielist:
        mlist[cnt]=(m,c,s,t)
        print(mlist[cnt])
        cnt+=1
except (Exception, psycopg2.Error) as error:
    print("Failed to connect to the database", error)

finally:
    # closing database connection.
    if connection:
        connection.commit()
        cursor.close()
        connection.close()
        print("Success")
