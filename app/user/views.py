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
    nick = session["username"]
    hrac = db_get("""
    SELECT hrac.jmeno, hrac.prezdivka, klan.id, klan.nazev, tym.id, tym.nazev
    FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
              LEFT JOIN klan          ON ( klan.id = klan_clenstvi.klan ) 
              LEFT JOIN tym_clenstvi  ON ( hrac.id = tym_clenstvi.hrac  )
              LEFT JOIN tym           ON ( tym.id  = tym_clenstvi.tym   )
    WHERE hrac.prezdivka='""" + nick+"'")[0]
    vybaveni = db_get("""
    SELECT typ , vyrobce, model ,popis, vybaveni.id
    FROM hrac JOIN vybaveni ON ( hrac.id = vybaveni.vlastnik )
    WHERE hrac.prezdivka='""" + nick+"'")
    zapasy = db_get("""
    SELECT id_zapas, skore, typ, hra.nazev_hry, tym.nazev, zapas.kdy, turnaj.kde, turnaj.odmena
    FROM hrac JOIN tym_clenstvi ON ( hrac.id = tym_clenstvi.hrac )
              JOIN tym          ON ( tym.id  = tym_clenstvi.tym  )
              JOIN ucastnici_zapasu ON ( ucastnici_zapasu.id_tym = tym.id )
              JOIN zapas ON ( ucastnici_zapasu.id_zapas = zapas.id )
              JOIN turnaj ON ( turnaj.id = zapas.turnaj )
              JOIN hra ON ( hra.id = zapas.hra )
    WHERE hrac.prezdivka = \"%s\" """ %(str(nick)))
    return render_template('user/hrac.html', account=account, table_name='hrac', hrac=hrac, vybaveni=vybaveni, content=zapasy )

@user.route('/prochazet/', methods=['GET', 'POST'])
@login_required('user')
def hrac_prochazet():
    account = session
    hraci = db_get("""
        SELECT hrac.jmeno, hrac.prezdivka, klan.id, klan.nazev, tym.id, tym.nazev
        FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
                  LEFT JOIN klan          ON ( klan.id = klan_clenstvi.klan ) 
                  LEFT JOIN tym_clenstvi  ON ( hrac.id = tym_clenstvi.hrac  )
                  LEFT JOIN tym           ON ( tym.id  = tym_clenstvi.tym   )""")
    tmp = []
    pismeno = ''
    if 'pismeno' in request.args:
        pismeno = request.args['pismeno']
        print pismeno.lower()
        for i in range(len(hraci)):
            if (hraci[i][1][0] == pismeno.upper()) or (hraci[i][1][0] == pismeno.lower()):
                tmp.append(hraci[i])
        hraci = tmp
    return render_template('user/hrac_prochazet.html', account=account, table_name='prochazet', hraci=hraci, pismeno=pismeno)

@user.route('/prochazet/detail/<string:nick>', methods=['GET', 'POST'])
@login_required('user')
def user_detail(nick):
    account = session
    hrac = db_get("""
    SELECT hrac.jmeno, hrac.prezdivka, klan.id, klan.nazev, tym.id, tym.nazev
    FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
              LEFT JOIN klan          ON ( klan.id = klan_clenstvi.klan ) 
              LEFT JOIN tym_clenstvi  ON ( hrac.id = tym_clenstvi.hrac  )
              LEFT JOIN tym           ON ( tym.id  = tym_clenstvi.tym   )
    WHERE hrac.prezdivka='""" + nick+"'")[0]
    vybaveni = db_get("""
    SELECT typ , vyrobce, model ,popis
    FROM hrac JOIN vybaveni ON ( hrac.id = vybaveni.vlastnik )
    WHERE hrac.prezdivka='""" + nick+"'")
    return render_template('user/hrac_detail.html', account=account, table_name='prochazet', hrac=hrac, vybaveni=vybaveni)

@user.route('/hra/', methods=['GET', 'POST'])
@login_required('user')
def hra():
    account = session
    table_head = db_describe("hra")
    database = db_get_from_all('hra', ['*'])
    return render_template('user/hra.html', account=account, table_name='hra', content=database, table_head=table_head)

