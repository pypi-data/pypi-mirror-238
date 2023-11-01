import os
from os import environ as env

from .cloud_mail_api import CloudMail
from .UploadResult import UploadResult


USERNAME = env['KARMA_USERNAME']
PASSWORD = env['KARMA_PASSWORD']

cm = CloudMail(USERNAME, PASSWORD)
cm.auth()


def push(local_path: str, remote_path: str = None):
    if remote_path is None:
        remote_path = os.path.join(os.sep, os.path.basename(local_path))

    response = cm.api.file(remote_path)

    if response.get('status') == 404:
        response = cm.api.file.add(local_path, remote_path)
        return UploadResult.from_response(response)

    # raise ValueError(f'File "{remote_path}" already exists. Choose another name')
    raise ValueError(UploadResult.file_exists(remote_path))


def add(local_path: str, remote_dir: str):
    remote_path = os.path.join(remote_dir, os.path.basename(local_path))

    response = cm.api.file(remote_path)

    if response.get('status') == 404:
        response = cm.api.file.add(local_path, remote_path)
        return UploadResult.from_response(response)

    # raise ValueError(f'File "{remote_path}" already exists. Choose another folder')
    raise ValueError(UploadResult.file_exists(remote_path))


def sync(local_dir: str, remote_dir: str):
    remote_dir = os.path.join(remote_dir, os.path.basename(local_dir))

    for file in os.listdir(local_dir):
        local_file = os.path.join(local_dir, file)

        if os.path.isfile(local_file):
            remote_file = os.path.join(remote_dir, file)

            try:
                yield push(local_file, remote_file)
            except ValueError as e:
                yield e
