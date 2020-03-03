#               ! /bin/sh
#
# copie.sh
# Copyright (C) 2020 fpizzacoca <fpizzacoca@jaguar>
#
# Distributed under terms of the MIT license.
#


echo "rm -rf  ~/Bureau/espaces/www/flask-scripts/*" | bash
echo "cp -r ../flask/flask-scripts ~/Bureau/espaces/www" | bash
echo "ls -al ~/Bureau/espaces/www/flask-scripts" | bash
