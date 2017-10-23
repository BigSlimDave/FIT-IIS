# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from jinja2 import TemplateNotFound
from app.functions import *

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

@admin.route('/', methods=['GET', 'POST'])
@login_required('admin')
def index():
    return render_template('admin/index.html', account=session, table='')

@admin.route('/<string:table_name>/', methods=['GET', 'POST'])
@login_required('admin')
def show_table(table_name):
    account = session
    table_head = db_describe(table_name)
    content = db_get_from_all(table_name, ['*'])
    return render_template('admin/index.html', account=account, table_name=table_name, content=content, table_head=table_head)

@admin.route('/<table>/add/', methods=['GET', 'POST'])
@login_required('admin')
def add(table):
    return "add"

@admin.route('/<table>/remove/', methods=['POST'])
@login_required('admin')
def remove_row(table):
    print request.form['remove_row']
    if 'remove_row' in request.form:
        db, cursor = database()
        cursor.execute("DELETE FROM %s WHERE id=%s" % (table, request.form['remove_row'],))
        db.commit()
        return redirect(url_for('index'))
    else:
        flash('Něco se pokazilo')
        return redirect(url_for('index'))

@admin.route('/<table>/edit/<int:row>', methods=['GET', 'POST'])
@login_required('admin')
def edit_row(table, row):
    if request.method == 'GET':
        content = db_get_from_where_one(table, "id='{0}'".format(row), ['*'])
        table_head = db_describe(table)
        return render_template('admin/admin_table_edit.html', content=content, account=session, header=table_head, table_name=table)
    else: # POST