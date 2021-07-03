# syntax=docker/dockerfile:1
FROM python:3.7-alpine  as app-server
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers python3-dev build-base openldap-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]


FROM osixia/openldap AS ldap-server
ENV LDAP_ORGANISATION="Lucas luz Feitosa - test"
ENV LDAP_DOMAIN="techinterview.com"
ENV LDAP_ADMIN_PASSWORD="123456"
# login DN: cn=admin,dc=techinterview,dc=com
COPY create_ou_users.ldif /container/service/slapd/assets/config/bootstrap/ldif/50-bootstrap.ldif