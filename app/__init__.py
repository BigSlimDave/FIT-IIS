# -*- encoding: UTF-8 -*-

from flask import Flask, render_template, request, session, redirect, flash
from passlib.hash import sha256_crypt
from app.functions import *

from app.admin.views import admin
from app.user.views import user

app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def not_found(error):
    return "Forbidden 403"

@app.route('/', methods=['GET', 'POST'])
def index():
    form = loginForm(request.form)
    if request.method == 'GET':
        if 'logged' in session:
            return redirect('/'+session['logged'])
        else:
            return render_template('login.html', form=form)
    else: # POST
        if 'password' in request.form:
            content = db_get_from_where_one('uzivatele', "prezdivka='{0}'".format(request.form['username']), ['heslo', 'role', 'id'])
            try:
                hash1 = content[0]
                role1 = content[1]
            except:
                flash('Přihlášení se nezdařilo, opakujte ho prosím.')
                return render_template('login.html', form=form)
            if sha256_crypt.verify(request.form['password'], hash1):
                session['username'] = request.form['username']
                session['logged'] = role1
                session['id'] = content[2]
                return redirect('/'+role1)
            else:
                flash('Přihlášení se nezdařilo, opakujte ho prosím.')
                return render_template('login.html', form=form)
        else:
            flash('Operace se nezdařila')
            return render_template('login.html')


# Blueprints
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(user, url_prefix="/user")
