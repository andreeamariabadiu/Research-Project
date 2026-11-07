import platform
import subprocess


def ping_host(host: str, count: int = 4) -> tuple[int, str]:
    """Pings a host and returns the exit code and command output.

    :param host: Hostname or IP address to ping.
    :param count: Number of ICMP packets to send.
    :return: A tuple of (exit_code, output_text).
    """
    # Choose parameter based on OS (-n for Windows, -c for Unix-like systems)
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Command arguments passed as a list to prevent shell injection vulnerabilities
    command = ["ping", param, str(count), host]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        return result.returncode, result.stdout
    except Exception as e:
        return -1, str(e)
