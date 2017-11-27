# -*- encoding: UTF-8 -*-

from flask import Blueprint, render_template, abort, request, session, redirect, flash, url_for
from time import strftime
from jinja2 import TemplateNotFound
from app.functions import *
from werkzeug.utils import secure_filename
import os

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
        WHERE hrac.prezdivka='""" + nick+"'")
    try:
        hrac = hrac[0]
    except:
        hrac = ['',('unknown')]
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
    if request.method == 'GET':
            account = session
            return render_template('user/klan_zalozit.html', account=account, table_name='klan')
    else:
        print request.files
        if 'odeslat' in request.form:
            if 'file' in request.files:
                file = request.files['file']
                print str(file)
                if allowed_photo(file.filename):
                    filename1 = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename1))
                else:
                    flash("Nepodporovaný formát souboru logo")
                    return redirect(url_for("user.klan_zalozit"))
            if 'song' in request.files:
                file = request.files['song']
                if allowed_song(file.filename):
                    filename2 = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename2))
                else:
                    flash("Nepodporovaný formát souboru hymna")
                    return redirect(url_for("user.klan_zalozit"))
            # ted je nahranej soubor jestli byl
            nazev = request.form['nazev']
            try:
                db_get("""INSERT INTO klan (nazev, hymna, logo, vudce) 
                        VALUES  ('%s', '%s', '%s', '%s')""" % (nazev, filename2, filename1, session['id']))
                flash("Klan byl úspěšně vytvořen")
            except:
                flash("Chyba při vytváření klanu, duplicita")
            return redirect(url_for('user.klan'))
        else:
            flash("Neznámý požadavek")
            return redirect(url_for("klan_zalozit"))

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
    if request.method == 'GET':
        account = session
        tym = db_get_from_where_one('tym', "vudce='{}'".format(session['id']), ['*'])
        vudce = True
        vudce_tymu = session['username']
        if tym == None:
            vudce = False
            tym = db_get("""
                SELECT * FROM tym
                    INNER JOIN tym_clenstvi ON ( tym.id = tym_clenstvi.tym ) 
                    WHERE tym_clenstvi.hrac='""" +str(session['id'])+"'")
            if tym:
                tym = tym[0]
                vudce_tymu = db_get("""
                    SELECT hrac.prezdivka FROM hrac
                        INNER JOIN tym ON ( tym.vudce = hrac.id ) 
                        INNER JOIN tym_clenstvi ON ( tym.id = tym_clenstvi.tym ) 
                        WHERE tym_clenstvi.hrac='""" +str(session['id'])+"'")
                if vudce_tymu:
                    vudce_tymu = vudce_tymu[0][0]
        clenove = None
        if tym != ():
            clenove = db_get("""
                SELECT hrac.jmeno, hrac.prezdivka, hrac.id
                FROM hrac LEFT JOIN tym_clenstvi ON ( hrac.id = tym_clenstvi.hrac ) 
                  LEFT JOIN tym ON ( tym.id = tym_clenstvi.tym ) 
                WHERE tym_clenstvi.tym='""" + str(tym[0])+"'")
        return render_template('user/tym.html', account=account, table_name='tym', database=database, tym=tym, vudce=vudce, clenove=clenove, vudce_tymu=vudce_tymu)
    else:   # POST
        if 'zrusit' in request.form:
            db, cursor = database()
            cursor.execute("DELETE FROM tym WHERE id=%s" % (request.form['id'],))
            db.commit()
            return redirect(url_for("user.tym"))
        elif 'vyhodit' in request.form:
            db, cursor = database()
            cursor.execute("DELETE FROM tym_clenstvi WHERE hrac=%s" % (request.form['id'],))
            db.commit()
            return redirect(url_for("user.tym"))
        elif 'opustit' in request.form:
            db, cursor = database()
            cursor.execute("DELETE FROM tym_clenstvi WHERE hrac=%s" % (session['id'],))
            db.commit()
            return redirect(url_for("user.tym"))
        return "chyba"

