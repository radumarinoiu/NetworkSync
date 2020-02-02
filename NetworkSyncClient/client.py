import os
import requests

from NetworkSyncServer.utils import file_sha256sum


if __name__ == '__main__':
    for root, dirs, files in os.walk("/home/radu/Pictures/"):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            response = requests.post("http://localhost:5000/file_changed_event", json={
                "path": file_path,
                "sha256sum": file_sha256sum(file_path)
            })
            if response.status_code == 201:
                upload_token = response.json().get("upload token", None)
                if upload_token:
                    with open(file_path, "rb") as fd:
                        response = requests.post(
                            "http://localhost:5000/upload_file/{}".format(upload_token),
                            data=fd)
                        if response.status_code != 201:
                            print("Failed to upload file: {}".format(file_path))
