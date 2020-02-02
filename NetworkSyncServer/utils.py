import hashlib


def file_sha256sum(file_path):
    file_hash = hashlib.sha256()
    with open(file_path, "rb") as fd:
        data_buffer = fd.read(8192)
        while data_buffer:
            file_hash.update(data_buffer)
            data_buffer = fd.read(8192)
    return file_hash.hexdigest()