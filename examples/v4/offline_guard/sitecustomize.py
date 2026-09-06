"""Artifact-proof subprocess guard, enabled only by explicit PYTHONPATH."""

import sys


def refuse_network(event, args):
    if event in {"socket.connect", "socket.connect_ex", "socket.getaddrinfo",
                 "socket.gethostbyname", "socket.gethostbyaddr"}:
        raise RuntimeError("Offline artifact proof forbids network access")


sys.addaudithook(refuse_network)
