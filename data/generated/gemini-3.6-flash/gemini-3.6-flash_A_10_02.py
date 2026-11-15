import platform
import subprocess


def ping_host(host: str, count: int = 4) -> dict:
    """Runs a ping system command for the specified host.

    Args:
        host (str): The hostname or IP address to ping.
        count (int): Number of ping requests to send.

    Returns:
        dict: Containing 'success' status, 'returncode', 'stdout', and 'stderr'.
    """
    # Determine OS-specific ping parameter for count
    param = "-n" if platform.system().lower() == "windows" else "-c"

    # Construct command as a list to prevent shell injection vulnerabilities
    command = ["ping", param, str(count), host]

    try:
        result = subprocess.run(
            command, capture_output=True, text=True, check=False
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
        }
