import ldap
from ldap import modlist
from ldap.controls.libldap import SimplePagedResultsControl
import os

LDAP_SERVER_ADRESS = os.environ.get('LDAP_SERVER_ADRESS')
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
    attrs['objectclass'] = [x.encode('utf-8') for x in ['inetOrgPerson', 'top', 'organizationalPerson', 'person']]
    attrs['cn'] = cn.encode('utf-8')
    attrs['uid'] = uid.encode('utf-8')
    attrs['sn'] = sn.encode('utf-8')

    if description:
        attrs['description'] = description.encode('utf-8')

    ldif = modlist.addModlist(attrs)

    conn.add_s(dn, ldif)
    conn.unbind_s()



def get_user(uid):
    conn = open_conn()

    ldap_filter = f'(uid={uid})'
    base = 'ou=users,' + LDAP_DC
    res = conn.search_s(base, ldap.SCOPE_SUBTREE, ldap_filter)
    conn.unbind_s()
    data = None
    if res:
        data = res[0][1]
        for key in data:
            data[key] = data[key][0].decode('utf-8')

    return data


def get_users():
    conn = open_conn()

    page_control = SimplePagedResultsControl(True, size=500, cookie="")

    ldap_filter = 'objectClass=inetOrgPerson'
    base = 'ou=users,' + LDAP_DC
    response = conn.search_ext(
        base,
        ldap.SCOPE_SUBTREE,
        ldap_filter,
        [],
        serverctrls=[page_control],
    )
    result = []
    pages = 0
    while True:
        pages += 1
        rtype, rdata, rmsgid, serverctrls = conn.result3(response)
        result.extend(rdata)
        controls = [
            control
            for control in serverctrls
            if control.controlType == SimplePagedResultsControl.controlType
        ]
        if not controls:
            break
        if not controls[0].cookie:
            break
        page_control.cookie = controls[0].cookie
        response = conn.search_ext(
            base,
            ldap.SCOPE_SUBTREE,
            ldap_filter,
            [],
            serverctrls=[page_control],
        )

    conn.unbind_s()

    for index, user in enumerate(result):
        data = user[1]
        for key in data:
            data[key] = data[key][0].decode('utf-8')
        result[index] = data

    return result


def delete_user(cn):
    conn = open_conn()
    filter = f'cn={cn},ou=users,' + LDAP_DC
    conn.delete_s(filter)
    conn.unbind_s()


def update_user(uid, sn, description):
    sucess = False
    conn = open_conn()

    ldap_filter = f'(uid={uid})'
    base = 'ou=users,' + LDAP_DC
    res = conn.search_s(base, ldap.SCOPE_SUBTREE, ldap_filter)
    if res:
        data = res[0]
        dn = data[0]
        old = data[1]

        new = {**old}
        if sn:
            new['sn'] = [sn.encode('utf-8')]
        if description:
            new['description'] = [description.encode('utf-8')]

        ldif = modlist.modifyModlist(old,new)
        conn.modify_s(dn,ldif)
        sucess = True

    return sucess