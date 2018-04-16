#! /usr/bin/python3.5
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, g, session, url_for, redirect
import mysql.connector
import hashlib
import requests
from pprint import pprint

#Construct app
app = Flask(__name__)
app.config.from_object('config')
app.config.from_object('secret_config')


#Database functions
def connect_db () :
    g.mysql_connection = mysql.connector.connect(
        host = app.config['DATABASE_HOST'],
        user = app.config['DATABASE_USER'],
        password = app.config['DATABASE_PASSWORD'],
        database = app.config['DATABASE_NAME']
    )

    g.mysql_cursor = g.mysql_connection.cursor()
    return g.mysql_cursor

def get_db () :
    if not hasattr(g, 'db') :
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db (error) :
    if hasattr(g, 'db') :
        g.db.close()


#Pages
@app.route('/')
def index () :
    db = get_db()
    db.execute("SELECT * FROM urls")
    rows = db.fetchall()
    tab = []
    for row in rows:
        tab.append(requests.get(row[1]).status_code)
    return render_template('index.html', rows = rows, tab = tab)

@app.route('/login/', methods = ['GET', 'POST'])
def login () :
    if session.get('user') :
        return redirect(url_for('/'))
    email = str(request.form.get('email'))
    password = hashlib.sha512(str(request.form.get('password')).encode('utf-8')).hexdigest()

    valid_user = False

    db = get_db()
    db.execute('SELECT * from user where email= %s AND password = %s', (email, password))
    user = db.fetchone()

    if user:
        valid_user = True
    else:
        valid_user = False
        redirect(url_for('admin_logout'))

    if valid_user:
        session['user'] = valid_user
        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/admin/', methods = ['GET', 'POST'])
def admin () :
    url = ''
    if not session.get('user') :
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = request.form.get('urlinput')
        db = get_db()
        db.execute("INSERT INTO urls (url) VALUES('"+str(url)+"')")
        g.mysql_connection.commit()
    db = get_db()
    db.execute("SELECT * FROM urls")
    rows = db.fetchall()
    tab = []
    for row in rows:
        tab.append(requests.get(row[1]).status_code)

    return render_template('index_admin.html', user = session['user'], url = url, rows = rows, tab = tab)


@app.route('/admin/logout/')
def admin_logout () :
    session.clear()
    return redirect(url_for('login'))

@app.route('/supprimer_url/<id>/')
def supprimer_url (id) :
    if not session.get('user') :
        return redirect(url_for('login'))
    db = get_db()
    db.execute("DELETE FROM `urls` WHERE id = "+id+" ")
    g.mysql_connection.commit()
    return redirect(url_for('admin'))

@app.route('/modifier_url/<id>/', methods = ['POST', 'GET'])
def modifier_url (id) :
    if not session.get('user') :
        return redirect(url_for('login'))
    if request.method == 'POST':
        url = request.form.get('urlinput')
        db = get_db()
        db.execute("UPDATE `urls` SET `url`= '"+url+"' WHERE id = "+id+" ")
        g.mysql_connection.commit()
        return redirect(url_for('admin'))
    else :
        return render_template('modif_url.html', id=id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

