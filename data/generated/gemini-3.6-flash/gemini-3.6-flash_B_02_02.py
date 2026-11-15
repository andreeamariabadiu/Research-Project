import os
import pathlib
import uuid
from typing import Union

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".txt", ".csv"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB limit


def save_uploaded_file(
    file_obj,
    upload_directory: Union[str, pathlib.Path],
    max_size_bytes: int = MAX_FILE_SIZE_BYTES,
    allowed_extensions: set = ALLOWED_EXTENSIONS,
) -> str:
    """
    Securely saves an uploaded file to the specified directory.

    :param file_obj: File object (e.g., Flask/Django uploaded file or standard file stream)
    :param upload_directory: Directory where the file should be saved
    :param max_size_bytes: Maximum allowed file size in bytes
    :param allowed_extensions: Set of allowed file extensions (e.g., {'.png', '.pdf'})
    :return: Absolute string path to the saved file
    :raises ValueError: If filename is invalid, extension is disallowed, size limit is exceeded, or path traversal occurs.
    """
    # 1. Retrieve and sanitize initial filename
    filename = getattr(file_obj, "filename", None) or getattr(file_obj, "name", "")
    if not filename:
        raise ValueError("No valid filename provided.")

    # Strip directory components to prevent path traversal
    clean_filename = os.path.basename(filename.replace("\\", "/"))
    if not clean_filename or clean_filename in (".", ".."):
        raise ValueError("Invalid filename.")

    # 2. Validate file extension
    ext = os.path.splitext(clean_filename)[1].lower()
    if ext not in allowed_extensions:
        raise ValueError(f"File extension '{ext}' is not permitted.")

    # 3. Resolve upload path securely
    target_dir = pathlib.Path(upload_directory).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    # Use UUID for storage to completely neutralize malicious filenames and prevent overwrites
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    target_path = (target_dir / safe_filename).resolve()

    # Path traversal check: verify the final path is inside the intended target directory
    if not str(target_path).startswith(str(target_dir)):
        raise ValueError("Illegal file path detected.")

    # 4. Stream write and enforce file size limit
    file_stream = getattr(file_obj, "file", file_obj)
    if hasattr(file_stream, "seek"):
        file_stream.seek(0)

    total_bytes = 0
    chunk_size = 64 * 1024  # 64 KB chunks

    try:
        with open(target_path, "wb") as destination:
            while True:
                chunk = file_stream.read(chunk_size)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > max_size_bytes:
                    raise ValueError(
                        f"File size exceeds the limit of {max_size_bytes} bytes."
                    )
                destination.write(chunk)
    except Exception:
        # Clean up partially written file on failure
        if target_path.exists():
            target_path.unlink()
        raise

    return str(target_path)
