from flask import * # includes the render_template method
import sys
import time
from datetime import datetime
from datetime import date
import psycopg2
import psycopg2.extras
from pymongo import * #mongodb
from sql import * #est-ce utile? à vérifier

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'some_secret'

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

#route test
@app.route('/hello')
def hello_world():
    return mgdb_init_db()


###########################################
#route pour la page d'accueil
@app.route('/', methods=['GET','POST']) #attends-toi à être sollicité par la méthode POST ou GET
def accueil():
    listemail = listemails()  #fonction listemails() créée en bas du code source
    return render_template("index.html", listemail=listemail)

#on veut maintenant lier la page accueil à la page datesdereservation

#route pour la page de choix de dates
@app.route('/datesdereservation', methods=['GET','POST'])
def dates_de_reservation():
    session['mail'] = request.form['mail'] #la fonction request.form va chercher le champ qui a pour nom name='email' dans le fichier index.html 
    session['prenom'] = prenom_du_client(session['mail']) #va chercher le prénom du client correspondant au mail choisi dans le formulaire/liste déroulante
    return render_template("dates-de-reservation.html", session=session) #session=session permet de transmettre la variable session d'une page à l'autre pour une session utilisateur donnée

#route pour la page de réservation de chambre
@app.route('/reservezvotrechambre', methods=['GET','POST'])
def reservez_votre_chambre():
    session['arrivee'] = request.form['arrivee'] 
    session['depart'] = request.form['depart'] 
    return render_template("reservez-votre-chambre.html")

#route pour la page de confirmationde réservation
@app.route('/reservationenregistree', methods=['GET', 'POST'])
def reservation_enregistree():
    return render_template("reservation-enregistree.html")


##################################
#Configuration de l'accès à la base de données postgreSQL sur le serveur dédié au Cremi de l'Université de Bordeaux
#################################

# 1. Connexion à la Base De Données PostGres du Cremi depuis l'app Flask:
###################################################################
def pgsql_connect():
    try:
        db = psycopg2.connect("host=dbserver.emi.u-bordeaux.fr dbname=hbelaribi user=hbelaribi")
        return db
    except Exception as e :
        erreur_pgsql("Désolé, connexion impossible actuellement.", e)


# 2.Faire n'importe quelle requêtes auprès de la Base de Données depuis l'app Flask
#############################################################################
def pgsql_select(command, param):
    db = pgsql_connect()
    # pour récupérer les attributs des relations
    # cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor = db.cursor()
    try:
        cursor.execute(command, param)
        rows = cursor.fetchall()
        # close communication
        cursor.close()
        db.close()
        return rows
    except Exception as e :
        erreur_pgsql("Désolé, service indisponible actuellement.", e)


# 3. Insérer de nouvelles entrées dans la Base de Données depuis l'app Flask
######################################################################
def pgsql_insert(command, param):
    db = pgsql_connect()
    cursor = db.cursor()
    try:
        cursor.execute(command, param)
        rows = cursor.rowcount()
        # close communication
        cursor.close()
        db.close()
        db.commit()
    except Exception as e :
        erreur_pgsql("Désolé, service indisponible actuellement.", e)

# 4. Gestion des erreurs depuis l'app Flask
###########################################
def erreur_pgsql(mess, e):
        flash(str(e))
        return redirect(url_for('accueil', errors=str(mess)))


################################################
# Récupération des donnnées des tables de la BDD
################################################

#1. dans la table hotel2019.client (telle que définie dans le projet création de BDD postgreSQL)
###########
#Cette fonction récupère le mail des clients dans la table client (utilisée dans page index.html)
def listemails():
    return pgsql_select('SELECT mail FROM hotel2019.client ORDER BY mail ;', []) #à la manière d'une requête SQL dans postgreSQL

#Cette fonction récupère le prénom du client dans la table client (utilisée dans dates-de-reservation.html)
def prenom_du_client(mail):
    return pgsql_select('SELECT prenom FROM hotel2019.client WHERE mail = (%s) ;', [mail])


##############
#MongoDB
#############

#se connecter à la BDD NoSQL Mongo
def get_mg_db():
	db MongoClient("mongodb://mongodb.emi.u-bordeaux.fr:27017").
	return db

def mgdb_drop_db():
	mgdb=get_mg_db()
	mgdb.chambres.drop()
	mgdb.comments.drop()

def mgdb_init_db():
	mgdb=get_mg_db()
	with app.open_resource('/json/hotel_chambres.json') as f:
	mgdb.chambres.insert(json.loads(f.read().decode('utf8')))

def mgdb_display_chambre(idChambre):
	mgdb=get_mg_db()
	if mgdb:
		return mgdb.comments.find({"chambre_id":int(idChambre)})
	else:
		return None

def mgdb_display_comments(idChambre):
	mgdb=get_mg_db()
	if mgdb:
		return mgdb.comments.find({"chambre_id":int(idChambre)})
	else:
		return None

def mgdb_insert_comment(idChambre, nom, prenom, jour, debut, fin, avis):
	mgdb=get_mg_db()
	result=mgdb.comments.insert(
		{
			"chambre_id": int(idChambre),
			"client_nom": nom,
			"client_prenom": prenom,
			"date": jour,
			"date_debut": debut,
			"date_fin": fin,
			"avis": avis
		}
	)
	return result


###########################################################################
###########################################################################
#Ne surtout pas toucher cette ligne de code! Elle lance l'application Flask!
###########################################################################
if __name__ == "__main__":
    app.run()
###########################################################################

