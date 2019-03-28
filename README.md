# cert-manager-charm

Issue and manage certificates and keys for private self-signed CAs

This charm is intended for use with easyrsa to issue client certificates
that can be given to external clients that need to communicate with services
secured by an easyrsa self-signed CA.

# Basic use

    juju deploy easyrsa
    juju deploy cert-mananger
    juju relate easyrsa cert-manager

Configure clients and servers (see config.yaml), then request the certificate and key with actions.