@user.route('/klan/', methods=['GET', 'POST'])
@login_required('user')
def klan():
    if request.method == 'GET':
        account = session
        klan = db_get_from_where_one('klan', "vudce='{}'".format(session['id']), ['*'])
        vudce = True
        vudce_klanu = session['username']
        if klan == None:
            vudce = False
            klan = db_get("""
                SELECT * FROM klan
                    INNER JOIN klan_clenstvi ON ( klan.id = klan_clenstvi.klan ) 
                    WHERE klan_clenstvi.hrac='""" +str(session['id'])+"'")
            if klan:
                klan = klan[0]
                vudce_klanu = db_get("""
                    SELECT hrac.prezdivka FROM hrac
                        INNER JOIN klan ON ( klan.vudce = hrac.id ) 
                        INNER JOIN klan_clenstvi ON ( klan.id = klan_clenstvi.klan ) 
                        WHERE klan_clenstvi.hrac='""" +str(session['id'])+"'")
                if vudce_klanu:
                    vudce_klanu = vudce_klanu[0][0]
        clenove = None
        if klan != ():
            clenove = db_get("""
                SELECT hrac.jmeno, hrac.prezdivka, hrac.id
                FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
                  LEFT JOIN klan ON ( klan.id = klan_clenstvi.klan ) 
                WHERE klan_clenstvi.klan='""" + str(klan[0])+"'")
        return render_template('user/klan.html', account=account, table_name='klan', database=database, klan=klan, vudce=vudce, clenove=clenove, vudce_klanu=vudce_klanu)
    else:   # POST
        if 'zrusit' in request.form:
            db, cursor = database()
            cursor.execute("DELETE FROM klan WHERE id=%s" % (request.form['id'],))
            db.commit()
            return redirect(url_for("user.klan"))
        elif 'vyhodit' in request.form:
            db, cursor = database()
            cursor.execute("DELETE FROM klan_clenstvi WHERE hrac=%s" % (request.form['id'],))
            db.commit()
            return redirect(url_for("user.klan"))
        elif 'opustit' in request.form:
            db, cursor = database()
            cursor.execute("DELETE FROM klan_clenstvi WHERE hrac=%s" % (session['id'],))
            db.commit()
            return redirect(url_for("user.klan"))
        return "chyba"

@user.route('/klan/zalozit/', methods=['GET', 'POST'])
@login_required('user')
def klan_zalozit():
    account = session
    return render_template('user/klan_zalozit.html', account=account, table_name='klan_zalozit')

@user.route('/klan_prochazet/', methods=['GET', 'POST'])
@login_required('user')
def klan_prochazet():
    account = session
    klany = db_get_from_all('klan', ['*'])
    tmp = []
    pismeno = ''
    if 'pismeno' in request.args:
        pismeno = request.args['pismeno']
        print pismeno.lower()
        for i in range(len(klany)):
            if (klany[i][1][0] == pismeno.upper()) or (klany[i][1][0] == pismeno.lower()):
                tmp.append(klany[i])
        klany = tmp
    return render_template('user/klan_prochazet.html', account=account, table_name='klan_prochazet', klany=klany)

@user.route('/klan_prochazet/detail/<string:nick>', methods=['GET', 'POST'])
@login_required('user')
def klan_detail(nick):
    account = session
    klan = db_get("""SELECT * FROM klan WHERE klan.nazev='""" +nick+"'")
    if klan:
        klan = klan[0]
        vudce_klanu = db_get("""
            SELECT hrac.prezdivka FROM hrac
                INNER JOIN klan ON ( klan.vudce = hrac.id ) 
                WHERE klan.nazev='""" +nick+"'")
        if vudce_klanu:
            vudce_klanu = vudce_klanu[0][0]
    clenove = db_get("""
                SELECT hrac.jmeno, hrac.prezdivka, hrac.id
                FROM hrac LEFT JOIN klan_clenstvi ON ( hrac.id = klan_clenstvi.hrac ) 
                  LEFT JOIN klan ON ( klan.id = klan_clenstvi.klan ) 
                WHERE klan_clenstvi.klan='""" + str(klan[0])+"'")
    return render_template('user/klan_detail.html', account=account, table_name='klan_prochazet', klan=klan, clenove=clenove, vudce_klanu=vudce_klanu)

@user.route('/tym/', methods=['GET', 'POST'])
@login_required('user')
def tym():
    account = session
    database = db_get_from_all('tym', ['*'])
    return render_template('user/tym.html', account=account, table_name='tym', database=database)

@user.route('/zapas/', methods=['GET', 'POST'])
@login_required('user')
def zapas():
    account = session
    database = db_get_from_all('zapas', ['*'])
    return render_template('user/zapas.html', account=account, table_name='zapas', database=database)

