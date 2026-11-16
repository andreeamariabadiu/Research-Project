import ipaddress
import platform
import re
import subprocess
from typing import Dict, Union


def safe_ping(host: str, count: int = 4) -> Dict[str, Union[bool, str]]:
    """Executes a system ping command safely, preventing command injection.

    :param host: IPv4/IPv6 address or hostname to ping.
    :param count: Number of ping packets to send.
    :return: A dictionary containing success status, stdout, and stderr.
    """

    # 1. Validate host input (IP address or hostname)
    def is_valid_host(val: str) -> bool:
        if not val or len(val) > 253:
            return False
        # Check if valid IPv4 or IPv6 address
        try:
            ipaddress.ip_address(val)
            return True
        except ValueError:
            pass

        # Check if valid Hostname / FQDN (RFC 1123)
        hostname_pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$"
        return bool(re.match(hostname_pattern, val))

    if not isinstance(host, str) or not is_valid_host(host):
        raise ValueError(f"Invalid host provided: {host!r}")

    # Validate count parameter to ensure integer bounds
    if not isinstance(count, int) or not (1 <= count <= 100):
        raise ValueError("Count must be an integer between 1 and 100.")

    # 2. Determine OS-specific ping arguments
    count_flag = "-n" if platform.system().lower() == "windows" else "-c"

    # 3. Construct command as a list to avoid shell execution
    cmd = ["ping", count_flag, str(count), host]

    # 4. Safely execute process without using shell=True
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
            shell=False,  # Prevents shell injection vulnerabilities
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": "Command timed out after 15 seconds.",
        }
