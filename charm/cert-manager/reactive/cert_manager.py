import os
import yaml

from charmhelpers.core import hookenv

from charms.reactive import when, when_not, set_flag
from charms.reactive.helpers import data_changed

from charms.layer.tls_client import request_client_cert, request_server_cert


@when_not('cert-manager.installed')
def install():
    os.makedirs('/etc/ssl/cert-manager/clients', exist_ok=True)
    os.makedirs('/etc/ssl/cert-manager/clients/private', mode=0o700,
                exist_ok=True)
    os.makedirs('/etc/ssl/cert-manager/servers', exist_ok=True)
    os.makedirs('/etc/ssl/cert-manager/servers/private', mode=0o700,
                exist_ok=True)
    set_flag('cert-manager.installed')


@when('endpoint.certificates.joined')
def cerfificates_joined():
    clients = yaml.load(hookenv.config().get('clients'))
    servers = yaml.load(hookenv.config().get('servers'))
    if clients:
        request_client_certs(clients)
    if servers:
        request_server_certs(servers)

    if clients or servers:
        hookenv.status_set('active',
                           '{} client, '
                           '{} server certs'.format(len(clients),
                                                    len(servers)))


@when('certificates.available')
@when('config.changed')
def config_changed():
    if data_changed('cert-manager.clients', hookenv.config().get('clients')):
        clients = yaml.load(hookenv.config().get('clients'))
        request_client_certs(clients)
    else:
        clients = []
    if data_changed('cert-manager.servers', hookenv.config().get('servers')):
        servers = yaml.load(hookenv.config().get('servers'))
        request_server_certs(servers)
    else:
        servers = []
    hookenv.status_set('active',
                       '{} client, '
                       '{} server certs'.format(len(clients), len(servers)))


def request_client_certs(clients):
    try:
        for client in clients:
            cn = client['common_name']
            hookenv.log('requesting client cert for {}'.format(cn))
            request_client_cert(cn, client.get('sans', []),
                                crt_path='/etc/ssl/cert-manager/clients/'
                                         '{}.crt'.format(cn),
                                key_path='/etc/ssl/cert-manager/clients/'
                                         'private/{}.key'.format(cn))
    except Exception as e:
        hookenv.log('"clients" config setting is invalid: {}'.format(e))
        hookenv.status_set('blocked',
                           '"clients" config setting is invalid')
        return


def request_server_certs(servers):
    try:
        for server in servers:
            cn = server['common_name']
            hookenv.log('requesting server cert for {}'.format(cn))
            request_server_cert(cn, server.get('sans', []),
                                crt_path='/etc/ssl/cert-manager/servers/'
                                         '{}.crt'.format(cn),
                                key_path='/etc/ssl/cert-manager/servers/'
                                         'private/{}.key'.format(cn))
    except Exception as e:
        hookenv.log('"servers" config setting is invalid: {}'.format(e))
        hookenv.status_set('blocked',
                           '"servers" config setting is invalid')
        return
