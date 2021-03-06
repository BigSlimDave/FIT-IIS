# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from jinja2 import TemplateNotFound
from passlib.hash import sha256_crypt
from app.functions import *

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

@admin.route('/', methods=['GET', 'POST'])
@login_required('admin')
def index():
    return redirect(url_for('admin.uzivatele'))
    return render_template('admin/index.html', account=session, table='')

################# uzivatele ###########################
@admin.route('/uzivatele/', methods=['GET', 'POST'])
@login_required('admin')
def uzivatele():
    account = session
    table_head = db_describe("uzivatele")
    content = db_get_from_all("uzivatele", ['*'])
    return render_template('admin/uzivatele.html', account=account, content=content, table_head=table_head, table_name='uzivatele')

@admin.route('/uzivatele/edit/<int:id>/', methods=['GET', 'POST'])
@login_required('admin')
def uzivatele_edit(id):
    if 'Upravit' in request.form or request.method == 'GET':
        content = db_get_from_where_one('uzivatele', "id='{0}'".format(id), ['*'])
        table_head = db_describe('uzivatele')
        return render_template('admin/uzivatele_edit.html', content=content, account=session, header=table_head, table_name='uzivatele')
    elif 'Odeslat' in request.form:
        if db_update_where_what('uzivatele', "id='{0}'".format(id), request.form) == True:
            return redirect(url_for('admin.uzivatele'))
        else:
            flash("chyba databaze")
            return redirect(url_for('admin.uzivatele'))
    else: # POST
        pass

@admin.route('/uzivatele/nove_heslo/<int:id>', methods=['GET', 'POST'])
@login_required('admin')
def uzivatele_heslo(id):
    if 'Heslo' in request.form or request.method == 'GET':
        prezdivka = db_get_from_where_one('uzivatele', "id='{0}'".format(id), ['prezdivka'])[0]
        return render_template('admin/uzivatele_nove_heslo.html', prezdivka=prezdivka, account=session, table_name='uzivatele')
    elif 'heslo' in request.form:
        hashh = sha256_crypt.hash(request.form['heslo'])
        db, cursor = database()
        cursor.execute("UPDATE uzivatele SET heslo='%s' WHERE id=%s" % (hashh, id))
        db.commit()
        db.close()
        return redirect(url_for('admin.uzivatele'))
    else: # POST
        pass

@admin.route('/uzivatele/pridat_uzivatele', methods=['GET', 'POST'])
@login_required('admin')
def uzivatele_pridat():
    print request.form
    if request.method == 'GET':
        return render_template('admin/uzivatele_pridat.html', account=session, table_name='uzivatele')
    elif 'Odeslat' in request.form:
        hashh = sha256_crypt.hash(request.form['heslo'])
        role = request.form['role']
        if role == 'admin':
            db, cursor = database()
            cursor.execute("INSERT INTO uzivatele (prezdivka, heslo, role) VALUES ('%s', '%s', '%s')" % (request.form['prezdivka'], hashh, role))
            db.commit()
            db.close()
        else:
            db, cursor = database()
            cursor.execute("INSERT INTO uzivatele (prezdivka, heslo, role) VALUES ('%s', '%s', '%s')" % (request.form['prezdivka'], hashh, role))
            db.commit()
            cursor.execute("INSERT INTO hrac (prezdivka, jmeno, odberatel) VALUES ('%s', '%s', %s)" % (request.form['prezdivka'], request.form['jmeno'], 1))
            db.commit()
            db.close()
        return redirect(url_for('admin.uzivatele'))
    else: # POST
        pass

@admin.route('/uzivatele/remove/', methods=['POST'])
@login_required('admin')
def uzivatele_remove():
    print request.form['remove_row']
    if 'remove_row' in request.form:
        db, cursor = database()
        cursor.execute("DELETE FROM %s WHERE id=%s" % ('uzivatele', request.form['remove_row'],))
        db.commit()
        return redirect(url_for("admin.uzivatele"))
    else:
        flash('Něco se pokazilo')
        return redirect(url_for("admin.uzivatele"))
