from flask import * # render_template
import sys
import time
from datetime import datetime
from datetime import date
import psycopg2
import psycopg2.extras


#from sql import *

app = Flask(__name__)
app.secret_key = 'some_secret'

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

#route test
@app.route('/hello')
def hello_world():
    return 'Hello, World!'


###########################################
#route pour la page d'accueil
@app.route('/', methods=['POST']) #attends-toi à être sollicité par la méthode POST
def accueil():
    return render_template("index.html")

#on veut maintenant lier la page accueil à la page datesdereservation

#route pour la page de choix de dates
@app.route('/datesdereservation', methods=['GET','POST'])
def dates_de_reservation():
    return render_template("dates-de-reservation.html")

#route pour la page de réservation de chambre
@app.route('/reservezvotrechambre', methods=['POST'])
def reservez_votre_chambre():
    return render_template("reservez-votre-chambre.html")

#route pour la page de confirmation de réservation
@app.route('/reservationenregistree', methods=['POST'])
def reservation_enregistree():
    return render_template("reservation-enregistree.html")


###########################################
#COnfiguration de l'accès à la base de données postgreSQL sur le serveur dédié au Cremi de l'Université de Bordeaux

def pgsql_connect():
    try:
        db = psycopg2.connect("host=dbserver.emi.u-bordeaux.fr dbname=fpizzacoca user=fpizzacoca")
        return db
    except Exception as e :
        erreur_pgsql("Désolé, connexion impossible actuellement.", e)

def pgsql_select(command, param):  #possibilité de lancer des requêtes au sein de la BDD en question
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


#ne pas toucher! lance l'application
if __name__ == "__main__":
    app.run()
