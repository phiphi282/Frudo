FROM python:jessie

WORKDIR /var/opt/

COPY Django /var/opt/
COPY requirements.txt /var/opt/
COPY cron_mail /etc/cron.d/cron_mail

RUN apt update && apt -y  -qq --force-yes install libsasl2-dev python-dev libldap2-dev libssl-dev cron && pip3 install -r requirements.txt && ./new_db.sh && chmod 0644 /etc/cron.d/cron_mail && crontab /etc/cron.d/cron_mail && touch /var/log/cron.log

COPY entrypoint.sh /var/opt/

CMD ["bash", "entrypoint.sh"]