#############################################################

@admin.route('/hrac/', methods=['GET', 'POST'])
@login_required('admin')
def hrac():
    account = session
    table_head = db_describe("hrac")
    content = db_get(" SELECT * FROM hrac")
    return render_template('admin/hrac.html', account=account, content=content, table_head=table_head, table_name='hrac')

@admin.route('/vybaveni/', methods=['GET', 'POST'])
@login_required('admin')
def vybaveni():
    account = session
    table_head = db_describe("vybaveni")
    content = db_get_from_all("vybaveni", ['*'])
    return render_template('admin/vybaveni.html', account=account, content=content, table_head=table_head, table_name='vybaveni')

@admin.route('/hra/', methods=['GET', 'POST'])
@login_required('admin')
def hra():
    account = session
    table_head = db_describe("hra")
    content = db_get_from_all("hra", ['*'])
    return render_template('admin/hra.html', account=account, content=content, table_head=table_head, table_name='hra')

@admin.route('/klan/', methods=['GET', 'POST'])
@login_required('admin')
def klan():
    account = session
    table_head = db_describe("klan")
    content = db_get_from_all("klan", ['*'])
    return render_template('admin/klan.html', account=account, content=content, table_head=table_head, table_name='klan')

@admin.route('/tym/', methods=['GET', 'POST'])
@login_required('admin')
def tym():
    account = session
    table_head = db_describe("tym")
    content = db_get_from_all("tym", ['*'])
    return render_template('admin/tym.html', account=account, content=content, table_head=table_head, table_name='tym')

@admin.route('/zapas/', methods=['GET', 'POST'])
@login_required('admin')
def zapas():
    account = session
    table_head = db_describe("zapas")
    content = db_get_from_all("zapas", ['*'])
    ucastnici = db_get_from_all("ucastnici_zapasu", ['*'])
    turnaje = db_get_from_all("turnaj", ['id', 'nazev'])
    tymy = db_get_from_all("tym", ['id', 'nazev'])
    hry = db_get_from_all("hra", ["id", "nazev_hry"])
    return render_template('admin/zapas.html', account=account, content=content, table_head=table_head, ucastnici = ucastnici, turnaje=turnaje, tymy=tymy, hry=hry, table_name='zapas')

@admin.route('/zapas/pridat/', methods=['GET', 'POST'])
@login_required('admin')
def zapas_pridat():
    if request.method == "GET":
        account = session
        turnaje = db_get_from_all("turnaj", ['id', 'nazev'])
        tymy = db_get_from_all("tym", ['id', 'nazev'])
        hry = db_get_from_all("hra", ["id", "nazev_hry"])
        return render_template('admin/zapas_pridat.html', account=account, turnaje=turnaje, tymy=tymy, hry=hry, table_name='zapas')
    else:
        if 'Odeslat' in request.form:
            # return str(request.form)
            tym1 = request.form['tym1']
            tym2 = request.form['tym2']
            if tym1 != "NULL":
                tym1 = "'%s'" % tym1
            if tym2 != "NULL":
                tym2 = "'%s'" % tym2
            last_id = None
            turnaj = request.form['turnaj']
            if turnaj != "NULL":
                turnaj = "'%s'" % turnaj
            db_get("""INSERT INTO zapas (kdy, skore, typ, hra, turnaj, cas) 
                VALUES ('%s', '%s', '%s', '%s', %s, '%s')"""
                % (request.form['kdy'], request.form['skore'], 
                    request.form['typ'], request.form['hra'], 
                    turnaj, request.form['cas']))
            last_id = db_get("SELECT id FROM zapas ORDER BY id DESC LIMIT 1;")[0][0]
            db_get("""INSERT INTO ucastnici_zapasu (id_zapas, id_tym1, id_tym2) 
                VALUES ('%s', %s, %s)"""
                % (last_id, tym1, tym2))
            flash("Zápas byl úspěšně přidán")
            return redirect(url_for("admin.zapas"))
        else:
            flash("Neznámý požadavek")
            return redirect(url_for("admin.zapas"))

