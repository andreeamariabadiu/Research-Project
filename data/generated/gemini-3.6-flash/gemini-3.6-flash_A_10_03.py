import platform
import subprocess


def ping_host(host: str, count: int = 4) -> tuple[int, str]:
    """Pings a host safely using subprocess.run to prevent command injection.

    Returns a tuple of (return_code, output).
    """
    # Determine the parameter for count based on the operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Pass command arguments as a list to avoid shell injection vulnerabilities
    command = ["ping", param, str(count), host]

    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        return result.returncode, result.stdout
    except Exception as e:
        return -1, str(e)
