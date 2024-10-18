#!/bin/sh

export KP_API_TOKEN="FCE2VJ9-C2K4Z3C-MVJGV8V-XEGG0AW"
python utils/top_secret.py
if ! command -v toilet > /dev/null 2>&1; then sudo apt install -y toilet; else echo ""; fi
for i in $(seq 1 3); do date '+%D %T' | toilet -f term -F border --gay; sleep 1; done
python manage.py runserver
