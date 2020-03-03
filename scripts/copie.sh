#               ! /bin/sh
#
# copie.sh
# Copyright (C) 2020 fpizzacoca <fpizzacoca@jaguar>
#
# Distributed under terms of the MIT license.
#


#echo "cp -r  ~/Bureau/espaces/www/flask-scripts ~/Bureau/espaces/www/flask-scripts.bak" 
#echo "cp -r  ~/Bureau/espaces/www/flask-scripts ~/Bureau/espaces/www/flask-scripts.bak" | bash
#echo "rm -rf  ~/Bureau/espaces/www/flask-scripts.bak" 
echo "rm -rf  ~/Bureau/espaces/www/flask-scripts/*" | bash
echo "cp -r ../* ~/Bureau/espaces/www/flask-scripts" 
echo "cp -r ../* ~/Bureau/espaces/www/flask-scripts"  | bash
echo "ls -al ~/Bureau/espaces/www/flask-scripts" 
echo "ls -al ~/Bureau/espaces/www/flask-scripts" | bash
