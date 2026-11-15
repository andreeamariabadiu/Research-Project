import os
import shutil
from pathlib import Path


def save_uploaded_file(uploaded_file, upload_dir: str) -> str:
    """Saves an uploaded file object (Flask, FastAPI, or file-like object) to a directory safely."""
    upload_path = Path(upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)

    filename = getattr(uploaded_file, "filename", "uploaded_file")
    safe_filename = os.path.basename(filename)
    destination = upload_path / safe_filename

    if hasattr(uploaded_file, "save"):
        # Flask / Werkzeug FileStorage
        uploaded_file.save(str(destination))
    elif hasattr(uploaded_file, "file"):
        # FastAPI / Starlette UploadFile
        with open(destination, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)
    else:
        # Standard file-like object or bytes
        content = (
            uploaded_file.read()
            if hasattr(uploaded_file, "read")
            else uploaded_file
        )
        mode = "wb" if isinstance(content, bytes) else "w"
        with open(destination, mode) as buffer:
            buffer.write(content)

    return str(destination)
