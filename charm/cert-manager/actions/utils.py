from charmhelpers.core import hookenv


def cert(cn, cert_type):
    with open('/etc/ssl/cert-manager/{}/{}.crt'.format(cert_type, cn),
              'r') as f:
        return f.read()


def key(cn, cert_type):
    with open('/etc/ssl/cert-manager/{}/private/{}.key'.format(cert_type, cn),
              'r') as f:
        return f.read()


def fail(msg):
    hookenv.action_set({'outcome': 'failure'})
    hookenv.action_fail(msg)


def ok_cert(result):
    hookenv.action_set({'cert': result, 'outcome': 'success'})


def ok_certkey(cert, key):
    hookenv.action_set({'cert': cert, 'key': key, 'outcome': 'success'})
