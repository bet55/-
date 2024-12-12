#!/bin/sh

export KP_API_TOKEN=""
python utils/top_secret.py
#if ! command -v toilet > /dev/null 2>&1; then sudo apt install -y toilet; else echo ""; fi
#for i in $(seq 1 1); do date '+%D %T' | toilet -f term -F border --gay; sleep 0; done
python manage.py runserver 185.80.91.29:8000
