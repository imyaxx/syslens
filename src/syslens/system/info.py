import platform
import socket


def get_hostname() -> str:
    return socket.gethostname()


def get_operating_system() -> str:
    return platform.system()


def get_kernel() -> str:
    return platform.release()


def get_architecture() -> str:
    return platform.machine()


def get_python_version() -> str:
    return platform.python_version()
