# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from jinja2 import TemplateNotFound
from app.functions import *

user = Blueprint('user', __name__, static_folder='static', template_folder='templates')

@user.route('/', methods=['GET', 'POST'])
@login_required('user')
def index():
    account = session
    return render_template('user/index.html', account=account, table='')

@user.route('/<string:table_name>/', methods=['GET', 'POST'])
@login_required('user')
def show_table(table_name):
    account = session
    content = db_get_from_all(table_name, ['*'])
    return render_template('user/index.html', account=account, table_name=table_name, content=content)
