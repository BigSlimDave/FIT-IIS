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
    if ( request.method == "GET" ):
        account = session
        table_head = db_describe(table)
        return render_template('admin/admin_table_add.html', account=account, table_name=table, header=table_head)
    else:
        validation = {}
        table_head = db_describe(table)
        for i in table_head:
            validation[i[0]] = i[1]
        for i in request.form:
            if ( i == "Odeslat"):
                continue
            print(validation[i])
            if ( not check_database_type(validation[i],request.form[i]) ):
                flash(i + " " + validation[i])
                return redirect(url_for("add"))
            
        db_insert_what(table, request.form)
        return redirect(url_for("admin.show_table", table_name = table))

@admin.route('/<table>/remove/', methods=['POST'])
@login_required('admin')
def remove_row(table):
    print request.form['remove_row']
    if 'remove_row' in request.form:
        db, cursor = database()
        cursor.execute("DELETE FROM %s WHERE id=%s" % (table, request.form['remove_row'],))
        db.commit()
        return redirect(url_for("admin.show_table", table_name = table))
    else:
        flash('Něco se pokazilo')
        return redirect(url_for("admin.show_table", table_name = table))

@admin.route('/<table>/edit/<int:row>', methods=['GET', 'POST'])
@login_required('admin')
def edit_row(table, row):
    if 'Upravit' in request.form or request.method == 'GET':
        content = db_get_from_where_one(table, "id='{0}'".format(row), ['*'])
        table_head = db_describe(table)
        return render_template('admin/admin_table_edit.html', content=content, account=session, header=table_head, table_name=table)
    elif 'Odeslat' in request.form:
        if db_update_where_what(table, "id='{0}'".format(row), request.form) == True:
            return redirect(url_for('admin.index'))
        else:
            return "chyba databaze"
    else: # POST
        pass