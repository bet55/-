export KP_API_TOKEN="FCE2VJ9-C2K4Z3C-MVJGV8V-XEGG0AW"
python utils/top_secret.py
for i in {1..3}; do echo "$(date '+%D %T' | toilet -f term -F border --gay)"; sleep 1; done
python manage.py runserver
