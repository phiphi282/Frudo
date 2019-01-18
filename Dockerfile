FROM python:jessie

WORKDIR /var/opt/

COPY Django /var/opt/
COPY requirements.txt /var/opt/

RUN apt update && apt -y  -qq --force-yes install libsasl2-dev python-dev libldap2-dev libssl-dev && pip3 install -r requirements.txt && ./new_db.sh

COPY entrypoint.sh /var/opt/

CMD ["bash", "entrypoint.sh"]
