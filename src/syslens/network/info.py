import platform
import socket
import struct
import subprocess
from pathlib import Path

import psutil

UNAVAILABLE = "Unavailable"


def get_hostname() -> str:
    try:
        return socket.gethostname() or UNAVAILABLE
    except OSError:
        return UNAVAILABLE


def get_local_ip() -> str:
    try:
        addresses = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
    except (OSError, RuntimeError):
        return UNAVAILABLE

    for name, interface_addresses in addresses.items():
        if not stats.get(name) or not stats[name].isup:
            continue
        for address in interface_addresses:
            if address.family == socket.AF_INET and not address.address.startswith(
                "127."
            ):
                return address.address
    return UNAVAILABLE


def get_default_gateway() -> str:
    operating_system = platform.system()

    if operating_system == "Linux":
        try:
            lines = Path("/proc/net/route").read_text(encoding="utf-8").splitlines()
            for line in lines[1:]:
                fields = line.split()
                if len(fields) > 2 and fields[1] == "00000000":
                    gateway = struct.pack("<L", int(fields[2], 16))
                    return socket.inet_ntoa(gateway)
        except (OSError, ValueError, struct.error):
            return UNAVAILABLE

    elif operating_system == "Darwin":
        try:
            result = subprocess.run(
                ["route", "-n", "get", "default"],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
            for line in result.stdout.splitlines():
                key, separator, value = line.strip().partition(":")
                if separator and key == "gateway":
                    return value.strip() or UNAVAILABLE
        except (OSError, subprocess.SubprocessError):
            return UNAVAILABLE

    return UNAVAILABLE


def get_dns_servers() -> tuple[str, ...]:
    try:
        lines = Path("/etc/resolv.conf").read_text(encoding="utf-8").splitlines()
    except OSError:
        return (UNAVAILABLE,)

    servers = tuple(
        line.split()[1]
        for line in lines
        if line.strip().startswith("nameserver ") and len(line.split()) >= 2
    )
    return tuple(dict.fromkeys(servers)) or (UNAVAILABLE,)


def get_network_interfaces() -> tuple[str, ...]:
    try:
        active_names = {
            name for name, stats in psutil.net_if_stats().items() if stats.isup
        }
    except (OSError, RuntimeError):
        return (UNAVAILABLE,)

    return tuple(sorted(active_names)) or (UNAVAILABLE,)