@admin.route('/turnaj/', methods=['GET', 'POST'])
@login_required('admin')
def turnaj():
    account = session
    table_head = db_describe("turnaj")
    content = db_get_from_all("turnaj", ['*'])
    return render_template('admin/turnaj.html', account=account, content=content, table_head=table_head, table_name='turnaj')

@admin.route('/sponzor/', methods=['GET', 'POST'])
@login_required('admin')
def sponzor():
    account = session
    table_head = db_describe("sponzor")
    content = db_get_from_all("sponzor", ['*'])
    return render_template('admin/sponzor.html', account=account, content=content, table_head=table_head, table_name='sponzor')

@admin.route('/turnaj/add/', methods = ['GET', 'POST'])
@login_required('admin')
def turnaj_add():
    if ( request.method == "GET" ):
        account = session
        table_head = db_describe('turnaj')
        return render_template('admin/turnaj_add.html', account=account, table_name='turnaj', header=table_head)
    else:
        typ = request.form['typ']
        last_id = None;
        if typ == 'wc':
            db_get("""INSERT INTO turnaj_wc (prvni, druhy, treti, ctvrty, paty) VALUES (NULL, NULL, NULL, NULL, NULL)""")
            last_id = db_get("SELECT id FROM turnaj_wc ORDER BY id DESC LIMIT 1;")[0][0]
            db_get("""INSERT INTO turnaj (nazev, odmena, kdy, kde, kapacita, bezny, wc) 
                        VALUES ('%s','%s','%s','%s','%s', NULL, '%s')""" %
                        (request.form['nazev'], request.form['odmena'], request.form['kdy'],
                            request.form['kde'], request.form['kapacita'], last_id))
            flash("Turnaj byl přidán")
            return redirect(url_for('admin.turnaj'))
        else: # bezny
            db_get("""INSERT INTO turnaj_bezny (vitez) VALUES (NULL)""")
            last_id = db_get("SELECT id FROM turnaj_bezny ORDER BY id DESC LIMIT 1;")[0][0]
            db_get("""INSERT INTO turnaj (nazev, odmena, kdy, kde, kapacita, bezny, wc) 
                        VALUES ('%s','%s','%s','%s','%s', '%s', NULL)""" %
                        (request.form['nazev'], request.form['odmena'], request.form['kdy'],
                            request.form['kde'], request.form['kapacita'], last_id))
            flash("Turnaj byl přidán")
            return redirect(url_for('admin.turnaj'))
        # vlozeni veci z turnaje

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
                return redirect(url_for("admin.{0}".format(table)))
            
        db_insert_what(table, request.form)
        return redirect(url_for("admin.{0}".format(table)))

@admin.route('/<table>/remove/', methods=['POST'])
@login_required('admin')
def remove_row(table):
    print request.form['remove_row']
    if 'remove_row' in request.form:
        db, cursor = database()
        cursor.execute("DELETE FROM %s WHERE id=%s" % (table, request.form['remove_row'],))
        db.commit()
        return redirect(url_for("admin."+table))
    else:
        flash('Něco se pokazilo')
        return redirect(url_for("admin."+table))

@admin.route('/<table>/edit/<int:row>/', methods=['GET', 'POST'])
@login_required('admin')
def edit_row(table, row):
    if 'Upravit' in request.form or request.method == 'GET':
        content = db_get_from_where_one(table, "id='{0}'".format(row), ['*'])
        table_head = db_describe(table)
        return render_template('admin/admin_table_edit.html', content=content, account=session, header=table_head, table_name=table)
    elif 'Odeslat' in request.form:
        if db_update_where_what(table, "id='{0}'".format(row), request.form) == True:
            return redirect('/admin/%s/' % (table))
        else:
            flash("Chyba databáze, požadavek se nepodařilo dokončit")
            return redirect('/admin/%s/' % (table))
    else: # POST
        flash("Neznámý požadavek :(")
        return redirect('/admin/%s/' % (table))

