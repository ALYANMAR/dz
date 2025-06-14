import socket
import psutil
from components import IPAddress, CPU, Memory, Disk, Partition


def get_ip_addresses():
    """Получить все IPv4-адреса"""
    addresses = []
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                addresses.append(IPAddress(addr.address))
    return addresses


def get_cpu_info():
    """Получить информацию о процессоре"""
    cores = psutil.cpu_count(logical=False)  # Количество физических ядер
    frequency = psutil.cpu_freq().current if psutil.cpu_freq() else 0  # Частота процессора

    return CPU(
        cores=cores,
        frequency=int(frequency * 1000)  # Переводим в МГц
    )

def get_memory_info():
    """Получить информацию о памяти"""
    mem = psutil.virtual_memory()
    return Memory(size=int(mem.total / (1024 * 1024)))  # В мегабайтах


def get_disk_partitions():
    """Получить информацию о дисках и разделах"""
    disks = []

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk = Disk(disk_type=partition.fstype, size=int(usage.total / (1024 * 1024 * 1024)))  # Гигабайты

            # Добавляем разделы (примерно один на диск)
            disk.add_partition(Partition(
                index=0,
                size=int(usage.used / (1024 * 1024 * 1024)),
                label="used"
            ))
            disk.add_partition(Partition(
                index=1,
                size=int(usage.free / (1024 * 1024 * 1024)),
                label="free"
            ))

            disks.append(disk)
        except PermissionError:
            continue

    return disks