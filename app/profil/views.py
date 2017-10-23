# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from jinja2 import TemplateNotFound
from app.functions import login_required, loginForm, database

profil = Blueprint('profil', __name__, static_folder='static', template_folder='templates')

@profil.route('/', methods=['GET', 'POST'])
@login_required('user')
def index():
    account = session
    return render_template('profil/index.html', account=account, table='')

