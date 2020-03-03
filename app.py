from flask import Flask
#from sql import *

app = Flask(__name__)

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')
# To get one variable, tape app.config['MY_VARIABLE']

#route test
@app.route('/')
def hello_world():
    return 'Hello, World!'



#route pour la page d'accueil
@app.route('/accueil')
def accueil():
    return render_template("index.html")


#route pour la page de choix de dates
@app.route('/dates-de-reservation')
def dates_de_reservation():
    return render_template("dates-de-reservation.html")

#route pour la page de réservation de chambre
@app.route('/reservez-votre-chambre')
def reservez_votre_chambre():
    return render_template("reservez-votre-chambre.html")

#route pour la page de confirmation de réservation
@app.route('/reservation-enregistree')
def reservation_enregistree():
    return render_template("reservation-enregistree.html")




#ne pas toucher! lance l'application
if __name__ == "__main__":
    app.run()
