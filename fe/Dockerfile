FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app/frontend

EXPOSE 3031

CMD [ "uwsgi", "--ini", "uwsgi_uwsgi_mount.ini" ]
