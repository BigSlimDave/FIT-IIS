# -*- encoding: UTF-8 -*-

from functools import wraps
from flask import request, redirect, session, render_template, abort, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import MySQLdb

def database():
    db = MySQLdb.connect(   host="localhost",   # your host, usually localhost
                            user="root",        # your username
                            passwd="root",      # your password
                            db="content")       # name of the data base
    return db, db.cursor()

def db_get_from_all(_from, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s" % (what, _from))
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_get_from_one(_from, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s" % (what, _from))
    content = cursor.fetchone()[0]
    db.commit()
    db.close()
    return content

def db_get_from_where_all(_from, where, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s WHERE %s" % (what, _from, where))
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_get_from_where_one(_from, where, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s WHERE %s" % (what, _from, where))
    content = cursor.fetchone()
    db.commit()
    db.close()
    print content
    return content

def db_describe(table_name):
    db, cursor = database()
    cursor.execute("DESCRIBE %s" % table_name)
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def login_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            form = loginForm(request.form)
            if request.method == 'GET':
                if 'logged' in session:
                    if session['logged'] == role or session['logged'] == 'admin':
                        return f(*args, **kwargs)
                    else:
                        abort(403)
                else:
                    flash('Pro zobrázení se musíte přihlásit.')
                    return render_template('login.html', form=form)
            else: # POST
                if 'password' in request.form:
                    content = db_get_from_where_one('uzivatele', "prezdivka='{0}'".format(request.form['username']), ['heslo', 'role'])
                    hash1 = content[0]
                    role1 = content[1]
                    if sha256_crypt.verify(request.form['password'], hash1):
                        session['username'] = request.form['username']
                        session['logged'] = role1
                        if session['logged'] == role or session['logged'] == 'admin':
                            return f(*args, **kwargs)
                        else:
                            abort(403)
                    else:
                        flash('Přihlášení se nezdařilo, opakujte ho prosím.')
                        return render_template('login.html', form=form)
                elif 'logout' in request.form:
                    session.pop('logged')
                    session.pop('username')
                    return redirect('/')
                else:
                    flash('Neznámý požadavek.')
                    return render_template('login.html', form=form)
        return decorated_function
    return decorator

class loginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Heslo', [validators.DataRequired()])