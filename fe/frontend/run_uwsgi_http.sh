uwsgi --http :32770 --wsgi-file init.py --callable app --processes 1 --threads 1
