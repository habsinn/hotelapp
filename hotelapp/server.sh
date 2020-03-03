#! /bin/sh
#
# server.sh
# Copyright (C) 2020 fpizzacoca <fpizzacoca@westmale>
#
# Distributed under terms of the MIT license.
#


export FLASK_APP=webapp.py
export FLASK_DEBUG=1
flask run &
