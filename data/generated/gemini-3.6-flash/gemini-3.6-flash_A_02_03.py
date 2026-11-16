import os
from werkzeug.utils import secure_filename


def save_uploaded_file(file_storage_object, target_folder):
    """Saves an uploaded file (e.g., from Flask request.files) safely to the server.

    :param file_storage_object: Werkzeug FileStorage object from request.files
    :param target_folder: Directory path on the server where file should be
    saved
    :return: Full path to the saved file
    """
    os.makedirs(target_folder, exist_ok=True)
    filename = secure_filename(file_storage_object.filename)
    save_path = os.path.join(target_folder, filename)
    file_storage_object.save(save_path)
    return save_path
