# Distributed under terms of the MIT license.

import time
from flask import *
from datetime import datetime
from datetime import date
import sys
import psycopg2
import psycopg2.extras
 
#NE PAS MODIFIER LA LIGNE SUIVANTE
"""
"""
#######################
# CONNEXION BDD
#######################

def pgsql_connect():
    try:
        db = psycopg2.connect("host=dbserver.emi.u-bordeaux.fr dbname=fpizzacoca user=fpizzacoca")
        return db
    except Exception as e :
        erreur_pgsql("Désolé, connexion impossible actuellement.", e)


def pgsql_init_db():
    db = pgsql_connect()
    cursor = db.cursor()
    try:
        with app.open_ressource('static/01_creation_hotel.sql') as f:
            cursor.execute(f.read().decode('utf8'))
        db.commit()
        with app.open_ressource('static/02_hotel_function.sql') as f:
            cursor.execute(f.read().decode('utf8'))
        db.commit()
        with app.open_ressource('static/03_hotel_contrainte.sql') as f:
            cursor.execute(f.read().decode('utf8'))
        db.commit()
        with app.open_ressource('static/04_insertion_hotel.sql') as f:
            cursor.execute(f.read().decode('utf8'))
        db.commit()
        # close communication
        cursor.close()
        db.close()
        return rows
    except Exception as e :
        erreur_pgsql("Le renouvellement de la BDD a rencontré un problème.", e)

#######################
# REQUETES BDD
#######################
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

def pgsql_update(command, param):
    print(command, param)

    db = pgsql_connect()
    # pour récupérer les attributs des relations
    # cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor = db.cursor()
    try:
        modif = cursor.execute(command, param)
        #row = cursor.fetchall()
        # enregistrement
        db.commit()
        # close communication
        cursor.close()
        db.close()
        return modif
    except Exception as e :
        erreur_pgsql("Désolé, service indisponible actuellement.", e)


####################### 
# MODIFS BASE SQL
#######################

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
#def pgsql_display_chambre (idchambre):
#    return pgsql_select('select * from HotelBis.Chambre where mail = ''))

####################### 
#NE SURTOUT PAS MODIFIER     
####################### 
if __name__ == "__main__":
   app.run(debug=True)

####################### 
# erreurs plsql
#######################

def erreur_pgsql(mess, e):
        flash(str(e))
        return redirect(url_for('accueil', errors=str(mess)))




#######################
#VARIABLES DE SESSION
#######################

'''Assignation des variables de session du client '''
def session_client(identite):
    session['num_client']= identite[0][0]
    print (session['num_client'])
    session['nom']= identite[0][1]
    session['prenom']= identite[0][2]
    session['email']= identite[0][3]
    session['password']= identite[0][4]
    session['categorie']= identite[0][5]
    today = date.today()
    session['jour'] = today.strftime("%Y-%m-%d")

    return True

def session_chambre(chambre):
    session['num_chambre']= chambre[0][0]
    session['tarif_chambre']= chambre[0][1]
    session['nom_chambre']= chambre[0][2]
    session['photo_chambre']= chambre[0][3]
    return True

def session_reservations(reservation):
    session['num_facture']= reservation[0][0]
    print("num_facture : ",session['num_facture'])
    session['num_client']= reservation[0][1]
    print("num_client : ",session['num_client'])
    session['num_chambre']= reservation[0][2]
    print("num_client : ",session['num_client'])
    session['date_debut']= reservation[0][3].strftime("%Y-%m-%d")
    print("date_debut : ",session['date_debut'])
    session['date_fin']= reservation[0][4].strftime("%Y-%m-%d")
    print("date_fin : ",session['date_fin'])
    session['status_facture']= reservation[0][5]
    return True


#######################
# Appel des variables de session
#######################

