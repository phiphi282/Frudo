FROM python:jessie

WORKDIR /var/opt/

COPY Django /var/opt/
COPY requirements.txt /var/opt/

RUN pip3 install -r requirements.txt && ./new_db.sh

COPY entrypoint.sh /var/opt/

CMD ["bash", "entrypoint.sh"]
