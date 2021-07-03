import ldap
from ldap import modlist
import os

LDAP_SERVER_ADRESS = os.environ.get('LDAP_SERVER_ADRESS', 'ldap://ldap_server:389')
LDAP_DC = os.environ.get('LDAP_DC')
LDAP_ADMIN_PW = os.environ.get('LDAP_ADMIN_PW')


def open_conn():
    ldap_admin_dn = 'cn=admin,' + LDAP_DC
    connection = ldap.initialize(LDAP_SERVER_ADRESS)
    connection.protocol_version = ldap.VERSION3
    connection.simple_bind_s(ldap_admin_dn, LDAP_ADMIN_PW)
    return connection


def create_user(uid, cn, sn, description):
    conn = open_conn()

    dn=f"cn={cn},ou=users," + LDAP_DC

    attrs = {}
    attrs['objectclass'] = ['inetOrgPerson'.encode('utf-8')]
    attrs['cn'] = cn.encode('utf-8')
    attrs['uid'] = uid.encode('utf-8')
    attrs['sn'] = sn.encode('utf-8')

    if description:
        attrs['description'] = description.encode('utf-8')

    ldif = modlist.addModlist(attrs)

    conn.add_s(dn, ldif)
    conn.unbind_s()