@user.route('/turnaj/', methods=['GET', 'POST'])
@login_required('user')
def turnaj():
    account = session
    database = db_get_from_all('turnaj', ['*'])
    return render_template('user/turnaj.html', account=account, table_name='turnaj', database=database)

@user.route('/sponzor/', methods=['GET', 'POST'])
@login_required('user')
def sponzor():
    account = session
    database = db_get_from_all('sponzor', ['*'])
    return render_template('user/sponzor.html', account=account, table_name='sponzor', database=database)

@user.route('/profil/<nickname>', methods=['GET', 'POST'])
@login_required('user')
def profil(nickname):
    account = session
    vybaveni = db_get("""
        SELECT typ, model, popis
        FROM vybaveni JOIN hrac ON ( vybaveni.vlastnik = hrac.id )
        WHERE hrac.prezdivka = \"""" + str(nickname) + "\"")
    zapasy = db_get("""
    SELECT id_zapas, skore, typ, hra.nazev_hry, tym.nazev, zapas.kdy, turnaj.kde, turnaj.odmena
    FROM hrac JOIN tym_clenstvi ON ( hrac.id = tym_clenstvi.hrac )
              JOIN tym          ON ( tym.id  = tym_clenstvi.tym  )
              JOIN ucastnici_zapasu ON ( ucastnici_zapasu.id_tym = tym.id )
              JOIN zapas ON ( ucastnici_zapasu.id_zapas = zapas.id )
              JOIN turnaj ON ( turnaj.id = zapas.turnaj )
              JOIN hra ON ( hra.id = zapas.hra )
    WHERE hrac.prezdivka = \"%s\" """ %(str(nickname)))
    print(zapasy)
    return render_template('user/profil.html', vybaveni=vybaveni, zapasy=zapasy)

@user.route('/hrac/remove/', methods=['GET', 'POST'])
@login_required('user')
def remove_equipment():
    print(request.form["remove_id"])
    if 'remove_id' in request.form:
        db, cursor = database()
        cursor.execute("DELETE FROM %s WHERE id=%s" % ("vybaveni", request.form['remove_id'],))
        db.commit()
        return redirect(url_for("user.hrac"))
    else:
        flash('Něco se pokazilo')
        return redirect(url_for("user.index"))

@user.route('/hrac/add/equipment/', methods=['GET', 'POST'])
@login_required('user')
def add_equipment():
    table = "vybaveni"
    if ( request.method == "GET" ):
        account = session
        table_head = db_describe(table)
        id = session['id']
        return render_template('user/hrac_add_equipment.html',id=id, account=account, table_name=table, header=table_head)
    else:
        print(request.form)
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
                return redirect(url_for("user.hrac"))
            
        db_insert_what(table, request.form)
        return redirect(url_for("user.hrac"))

@user.route('/hra/detail/<name>', methods=['GET', 'POST'])
@login_required('user')
def games_detail(name):
    account = session
    db_c = db_get("SELECT turnaj.nazev, turnaj.kde, mod_hry, zapas.kdy, typ, turnaj.id FROM (hra JOIN zapas ON ( hra.id = zapas.hra )) JOIN turnaj ON ( zapas.turnaj = turnaj.id) WHERE nazev_hry = \"%s\"" %(name))
    return render_template('user/hra_detail.html', account=account, gameInfo=db_c )

@user.route('/hra/detail/genre/<genre>', methods=['GET', 'POST'])
@login_required('user')
def games_genre(genre):
    account = session
    db_c = db_get("SELECT nazev_hry, vydavatel_hry, rok_vydani_hry FROM hra WHERE zanr_hry=\"%s\"" %(genre))
    return render_template('user/hra_genre.html', account=account, genreSort=db_c, genre=genre)

@user.route('/hra/detail/mod/<mods>', methods=['GET', 'POST'])
@login_required('user')
def games_mods(mods):
    account = session
    db_c = db_get("SELECT nazev_hry, vydavatel_hry, rok_vydani_hry FROM hra WHERE mod_hry=\"%s\"" %(mods))
    return render_template('user/hra_mods.html', account=account, ModSort=db_c, mod=mods )

@user.route('/hra/detail/publisher/<pub>', methods=['GET', 'POST'])
@login_required('user')
def games_publisher(pub):
    account = session
    db_c = db_get("SELECT nazev_hry, rok_vydani_hry, zanr_hry FROM hra WHERE vydavatel_hry=\"%s\"" %(pub))
    return render_template('user/hra_vydavatel.html', account=account, PubSort=db_c, publisher=pub)
