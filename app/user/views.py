# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from jinja2 import TemplateNotFound
from app.functions import *

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')

@user.route('/', methods=['GET', 'POST'])
@login_required('user')
def index():
    account = session
    return render_template('user/index.html', account=account, table_name='')

@user.route('/hrac/', methods=['GET', 'POST'])
@login_required('user')
def hrac():
    account = session
    database = db_get("""
        SELECT hrac.jmeno, hrac.prezdivka, klan.id, klan.nazev, tym.id, tym.nazev
        FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
                  LEFT JOIN klan          ON ( klan.id = klan_clenstvi.klan ) 
                  LEFT JOIN tym_clenstvi  ON ( hrac.id = tym_clenstvi.hrac  )
                  LEFT JOIN tym           ON ( tym.id  = tym_clenstvi.tym   )""")
    return render_template('user/hrac.html', account=account, table_name='hrac', database=database)

@user.route('/vybaveni/', methods=['GET', 'POST'])
@login_required('user')
def vybaveni():
    account = session
    database = db_get_from_all('vybaveni', ['*'])
    return render_template('user/vybaveni.html', account=account, table_name='hrac', database=database)

@user.route('/hra/', methods=['GET', 'POST'])
@login_required('user')
def hra():
    account = session
    database = db_get_from_all('hra', ['*'])
    return render_template('user/hra.html', account=account, table_name='hrac', database=database)

@user.route('/klan/', methods=['GET', 'POST'])
@login_required('user')
def klan():
    account = session
    database = db_get_from_all('klan', ['*'])
    return render_template('user/klan.html', account=account, table_name='hrac', database=database)

@user.route('/tym/', methods=['GET', 'POST'])
@login_required('user')
def tym():
    account = session
    database = db_get_from_all('tym', ['*'])
    return render_template('user/tym.html', account=account, table_name='hrac', database=database)

@user.route('/zapas/', methods=['GET', 'POST'])
@login_required('user')
def zapas():
    account = session
    database = db_get_from_all('zapas', ['*'])
    return render_template('user/zapas.html', account=account, table_name='hrac', database=database)

@user.route('/turnaj/', methods=['GET', 'POST'])
@login_required('user')
def turnaj():
    account = session
    database = db_get_from_all('turnaj', ['*'])
    return render_template('user/turnaj.html', account=account, table_name='hrac', database=database)

@user.route('/sponzor/', methods=['GET', 'POST'])
@login_required('user')
def sponzor():
    account = session
    database = db_get_from_all('sponzor', ['*'])
    return render_template('user/sponzor.html', account=account, table_name='hrac', database=database)
