# -*- encoding: UTF-8 -*-

from functools import wraps
from flask import request, redirect, session, render_template, abort, flash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import MySQLdb
import re
import datetime

def database():
    db = MySQLdb.connect(   host="localhost",   # your host, usually localhost
                            user="root",        # your username
                            passwd="root",      # your password
                            db="content",       # name of the data base
                            charset='utf8')
    return db, db.cursor()

def check_database_type(type,data):
    if ( re.match(ur"varchar\((\d+)\)",type) ):
        length = int( re.findall(ur"\d+", type)[0])
        if ( len(data) < length ):
            return True
        else:
            return False;
    elif ( re.match(ur"date",type) ):
        try:
            datetime.datetime.strptime(data,'%Y-%m-%d')
            return True
        except ValueError:
            return False;

def db_get(command):
    db, cursor = database()
    cursor.execute(command)
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_get_from_all(table_name, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s" % (what, table_name))
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_get_from_one(table_name, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s" % (what, table_name))
    content = cursor.fetchone()[0]
    db.commit()
    db.close()
    return content

def db_get_from_where_all(table_name, where, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    cursor.execute("SELECT %s FROM %s WHERE %s" % (what, table_name, where))
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_get_from_where_one(table_name, where, *what):
    for item in what:
        what = ', '.join(item) 
    db, cursor = database()
    print("SELECT %s FROM %s WHERE %s" % (what, table_name, where))
    cursor.execute("SELECT %s FROM %s WHERE %s" % (what, table_name, where))
    content = cursor.fetchone()
    db.commit()
    db.close()
    #print content
    return content

def db_describe(table_name):
    db, cursor = database()
    cursor.execute("DESCRIBE %s" % table_name)
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_update_where_what(table_name, where, *what):
    bla = []
    for i in what[0]:
        if i == 'Odeslat':
            continue
        bla += ["{0}='{1}'".format(i.encode('utf-8'), what[0][i].encode('utf-8'))]
    values = ", ".join(bla)
    db, cursor = database()
    print values
    cursor.execute("UPDATE %s SET %s WHERE %s" % (table_name, values.decode('utf-8'), where))
    db.commit()
    db.close()
    return True

def members_in_clan(id):
    db, cursor = database()
    cursor.execute("SELECT * FROM klan_clenstvi JOIN hrac ON ( hrac.id = klan_clenstvi.hrac ) WHERE klan_clenstvi.klan=%s" % (id))
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def members_in_team(id):
    db, cursor = database()
    cursor.execute("SELECT * FROM tym_clenstvi JOIN hrac ON ( hrac.id = tym_clenstvi.hrac ) WHERE tym_clenstvi.tym =%s" % (id))
    content = cursor.fetchall()
    db.commit()
    db.close()
    return content

def db_insert_what(table_name, *what):
    column_name = []
    values = []
    for i in what[0]:
        if i == 'Odeslat':
            continue
        column_name.append(i.encode('utf-8'))
        values.append("\'" + what[0][i].encode('utf-8') + "\'" )
    values = ", ".join(values)
    column_name = ", ".join(column_name)
    db, cursor = database()
    cursor.execute("INSERT INTO %s (%s) VALUES (%s)" % (table_name, column_name.decode('utf-8'), values.decode('utf-8')))
    db.commit()
    db.close()
    return True

def login_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            form = loginForm(request.form)
            if 'logged' in session:
                if request.method == 'GET':
                        if session['logged'] == role or session['logged'] == 'admin':
                            return f(*args, **kwargs)
                        else:
                            abort(403)
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
                    else:   # Aby prošly ostatní požadavky POST
                        return f(*args, **kwargs)
            else:
                if request.method == 'POST': # POST
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
                    else:   # Aby prošly ostatní požadavky POST
                        return f(*args, **kwargs)
                else:
                    flash('Pro zobrázení se musíte přihlásit.')
                    return render_template('login.html', form=form)

        return decorated_function
    return decorator

class loginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Heslo', [validators.DataRequired()])