'''Recherche des informations sur le client à partir de son num_client '''
def infos_client_num(num_client):
    identite = pgsql_select('SELECT * FROM Hotel.clients '\
            ' WHERE num_client = (%s) ;',\
            [num_client])
    session_client(identite)

'''Recherche des informations sur le client à partir de son mail '''
def infos_client_mail(mail):
    identite = pgsql_select('SELECT * FROM Hotel.clients '\
            ' WHERE mail = (%s) ;',\
            [mail])
    print(identite)
    session_client(identite)


''' Recherche des informations de la réservation à partir du numéro de facture'''
def infos_reservation (num_facture):
    informations_reservation = pgsql_select('SELECT * FROM Hotel.reservations '\
            ' WHERE num_facture = (%s) ;',\
            [num_facture])
    session_reservations(informations_reservation)
    return informations_reservation

''' Recherche des informations de la chambre à partir de son numéro'''
def infos_chambre_nom(nom_chambre):
    chambre = pgsql_select('SELECT * FROM hotel.chambres WHERE nom_chambre = (%s) ;',\
            [nom_chambre])
    session_chambre(chambre)
    return chambre

''' Recherche des informations de la chambre à partir de son nom'''
def infos_chambre_num(num_chambre):
    chambre = pgsql_select('SELECT * FROM hotel.chambres WHERE num_chambre = (%s) ;', [num_chambre])
    session_chambre(chambre)
    return chambre

'''Cette fonction récupère les informations de la chambre'''
def oldinfos_chambre(chambre):
    try:
        chambre = pgsql_select('SELECT * FROM Hotel.chambres WHERE nom_chambre = (%s) ;', [chambre])
        print(chambre)
        session_chambre(chambre)
        return chambre
    except Exception as e :
        erreur_pgsql("Vous devez être connecté.", e)

#######################
# Table clients
#######################
'''Calcul du prix de location de la chambre'''
def cout_nuitees(num_chambre , date_debut, date_fin) :
#    return pgsql_select('SELECT tarif_chambre FROM Hotel.Clients WHERE categorie = (%s) ORDER BY mail ;', [categorie])
    debut = datetime.strptime(date_debut, "%Y-%m-%d") 
    fin = datetime.strptime(date_fin, "%Y-%m-%d") 
    prix = (datetime.strptime(date_fin, "%Y-%m-%d")-datetime.strptime(date_debut ,"%Y-%m-%d")).days * session['tarif_chambre']
    return prix

'''Insertion d'un nouveau client'''
def pgsql_ajout_client(newnom,newprenom,newmail,newpassword):
    return pgsql_insert('insert into Hotel.Clients values(DEFAULT,(%s), (%s),(%s),(%s));',\
            [newnom, newprenom, newmail, newpassword])

    '''Récupération des informations du client 
- mail du client passé en paramètre'''
def fiche_client(who):
    try:
        identite = pgsql_select('SELECT * FROM Hotel.Clients WHERE mail = (%s) ;', [who])
        session_client(identite)
        if identite :
            today = date.today()
            cejour = today.strftime("%Y-%m-%d")
            print (who, cejour)
            num_user = session['num_client']
            try :
                sejour = pgsql_select('SELECT * FROM Hotel.reservations'\
                        ' WHERE num_client = (%s) '\
                        ' AND date_debut < (%s)'\
                        ' AND date_fin > (%s) ;', [num_user, cejour, cejour ])
                if sejour :
                    session['sejour'] = True
                else :
                    session['sejour'] = False
            except Exception as e :
                erreur_pgsql("Probleme requete sur table reservations.", e)
                return False
            return True
    except Exception as e :
        erreur_pgsql("Vous devez être connecté.", e)
        return False

def nouveau_client_in_base():
    prenom = (session['prenom'])
    nom = (session['nom'])
    email = (session['email'])
    mdp = (session['mdp'])
    categorie = (session['categorie'])
    result = pgsql_update('INSERT INTO Hotel.clients ( prenom, nom, mail, mdp, categorie ) VALUES ( (%s), (%s), (%s), (%s), (%s) );',\
            [nom, prenom, email, mdp, categorie] )
    return True

