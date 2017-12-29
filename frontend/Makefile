run-local:
	FLASK_APP=frontend/main.py python -m flask run

run-uwsgi-gateway:
	uwsgi --ini uwsgi_gateway.ini

run-uwsgi-http:
	uwsgi --ini uwsgi_http.ini

.PHONY: run-local run-uwsgi-gateway run-uwsgi-http
