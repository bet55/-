#rm db.sqlite3
#rm lists/migrations/*[0-9]*.py
python manage.py flush
python manage.py makemigrations
python manage.py migrate