def modif_client_in_base(num_client):
    prenom = (session['prenom'])
    nom = (session['nom'])
    email = (session['email'])
    result = pgsql_update('UPDATE Hotel.clients SET prenom = (%s), nom = (%s), mail = (%s) WHERE clients.num_client = (%s) ;',\
            [prenom, nom, email, num_client] )
    return result

'''Comparaison avec le mot de passe renseigné
- mot de passe passé en parametre'''
def verif_id(identifiant, mdp):
    #print (identifiant, mdp)
    try:
        num_client = pgsql_select('SELECT num_client FROM Hotel.Clients WHERE mail = (%s) AND mdp = (%s);', [identifiant, mdp])
        if num_client :
            return fiche_client(num_client)
        else :
            return False
    except Exception as e :
        erreur_pgsql("Mauvais identifiant.", e)
        return False

'''Cette fonction récupère la liste des mails des Clients par catégorie
- catégorie 'client' ou 'salarie' passé en parametre'''
def liste_mail(categorie):
    return pgsql_select('SELECT mail FROM Hotel.Clients WHERE categorie = (%s) ORDER BY mail ;', [categorie])

                
#######################
# table reservations
#######################

'''Annulation de la réservation'''
def annulation_reservation(numero_facture):
    facture = pgsql_update('DELETE FROM hotel.reservations '\
            ' WHERE reservations.num_facture = (%s) ;',\
            [numero_facture])
    return True

'''Paiement de la facture'''
def paiement_facture(numero):
    #facture = pgsql_select('SELECT * FROM hotel.reservations WHERE reservations.num_facture = (%s) ;', [numero])
    facture = pgsql_update('UPDATE hotel.reservations '\
            ' SET payee = True ' \
            ' WHERE reservations.num_facture = (%s) ;',\
            [numero])
    infos_reservation(numero)

'''Récupération des factures'''
def liste_reservations(who):
    reservations = pgsql_select('SELECT * FROM hotel.reservations WHERE num_client = (%s) ORDER BY reservations.date_debut ;', [who])
    if reservations != []:
        try:
            session_reservations(reservations)
            chambre = session['num_chambre']
            reservations = pgsql_select('SELECT * '\
                    ' FROM hotel.reservations , '\
                    ' hotel.chambres '\
                    ' WHERE reservations.num_client = (%s) '\
                    ' AND chambres.num_chambre = reservations.num_chambre ;',\
                    [who])
            return reservations
            
        except Exception as e :
            erreur_pgsql("Désolé, pb base de données.", e)
    else:
        session['num_facture']= ""
        session['num_chambre']= ""
        session['date_debut']= ""
        session['date_fin']= ""
        session['status_facture']= "" 
        return reservations

'''vérification des créneaux disponibles '''
''' Fonction non utilisée
def verif_creneau(table, arrivee, depart, chambre):
    verification = pgsql_select('SELECT * FROM Hotel.{} '\
                    ' WHERE date_debut >= (%s) AND date_debut < (%s) '\
                    ' AND num_chambre = (%s) ;'.format(table), [ arrivee , depart , chambre ])
    return verification
'''