@admin.route('/klan/detail/<nazev>/<id>', methods=['GET', 'POST'])
@login_required('admin')
def adoj(nazev, id):
    #print(nazev)
    account = session
    members = members_in_clan(id)
    klan_info = db_get_from_where_one('klan', "id='{0}'".format(id), ['*'])
    #print(klan_info)
    return render_template('admin/klan_detail.html', account=account, members=members, klan_info=klan_info, table_name='klan')

@admin.route('/tym/detail/<nazev>/<id>', methods=['GET', 'POST'])
@login_required('admin')
def team_members_detail(nazev, id):
    account = session
    members = members_in_team(id)
    print(members)
    return render_template('admin/team_detail.html', account=account, members=members, table_name='tym')

@admin.route('/turnaj/detail/<id>', methods=['GET', 'POST'])
@login_required('admin')
def turnament_detail(id):
    if request.method == 'GET':
        account = session
        games = db_get("""
            SELECT zapas.id,zapas.kdy,zapas.skore,zapas.typ,hra.nazev_hry
            FROM turnaj JOIN zapas ON ( turnaj.id = zapas.turnaj )
                        JOIN hra ON ( zapas.hra = hra.id )
            WHERE turnaj.id =""" + str(id))
        name = db_get("SELECT nazev FROM turnaj WHERE id=\""+id+"\"")
        sponzors = db_get("""
            SELECT sponzor.nazev, sponzor.typ, sponzoroval.castka, sponzoroval.id
            FROM turnaj JOIN sponzoroval ON ( turnaj.id = sponzoroval.turnaj )
                        JOIN sponzor     ON ( sponzoroval.sponzor = sponzor.id )
            WHERE turnaj.id = %s
            """%(id))
        all_sponsors = db_get("""SELECT nazev, typ, id FROM sponzor""")
        return render_template('admin/turnament_detail.html', account=account, members=games, Name=name[0][0], sponzors=sponzors, all_sponsors=all_sponsors, table_name='turnaj')
    else:
        print request.form
        if 'add_sponsor' in request.form:
            id_sponzora = request.form['sponsor_id_add']
            castka = request.form['castka']
            if castka == '':
                flash("Musite vyplnit částku!")
                return redirect(url_for("admin.turnament_detail", id=id))
            db_get("""INSERT INTO sponzoroval (castka, sponzor, turnaj) VALUES
                    (%s, %s, %s)""" % (castka, id_sponzora, id))
            return redirect(url_for('admin.turnament_detail', id=id))
        elif 'remove' in request.form:
            id_row = request.form['id']
            db_get("""DELETE FROM sponzoroval WHERE id=%s""" % (id_row))
            return redirect(url_for('admin.turnament_detail', id=id))
        else:
            flash('Neznámý požadavek')
            return redirect(url_for('admin.turnament_detail', id=id))

@admin.route('/turnaj/detail/location/<location>', methods=['GET', 'POST'])
@login_required('admin')
def turnament_location(location):
    account = session
    db_c = db_get("SELECT id, nazev, odmena, kdy, kapacita FROM turnaj WHERE kde=\"%s\"" %(location))
    return render_template('admin/turnament_location.html', account=account, turnaments=db_c, place=location , table_name='turnaj')

@admin.route('/hra/detail/<name>', methods=['GET', 'POST'])
@login_required('admin')
def games_detail(name):
    account = session
    db_c = db_get("SELECT turnaj.nazev, turnaj.kde, mod_hry, zapas.kdy, typ, turnaj.id FROM (hra JOIN zapas ON ( hra.id = zapas.hra )) JOIN turnaj ON ( zapas.turnaj = turnaj.id) WHERE nazev_hry = \"%s\"" %(name))
    return render_template('admin/hra_detail.html', account=account, gameInfo=db_c, table_name='hra')

