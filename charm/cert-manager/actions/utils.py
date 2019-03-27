import sys

from charmhelpers.core import hookenv


def fail(msg):
    hookenv.action_set({'outcome': 'failure'})
    hookenv.action_fail(msg)
    sys.exit()


def ok(result):
    hookenv.action_set({'raw', result})
    hookenv.action_set({'outcome', 'success'})
