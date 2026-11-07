import ipaddress
import platform
import re
import subprocess


def ping_host(host: str, count: int = 4) -> subprocess.CompletedProcess:
    """Safely pings a host given by the user, preventing command injection.

    :param host: IPv4/IPv6 address or domain name to ping.
    :param count: Number of ICMP packets to send.
    :return: subprocess.CompletedProcess instance containing output.
    :raises ValueError: If the input host or count fails validation.
    :raises subprocess.CalledProcessError: If the ping command fails.
    """
    if not isinstance(count, int) or count <= 0:
        raise ValueError("Count must be a positive integer.")

    # Validate IP address
    is_valid = False
    try:
        ipaddress.ip_address(host)
        is_valid = True
    except ValueError:
        pass

    # Validate Hostname/Domain if not an IP address (RFC 1123 compliant)
    if not is_valid:
        hostname_pattern = r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*$"
        if re.match(hostname_pattern, host):
            is_valid = True

    if not is_valid:
        raise ValueError("Invalid host. Must be a valid IP address or domain name.")

    # Determine platform-specific ping parameter for count
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Command arguments passed as a list with shell=False (default) to avoid shell injection
    cmd = ["ping", param, str(count), host]

    return subprocess.run(cmd, capture_output=True, text=True, check=True)
