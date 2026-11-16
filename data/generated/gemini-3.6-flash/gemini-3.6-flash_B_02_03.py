import os
import re
from pathlib import Path


def save_uploaded_file(
    file_obj,
    destination_dir,
    original_filename,
    allowed_extensions=None,
    max_size_bytes=5 * 1024 * 1024,
):
    """Safely saves an uploaded file to the server.

    :param file_obj: File-like object (supports .read())
    :param destination_dir: Folder path where the file will be stored
    :param original_filename: Name of the uploaded file
    :param allowed_extensions: Set/list of permitted file extensions (e.g., {'png', 'jpg', 'pdf'})
    :param max_size_bytes: Maximum allowed size in bytes (default: 5MB)
    :return: Path object to the saved file
    """
    if allowed_extensions is None:
        allowed_extensions = {"png", "jpg", "jpeg", "gif", "pdf", "txt", "csv"}

    # 1. Sanitize filename to prevent path traversal and strip dangerous characters
    safe_name = os.path.basename(original_filename)
    safe_name = re.sub(r"[^a-zA-Z0-9_.-]", "_", safe_name)

    if not safe_name or safe_name.startswith("."):
        raise ValueError("Invalid filename.")

    # 2. Validate file extension
    ext = safe_name.rsplit(".", 1)[-1].lower() if "." in safe_name else ""
    if ext not in {e.lower().lstrip(".") for e in allowed_extensions}:
        raise ValueError(f"File extension '{ext}' is not allowed.")

    # 3. Ensure target directory isolation
    dest_path = Path(destination_dir).resolve()
    target_path = (dest_path / safe_name).resolve()

    try:
        # Prevents directory traversal tricks (e.g. symlinks pointing outside)
        target_path.relative_to(dest_path)
    except ValueError:
        raise ValueError("Path traversal attempt detected.")

    dest_path.mkdir(parents=True, exist_ok=True)

    # 4. Save file while strictly enforcing size limit during streaming
    total_bytes = 0
    chunk_size = 8192

    with open(target_path, "wb") as destination:
        while True:
            chunk = file_obj.read(chunk_size)
            if not chunk:
                break
            total_bytes += len(chunk)
            if total_bytes > max_size_bytes:
                destination.close()
                target_path.unlink(missing_ok=True)  # Clean up partial file
                raise ValueError(
                    f"File exceeds maximum allowed size of {max_size_bytes} bytes."
                )

            destination.write(chunk)

    return target_path