@admin.route('/hra/detail/genre/<genre>', methods=['GET', 'POST'])
@login_required('admin')
def games_genre(genre):
    account = session
    db_c = db_get("SELECT nazev_hry, vydavatel_hry, rok_vydani_hry FROM hra WHERE zanr_hry=\"%s\"" %(genre))
    return render_template('admin/hra_genre.html', account=account, genreSort=db_c, genre=genre, table_name='hra')

@admin.route('/hra/detail/mod/<mods>', methods=['GET', 'POST'])
@login_required('admin')
def games_mods(mods):
    account = session
    db_c = db_get("SELECT nazev_hry, vydavatel_hry, rok_vydani_hry FROM hra WHERE mod_hry=\"%s\"" %(mods))
    return render_template('admin/hra_mods.html', account=account, ModSort=db_c, mod=mods, table_name='hra')

@admin.route('/hra/detail/publisher/<pub>', methods=['GET', 'POST'])
@login_required('admin')
def games_publisher(pub):
    account = session
    db_c = db_get("SELECT nazev_hry, rok_vydani_hry, zanr_hry FROM hra WHERE vydavatel_hry=\"%s\"" %(pub))
    return render_template('admin/hra_vydavatel.html', account=account, PubSort=db_c, publisher=pub, table_name='hra')

@admin.route('/hrac/detail/<id>', methods=['GET', 'POST'])
@login_required('admin')
def user_detail(id):
    if request.method == 'GET':
        account = session
        db_c = db_get("""
        SELECT hrac.jmeno, hrac.prezdivka, klan.id, klan.nazev, tym.id, tym.nazev
        FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
                LEFT JOIN klan          ON ( klan.id = klan_clenstvi.klan ) 
                LEFT JOIN tym_clenstvi  ON ( hrac.id = tym_clenstvi.hrac  )
                LEFT JOIN tym           ON ( tym.id  = tym_clenstvi.tym   )
        WHERE hrac.id =""" + str(id))
        db_vybaveni = db_get("""
        SELECT typ , vyrobce, model ,popis, vybaveni.id
        FROM hrac JOIN vybaveni ON ( hrac.id = vybaveni.vlastnik )
        WHERE hrac.id = """ + str(id))
        db_specialization = db_get("""
        SELECT nazev_hry, specializace.id
        FROM specializace JOIN hra ON hra.id = specializace.hra 
        WHERE hrac = %s
        """%(id))
        all_games = db_get("SELECT nazev_hry, id FROM hra")
        return render_template('admin/user_detail.html', account=account, PlayerInfo=db_c[0] ,PlayerVybaveniInfo=db_vybaveni, Specialization=db_specialization, playerID=id, all_games=all_games, table_name='hrac')
    else:
        if ( "odebrat_id" in request.form ):
            vybaveni_id = request.form["odebrat_id"]
            db_get("""DELETE FROM vybaveni WHERE id=%s""" % (vybaveni_id))
        if ( "remove_specialization" in request.form ):
            spec_id = request.form["remove_specialization"]
            db_get("""DELETE FROM specializace WHERE id=%s""" % (spec_id))
        if ( "add_specialization" in request.form ):
            spec_id = request.form["add_specialization_id"]
            db_specialization = db_get("""
            SELECT nazev_hry, specializace.id, hra.id
            FROM specializace JOIN hra ON hra.id = specializace.hra 
            WHERE hrac = %s
            """%(id))
            for i in db_specialization:
                if ( int(spec_id) == int(i[2]) ):
                    flash('Je již ve specializaci')
                    return redirect(url_for('admin.user_detail', id=id))
            db_get("INSERT INTO specializace (hrac,hra) VALUES(%s,%s)"%(id,spec_id))

        return redirect(url_for('admin.user_detail', id=id))