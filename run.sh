#!/bin/sh

# run the app via uwsgi on port http://127.0.0.1:8080

uwsgi --socket 0.0.0.0:8080 --protocol=http -w wsgi:app