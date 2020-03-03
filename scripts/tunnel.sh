#!/bin/sh

#où $1 est l'argument à passer lorsqu'on appelle le script. L'argument est le serveur distant sur lequel on se connecte en SSH (exemple: 'distant_escher' sur la configuraiton de ma machine tel que renseignée dans mon .ssh/config )
echo "ouverture du port local 127.0.0.1:33333 vers $1:5000"
echo "ssh -f hbelaribi@$1 -L 33333:localhost:5000 -N"
ssh -A -f hbelaribi@$1 -L 33333:localhost:5000 -N
