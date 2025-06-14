from abc import ABC
from copy import deepcopy
from io import StringIO

class Component(ABC):
    def print_me(self, out, prefix='', is_tail=True):
        pass

    def clone(self):
        return deepcopy(self)


class Host(Component):
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_me(self, out, prefix='', is_tail=True):
        line = f"{prefix}{'\\-' if is_tail else '|-'}Host: {self.name}"
        out.write(line + '\n')

        for i, child in enumerate(self.children):
            is_last = (i == len(self.children) - 1)
            child.print_me(out, prefix + ('  ' if is_tail else '| '), is_last)

    def clone(self):
        new_host = Host(self.name)
        new_host.children = [child.clone() for child in self.children]
        return new_host


class IPAddress(Component):
    def __init__(self, ip):
        self.ip = ip

    def print_me(self, out, prefix='', is_tail=True):
        line = f"{prefix}{'\\-' if is_tail else '|-'}{self.ip}"
        out.write(line + '\n')

    def clone(self):
        return IPAddress(self.ip)


class CPU(Component):
    def __init__(self, cores, frequency):
        self.cores = cores
        self.frequency = frequency

    def print_me(self, out, prefix='', is_tail=True):
        line = f"{prefix}{'\\-' if is_tail else '|-'}CPU, {self.cores} cores @ {self.frequency}MHz"
        out.write(line + '\n')

    def clone(self):
        return CPU(self.cores, self.frequency)


class Memory(Component):
    def __init__(self, size):
        self.size = size

    def print_me(self, out, prefix='', is_tail=True):
        line = f"{prefix}{'\\-' if is_tail else '|-'}Memory, {self.size} MiB"
        out.write(line + '\n')

    def clone(self):
        return Memory(self.size)


class Disk(Component):
    def __init__(self, disk_type, size):
        self.disk_type = disk_type
        self.size = size
        self.partitions = []

    def add_partition(self, partition):
        self.partitions.append(partition)

    def print_me(self, out, prefix='', is_tail=True):
        line = f"{prefix}{'\\-' if is_tail else '|-'}{self.disk_type}, {self.size} GiB"
        out.write(line + '\n')
        for i, part in enumerate(self.partitions):
            is_last = (i == len(self.partitions) - 1)
            part.print_me(out, prefix + ('  ' if is_tail else '| '), is_last)

    def clone(self):
        new_disk = Disk(self.disk_type, self.size)
        new_disk.partitions = [p.clone() for p in self.partitions]
        return new_disk


class Partition(Component):
    def __init__(self, index, size, label):
        self.index = index
        self.size = size
        self.label = label

    def print_me(self, out, prefix='', is_tail=True):
        line = f"{prefix}{'\\-' if is_tail else '|-'}[{self.index}]: {self.size} GiB, {self.label}"
        out.write(line + '\n')

    def clone(self):
        return Partition(self.index, self.size, self.label)