@user.route('/tym/zalozit/', methods=['GET', 'POST'])
@login_required('user')
def tym_zalozit():
    if request.method == 'GET':
        account = session
        return render_template('user/tym_zalozit.html', account=account, table_name='tym')
    else:
        print request.files
        if 'odeslat' in request.form:
            if 'file' in request.files:
                file = request.files['file']
                if allowed_photo(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                else:
                    flash("Nepodporovaný formát souboru")
                    return redirect(url_for("user.tym_zalozit"))
            # ted je nahranej soubor jestli byl
            nazev = request.form['nazev']
            popis = request.form['popis']
            try:
                db_get("""INSERT INTO tym (nazev, emblem, popis, vudce) 
                        VALUES  ('%s', '%s', '%s', '%s')""" % (nazev, filename, popis, session['id']))
                flash("Tým byl úspěšně vytvořen")
            except:
                flash("Chyba při vytváření týmu, duplicita")
            return redirect(url_for('user.tym'))
        else:
            flash("Neznámý požadavek")
            return redirect(url_for("tym_zalozit"))

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
    future_champ = db_get("""
    SELECT nazev, kdy, kde, odmena, kapacita, id
    FROM turnaj 
    WHERE kdy > '%s' 
    ORDER BY YEAR(kdy) DESC, MONTH(kdy) DESC, DAY(kdy) DESC
    """%(strftime("%Y-%m-%d")))
    past_champ = db_get("""
    SELECT nazev, kdy, kde, odmena, kapacita, id
    FROM turnaj 
    WHERE kdy <= '%s' 
    ORDER BY YEAR(kdy) DESC, MONTH(kdy) DESC, DAY(kdy) DESC"""
    %(strftime("%Y-%m-%d")))
    return render_template('user/turnaj.html', account=account, table_name='turnaj', future=future_champ, past=past_champ)

@user.route('/turnaj/detail/location/<location>')
@login_required('user')
def turnaj_location_detail(location):
    account = session
    turnaments = db_get("""
    SELECT id, nazev, odmena, kdy, kapacita 
    FROM turnaj 
    WHERE kde="%s"
    ORDER BY YEAR(kdy) DESC, MONTH(kdy) DESC, DAY(kdy) DESC""" %(location))
    return render_template('user/turnaj_location.html', account=account, place=location, turnaments=turnaments)

@user.route('/turnaj/detail/<id>', methods=['GET', 'POST'])
@login_required('user')
def turnaj_detail(id):
    account = session
    games = db_get("""
    SELECT zapas.cas, zapas.kdy, turnaj.kde, zapas.skore, hra.nazev_hry, zapas.typ
    FROM zapas JOIN turnaj ON ( zapas.turnaj = turnaj.id )
               JOIN hra ON ( hra.id = zapas.hra )
    WHERE turnaj = %s
    """%(id))
    sponzors = db_get("""
    SELECT nazev
    FROM sponzor JOIN sponzoroval ON ( sponzor.id = sponzoroval.sponzor )
    WHERE turnaj=%s
    """%(id))
    name = db_get("SELECT nazev FROM turnaj WHERE id = %s"%(id))[0][0]
    return render_template('user/turnaj_detail.html', account=account, table_name='turnaj', zapasy=games, Name=name, sponzors=sponzors)

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
    db_c = db_get("""
    SELECT nazev, turnaj.kde, mod_hry, turnaj.kdy, zapas.typ, turnaj.id
    FROM turnaj JOIN zapas ON ( zapas.turnaj = turnaj.id )
                JOIN hra   ON ( hra.id = zapas.hra )
    WHERE nazev_hry = "%s"
    GROUP BY nazev, turnaj.kde, mod_hry, kapacita, turnaj.kdy, zapas.typ, turnaj.id"""%(name))
    zapasy = db_get("""
    SELECT zapas.kdy, turnaj.kde, t1.nazev, skore, t2.nazev, typ
    FROM zapas JOIN turnaj ON ( zapas.turnaj = turnaj.id ) 
               JOIN ucastnici_zapasu ON ( ucastnici_zapasu.id_zapas = zapas.id )
               JOIN tym t1 ON ( id_tym = t1.id )
               JOIN tym t2 ON ( id_tym2 = t2.id )
    WHERE hra = ( SELECT id FROM hra WHERE nazev_hry = "%s" )
    LIMIT 10"""%(name))
    return render_template('user/hra_detail.html', account=account, gameInfo=db_c, zapasy=zapasy, name=name)

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
