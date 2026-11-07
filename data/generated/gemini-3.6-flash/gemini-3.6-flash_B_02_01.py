import os
import re
import uuid
from pathlib import Path
from typing import Union, Set, Optional

def save_uploaded_file(
    file_obj,
    upload_folder: Union[str, Path],
    allowed_extensions: Optional[Set[str]] = None,
    max_size_mb: float = 5.0
) -> Path:
    """
    Safely saves an uploaded file to the specified server directory.

    :param file_obj: File-like object (e.g., Flask/Django UploadedFile or standard IO stream).
    :param upload_folder: Target directory where file should be saved.
    :param allowed_extensions: Set of allowed extensions (e.g., {'.png', '.jpg', '.pdf'}).
    :param max_size_mb: Maximum allowed file size in megabytes.
    :return: Resolved absolute Path to the saved file.
    :raises ValueError: If file type is disallowed, path is invalid, or size limit is exceeded.
    """
    if allowed_extensions is None:
        allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".txt"}
    
    # Normalize extensions to lowercase with leading dot
    allowed_exts = {ext.lower() if ext.startswith('.') else f".{ext.lower()}" for ext in allowed_extensions}

    # Extract raw filename from common web framework attributes or fallback
    filename = getattr(file_obj, "filename", None) or getattr(file_obj, "name", "file")
    
    # 1. Path Traversal Prevention: Strip directory path components
    filename = Path(filename).name
    
    # Sanitize: Allow only alphanumeric, dashes, underscores, and dots
    filename = re.sub(r"[^\w\.-]", "_", filename)
    
    # Prevent hidden files or empty filenames
    if not filename or filename.startswith("."):
        filename = f"upload_{uuid.uuid4().hex[:8]}"

    # 2. Extension Validation
    ext = Path(filename).suffix.lower()
    if not ext or ext not in allowed_exts:
        raise ValueError(f"Forbidden file extension: '{ext}'. Allowed: {', '.join(sorted(allowed_exts))}")

    # Ensure upload directory absolute path resolution
    base_dir = Path(upload_folder).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    
    dest_path = (base_dir / filename).resolve()
    
    # Verify the final path remains inside the designated target directory
    try:
        dest_path.relative_to(base_dir)
    except ValueError:
        raise ValueError("Invalid target path: path traversal detected.")

    # 3. File Size Limit Check & Safe Write
    max_bytes = int(max_size_mb * 1024 * 1024)
    stream = getattr(file_obj, "stream", file_obj)

    if hasattr(stream, "seek"):
        stream.seek(0)

    written_bytes = 0
    chunk_size = 64 * 1024  # 64 KB chunks

    try:
        with open(dest_path, "wb") as out_file:
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                written_bytes += len(chunk)
                if written_bytes > max_bytes:
                    raise ValueError(f"File size exceeds maximum allowed limit of {max_size_mb} MB.")
                out_file.write(chunk)
    except Exception:
        # Clean up partial file on failure or size exceedance
        if dest_path.exists():
            dest_path.unlink()
        raise

    return dest_path
