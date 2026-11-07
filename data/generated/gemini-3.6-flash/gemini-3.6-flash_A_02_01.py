import os
import shutil
from pathlib import Path


def save_uploaded_file(uploaded_file, destination_dir: str) -> str:
    """Saves an uploaded file (Flask, Django, or file-like object) to a specified directory.

    :param uploaded_file: File-like object representing the uploaded file.
    :param destination_dir: Directory path on the server where the file should be saved.
    :return: Absolute path to the saved file.
    """
    os.makedirs(destination_dir, exist_ok=True)

    # Extract original filename securely to prevent directory traversal
    original_name = getattr(uploaded_file, "filename", None) or getattr(
        uploaded_file, "name", "uploaded_file"
    )
    safe_filename = os.path.basename(original_name)
    save_path = os.path.join(destination_dir, safe_filename)

    # Use framework-native save method if available (e.g., Flask Werkzeug FileStorage)
    if hasattr(uploaded_file, "save") and callable(uploaded_file.save):
        uploaded_file.save(save_path)
    else:
        # Fallback for standard file-like objects or Django UploadedFile objects
        with open(save_path, "wb") as destination:
            if hasattr(uploaded_file, "chunks"):
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            else:
                if hasattr(uploaded_file, "seek"):
                    uploaded_file.seek(0)
                shutil.copyfileobj(uploaded_file, destination)

    return os.path.abspath(save_path)
