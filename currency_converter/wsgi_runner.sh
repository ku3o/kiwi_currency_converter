#!/usr/bin/env bash

uwsgi --socket 0.0.0.0:8080 --protocol=http --manage-script-name --plugins python3 --mount /=wsgi:app
