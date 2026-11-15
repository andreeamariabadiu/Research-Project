import ipaddress
import platform
import re
import subprocess


def safe_ping(host: str, count: int = 4) -> subprocess.CompletedProcess:
    """Safely pings a host after validating the input to prevent command injection.

    :param host: IPv4 address, IPv6 address, or hostname to ping.
    :param count: Number of ICMP packets to send.
    :return: subprocess.CompletedProcess instance containing execution details.
    """
    # 1. Input Validation
    if not isinstance(host, str) or not host.strip():
        raise ValueError("Host must be a non-empty string.")

    host = host.strip()

    is_valid = False

    # Check if host is a valid IPv4 or IPv6 address
    try:
        ipaddress.ip_address(host)
        is_valid = True
    except ValueError:
        pass

    # If not an IP, validate as a standard RFC 1123 hostname
    if not is_valid:
        hostname_regex = re.compile(
            r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*"
            r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$"
        )
        if len(host) <= 253 and hostname_regex.match(host):
            is_valid = True

    if not is_valid:
        raise ValueError(f"Invalid hostname or IP address: {host!r}")

    # Validate count parameter
    if not isinstance(count, int) or count <= 0 or count > 100:
        raise ValueError("Count must be an integer between 1 and 100.")

    # 2. Safely Construct Command
    # Determine platform-specific flag for packet count
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Pass command as a list of arguments and set shell=False to avoid command injection
    command = ["ping", param, str(count), host]

    # 3. Execution
    return subprocess.run(
        command,
        shell=False,
        capture_output=True,
        text=True,
        check=True,
    )
