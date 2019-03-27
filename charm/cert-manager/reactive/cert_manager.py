import yaml

from charmhelpers.core import hookenv

from charms.reactive import when
from charms.reactive.helpers import data_changed

from charms.layer.tls_client import request_client_cert, request_server_cert


@when('certificates.available')
@when('config.changed')
def config_changed():
    if data_changed('cert-manager.clients', hookenv.config().get('clients')):
        try:
            clients = yaml.loads(hookenv.config().get('clients'))
            for client in clients:
                request_client_cert(common_name=client['common_name'],
                                    sans=client.get('sans', []))
        except Exception as e:
            hookenv.log('"clients" config setting is invalid: {}'.format(e))
            hookenv.status_set('blocked',
                               '"clients" config setting is invalid')
            return
    if data_changed('cert-manager.servers', hookenv.config().get('servers')):
        try:
            servers = yaml.loads(hookenv.config().get('servers'))
            for server in servers:
                request_server_cert(common_name=server['common_name'],
                                    sans=server.get('sans', []))
        except Exception as e:
            hookenv.log('"servers" config setting is invalid: {}'.format(e))
            hookenv.status_set('blocked',
                               '"servers" config setting is invalid')
            return
    hookenv.status_set('active', '')
