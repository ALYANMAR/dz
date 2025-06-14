from components import Component
import socket

class Network(Component):
    def __init__(self, name):
        self.name = name
        self.hosts = []

    def add_host(self, host):
        self.hosts.append(host)

    def print_me(self, out, prefix='', is_tail=True):
        out.write(f"{prefix}Network: {self.name}\n")
        for i, host in enumerate(self.hosts):
            is_last = (i == len(self.hosts) - 1)
            host.print_me(out, prefix + ('+-' if not is_last else '\\-'), is_last)

    def clone(self):
        new_network = Network(self.name)
        new_network.hosts = [host.clone() for host in self.hosts]
        return new_network

    def find_host_by_name(self, name):
        for host in self.hosts:
            if host.name == name:
                return host
        return None