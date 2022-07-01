#!/bin/sh
clear
rm -r ./flask_server/static/js/*
tsc
python ./master_router.py