'''Verification de disponibilité d'une chambre'''
def verif_date_reservation(depart, arrivee):
    print("##################### verif_date_reservations ##########################")
    start_date = datetime.strptime(arrivee, "%Y-%m-%d")
    end_date = datetime.strptime(depart,  "%Y-%m-%d")
    print (start_date, end_date, session['tarif_chambre'])
    devis = cout_nuitees(session['num_chambre'], arrivee, depart )
    devis = (datetime.strptime(depart, "%Y-%m-%d")-datetime.strptime(arrivee ,"%Y-%m-%d")).days * session['tarif_chambre']
    print ("devis : ", devis)
    if devis > 0:
        chambre = session['num_chambre']
        client = session['num_client']
        #verif_date_debut = verif_creneau('reservations', depart, arrivee, chambre)
        verif_date_debut = pgsql_select('SELECT * FROM Hotel.reservations '\
                ' WHERE date_debut >= (%s) AND date_debut < (%s) '\
                ' AND num_chambre = (%s) ;', [arrivee , depart , chambre ])
        #verif_date_fin = verif_creneau('reservations', depart, arrivee, chambre)
        verif_date_fin = pgsql_select('SELECT * FROM Hotel.reservations '\
                ' WHERE date_fin >= (%s) AND date_fin <= (%s) '\
                ' AND num_chambre = (%s) ;', [depart , arrivee , chambre ])
        verif_date_debut_travaux = pgsql_select('SELECT * FROM Hotel.travaux '\
                ' WHERE date_debut >= (%s) AND date_debut < (%s) '\
                ' AND num_chambre = (%s) ;', [arrivee , depart , chambre ])
        verif_date_fin_travaux = pgsql_select('SELECT * FROM Hotel.travaux '\
                ' WHERE date_fin >= (%s) AND date_fin <= (%s) '\
                ' AND num_chambre = (%s) ;', [depart , arrivee , chambre ])
        #verif_date_debut_travaux = verif_creneau('travaux', depart, arrivee, chambre)
        #verif_date_fin_travaux = verif_creneau('travaux', depart, arrivee, chambre)
        print ("Verification d'une date de début de séjour : ", verif_date_debut,not verif_date_debut)
        print("Vérification d'une date de fin de séjour : ", verif_date_fin ,not verif_date_fin)
        print("Vérification d'une date de debut de travaux : ", verif_date_debut_travaux,not verif_date_debut_travaux )
        print("Vérification d'une date de fin de travaux : ", verif_date_fin_travaux,not verif_date_fin_travaux )
        if not verif_date_debut  \
                and not verif_date_fin  \
                and not verif_date_debut_travaux  \
                and not verif_date_fin_travaux : 
            print("Ecriture en base de données ")
            try :
                result = pgsql_update('INSERT INTO Hotel.reservations '\
                        '( num_client, num_chambre, date_debut, date_fin )'\
                        'VALUES ( (%s) , (%s) , (%s) , (%s) ) ; ' ,\
                        [ client, chambre, arrivee, depart ] )
                return devis
            except Exception as e :
                erreur_pgsql("Erreur  de lecture de la table reservations.", e)
                return False
            #session_reservations(result)
            #if session['num_facture']
            #verif = pgsql_select('SELECT num_facture FROM Hotel.reservations '\
            #        ' WHERE date_debut = (%s) ;', [])

            print ("resultat insertion reservation : ",result)
            print ("Dates demandées : ", arrivee, depart)
            print ("Montant du devis : ",devis)
            #if not result :
            #    return False
            #else :
        else :    
            print("Chambre non réservée")
            return False
    else:
        print("Chambre non réservée")
        return False

#######################
# table consommations
#######################

''' Récupération de la liste des consommations disponibles'''
def liste_consommables():
    try:
        consommations = pgsql_select('SELECT * FROM Hotel.restauration ORDER BY consommation ;', [])
        print (consommations)
        return consommations
    except Exception as e :
        erreur_pgsql("Erreur sur la table consommations.", e)
        return False
            
''' Vérification de la presence d"une ligne consommation existante'''
def test_conso (facture, produit):
    print("########## TEST CONSOMMATIONS ##########")
    try :
        conso_existante = pgsql_select('SELECT quantite FROM Hotel.consommations ' \
                ' WHERE consommations.num_facture =(%s) AND consommations.consommation = (%s) ;',\
                [ facture, produit ] )
    except Exception as e :
        erreur_pgsql("Erreur sur la table consommations.", e)
        return False
    if not conso_existante :
        conso_existante = 0
    else :
        conso_existante = conso_existante[0][0]
        conso_existante = int(conso_existante)
    return conso_existante

