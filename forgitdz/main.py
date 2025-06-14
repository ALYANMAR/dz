import socket
from io import StringIO


from network import Network
from components import Host
from system_info import get_ip_addresses, get_cpu_info, get_memory_info, get_disk_partitions
import socket


def create_local_host():
    """Создать хост с информацией о локальной машине"""
    host_name = socket.gethostname()
    host = Host(name=host_name)

    host.add_child(get_cpu_info())
    host.add_child(get_memory_info())
    host.add_child(get_ip_addresses()[0])  # Берём первый IP

    for disk in get_disk_partitions():
        host.add_child(disk)

    return host


def main():
    network = Network("Local Network")

    # Автоматически добавляем текущий компьютер
    local_host = create_local_host()
    network.add_host(local_host)

    # Вывод структуры
    output = StringIO()
    network.print_me(output)
    print(output.getvalue())

    # Тестирование clone
    network_copy = network.clone()
    copied_host = network_copy.find_host_by_name(local_host.name)
    copied_host.name = "copied-host"

    print("\nOriginal after change:")
    output = StringIO()
    network.print_me(output)
    print(output.getvalue())

    print("\nCopy after change:")
    output = StringIO()
    network_copy.print_me(output)
    print(output.getvalue())


if __name__ == "__main__":
    main()