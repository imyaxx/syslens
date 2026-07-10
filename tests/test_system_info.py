from syslens.system.info import (
    get_architecture,
    get_hostname,
    get_kernel,
    get_operating_system,
    get_python_version,
)


def test_get_hostname_returns_non_empty_string() -> None:
    value = get_hostname()
    assert isinstance(value, str)
    assert value


def test_get_operating_system_returns_non_empty_string() -> None:
    value = get_operating_system()
    assert isinstance(value, str)
    assert value


def test_get_kernel_returns_non_empty_string() -> None:
    value = get_kernel()
    assert isinstance(value, str)
    assert value


def test_get_architecture_returns_non_empty_string() -> None:
    value = get_architecture()
    assert isinstance(value, str)
    assert value


def test_get_python_version_returns_non_empty_string() -> None:
    value = get_python_version()
    assert isinstance(value, str)
    assert value