'''mise à jour de la table consommations'''
def maj_conso(conso_existante, qtite, total_conso, produit, facture, jour):
    print("##########MAJ CONSOMMATIONS ##########")
        
    '''calcul du total des consommations sur cette facture '''
    total_conso = conso_existante + qtite
    print("Total des consommations : ",total_conso)

    if conso_existante > 0 :
        try:
            pgsql_update('UPDATE Hotel.consommations ' \
                    ' SET quantite = (%s) '\
                    ' WHERE consommation = (%s) AND num_facture = (%s) ;',\
                    [total_conso, produit, facture] )
        except Exception as e :
            erreur_pgsql("Erreur sur la table consommations.", e)
            return False
    else :
        try:
            pgsql_update('INSERT INTO Hotel.consommations' \
                    ' (num_facture, jour_conso, consommation, quantite) '\
                    ' VALUES ( (%s), (%s), (%s), (%s) ) ; ',\
                    [facture, jour, produit, qtite] )
        except Exception as e :
            erreur_pgsql("Erreur sur la table consommations.", e)
            return False

#######################
# table restauration
#######################
def maj_restauration(produit, qtite):
    print("##########MAJ RESTAURATION ##########")
    try:
        stock = pgsql_select('SELECT reserve FROM Hotel.restauration ' \
                ' WHERE consommation = (%s) ;',\
                [ produit ] )
        print ("stock restauration : ",stock)
    except Exception as e :
        erreur_pgsql("Erreur sur la table restauration.", e)
        return False
    if not stock:
        stock = 0
    else :
        stock = stock[0][0]
        stock = int(stock)
    reste = stock - qtite
    print ("reste du stock = ",reste)
    if reste >= 0 :
        try:
            pgsql_update('UPDATE Hotel.restauration ' \
                    ' SET reserve = (%s) '\
                    ' WHERE consommation = (%s) ;',\
                    [reste, produit] )
            return True
        except Exception as e :
            erreur_pgsql("Erreur sur la table consommations.", e)
            return False
        stock = pgsql_select('SELECT reserve FROM Hotel.restauration ' \
                ' WHERE consommation = (%s) ;',\
                [ produit ] )
        print ("stock restauration apres modif : ",stock)
    else : 
        return False

#######################
# Table chambres
#######################
'''Cette fonction récupère la liste des noms de chambres
- pas de parametre '''
def liste_chambres():
    return pgsql_select('SELECT nom_chambre FROM Hotel.chambres ORDER BY nom_chambre ;', [])


'''Cette fonction récupère les dates de réservation de la chambre dont le nom est passé en argument'''
def reservations_chambre(chambre):
    print ("################reservation chambre####################")
    informations_reservation = pgsql_select('SELECT * FROM Hotel.reservations '\
            ' WHERE num_chambre = (%s) ;',\
            [chambre])
    print (informations_reservation)
    #session_reservations(informations_reservation)
    #session['duree_sejour'] = delta_jours ( session['date_debut'], session['date_fin'])
    #print(session['duree_sejour'])
    return informations_reservation

'''Cette fonction récupère les chambres disponibles aux dates passées en argument'''
def recherche_chambres(debut, fin):
    return pgsql_select('SELECT num_chambre FROM Hotel.reservations WHERE date_debut < (%s) AND date_fin > (%s) ;', [(debut, fin)])


#######################
# détails facture
#######################


