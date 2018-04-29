FROM python:jessie

WORKDIR /var/opt/

COPY Django /var/opt/

RUN pip3 install django && ./new_db.sh

COPY entrypoint.sh /var/opt/

CMD ["bash", "entrypoint.sh"]
