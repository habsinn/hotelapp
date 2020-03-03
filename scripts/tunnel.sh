#!/bin/sh
echo "ouverture du port local 127.0.0.1:33333 vers $1:5000"
echo "ssh -f hbelaribi@$1 -L 33333:localhost:5000 -N"
ssh -A -f hbelaribi@$1 -L 33333:localhost:5000 -N