def sql_details_facture(numero_facture):
    print ("################sql_detail_facture####################")
    
    # Récupération des informations de la chambre
    num_chambre = session['num_chambre']
    session_chambre(num_chambre)
    
    # Prix de la réservation pour la chambre
    reservation = pgsql_select('SELECT * FROM hotel.reservations WHERE num_facture = (%s) ;', [numero_facture])
    print("test",session_reservations(reservation))
    
    # Récupération des informations de consommation
    # isinstance(numero_facture, int)
    print ("numero de facture : ", numero_facture)
    consommations = pgsql_select('SELECT * FROM hotel.consommations WHERE num_facture = (%s) ORDER BY consommation ;', [numero_facture])
    print("Infos consommations chambre : " , consommations)
    if consommations :
        return consommations
    else :
        return ""
    
'''
    pgsql_update('DELETE ONLY FROM Hotel.reservations WHERE reservations.num_facture = (%s) ;' ,[numero])
    pgsql_update('INSERT INTO Hotel.reservations ' \
            ' ( num_facture, num_client, num_chambre, date_debut, date_fin, payee)'\
            ' VALUES ( (%s), (%s), (%s), (%s), true ) ;', \
            [ numero, session['num_chambre'] , session['date_debut'] , session['date_fin'] ] )
    facture = pgsql_select('SELECT * FROM hotel.reservations WHERE num_facture = (%s) ;', [numero])
    print(facture)
    return True
'''

#######################
# achat
#######################
'''Achat d'une consommation, fonction principale'''
def achat(produit, qtite):
    print("##########FONCTION ACHAT ##########")
    facture = session['numero_facture']
    qtite = int(qtite)
    today = date.today()
    session['jour'] = today.strftime("%Y-%m-%d")
    jour = session['jour'] 
    
    '''test et mise à jour de la table restauration'''
    verif_stock = maj_restauration(produit, qtite)

    '''mise à jour de la table consommations'''
    if verif_stock :
        '''test d'une ligne de conso déja existante pour ce produit et cette facture '''
        conso_existante = test_conso(facture, produit)

        maj_conso(conso_existante, qtite, conso_existante, produit, facture, jour)
    else :
        print("consommation impossible")
    
####################### 
# VUE / JOIN
#######################

'''Chambres disponibles suivant la période'''
def sql_dispo_date_choisie(debut, fin):
    debut = datetime.strptime(debut,"%Y-%m-%d")
    fin = datetime.strptime(fin, "%Y-%m-%d")
    print ("dates de réservation souhaitée ",debut, fin, type(debut), type(fin))
    try :
        chambres_dispos = pgsql_select('SELECT * '\
                ' FROM hotel.chambres '\
                ' CROSS JOIN hotel.reservations' \
                ' GROUP BY chambres.num_chambre,  '\
                ' chambres.tarif_chambre , chambres.nom_chambre, chambres.photo_chambre ,'\
                ' reservations.num_facture, reservations.num_client, reservations.num_chambre,'\
                ' reservations.date_debut , reservations.date_fin, reservations.payee;',[])
        print ("Liste des chambres disponibles ",chambres_dispos)
        return chambres_dispos
    except Exception as e :
        erreur_pgsql("Erreur sur la recherche.", e)
        return False


'''sommes des consommations'''
def detail_consommations_facture(numero_facture):
    print ("################ détail consommations facture ####################")
    print ("date de début : ", session['date_debut'], type(session['date_debut']) )
    session['total'] = cout_nuitees( session['num_chambre'] , session['date_debut'], session['date_fin'] ) 
    #numero_facture = int(numero_facture)
    try :
        consommations_facture = pgsql_select('SELECT * FROM hotel.detail_consommations '\
                ' WHERE num_facture = (%s)  ORDER BY consommation ;',\
                [numero_facture])
    except Exception as e :
        erreur_pgsql("Erreur sur la table consommations.", e)
        return False
    print("Total avant calcul : ",session['total'])
    total_boissons = 0
    if consommations_facture :
        for row in consommations_facture :
            total_boissons = total_boissons + row[4]
    else :
        consommations_facture = 0
    session['total'] = int(session['total']) + total_boissons
    print("Total apres calcul : ",session['total'])
    return consommations_facture

