# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from jinja2 import TemplateNotFound
from app.functions import *

profil = Blueprint('profil', __name__, static_folder='static', template_folder='templates')

@profil.route('/', methods=['GET', 'POST'])
@login_required('user')
def index():
    account = session
    uzivatel = db_get_from_where_one('uzivatele', "prezdivka='{0}'".format(session['username']), ['*'])
    hrac = db_get_from_where_one('hrac', "prezdivka='{0}'".format(session['username']), ['*'])
    vybaveni = db_get_from_where_all('vybaveni', "vlastnik='{0}'".format(hrac[0]), ['*'])
    tym = db_get_from_where_one('tym_clenstvi', "hrac='{0}'".format(hrac[0]), ['id'])
    if tym != None:
        tym = db_get_from_where_one('tym', "id='{0}'".format(id_tym), ['*'])
    klan = db_get_from_where_one('klan_clenstvi', "hrac='{0}'".format(hrac[0]), ['id'])
    if klan != None:
        klan = db_get_from_where_one('klan', "id='{0}'".format(id_tym), ['*'])
    specializace = db_get_from_where_one('specializace', "hrac='{0}'".format(hrac[0]), ['hra'])
    return render_template('profil/index.html', account=account, uzivatel=uzivatel, hrac=hrac, vybaveni=vybaveni, tym=tym, klan=klan, specializace=specializace)

