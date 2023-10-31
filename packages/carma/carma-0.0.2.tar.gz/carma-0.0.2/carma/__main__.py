import os
from os import environ as env
from click import group, argument

from .cloud_mail_api import CloudMail


@group()
def main():
    pass


USERNAME = env['CARMA_USERNAME']
PASSWORD = env['CARMA_PASSWORD']

cm = CloudMail(USERNAME, PASSWORD)
cm.auth()


def _push(local_path: str, remote_path: str):
    response = cm.api.file(remote_path)

    if response.get('status') == 404:
        response = cm.api.file.add(local_path, remote_path)
        print(response)
    else:
        print(f'File "{remote_path}" already exists. Choose another name')


@main.command()
@argument('local_path', type = str)
@argument('remote_path', type = str, required = False)
def push(local_path: str, remote_path: str):
    _push(local_path, os.path.join(os.sep, os.path.basename(local_path)) if remote_path is None else remote_path)


@main.command()
@argument('local_path', type = str)
@argument('remote_dir', type = str)
def add(local_path: str, remote_dir: str):
    remote_path = os.path.join(remote_dir, os.path.basename(local_path))

    response = cm.api.file(remote_path)

    if response.get('status') == 404:
        response = cm.api.file.add(local_path, remote_path)
        print(response)
    else:
        print(f'File "{remote_path}" already exists. Choose another folder')


@main.command()
@argument('local_dir', type = str)
@argument('remote_dir', type = str)
def sync(local_dir: str, remote_dir: str):
    remote_dir = os.path.join(remote_dir, os.path.basename(local_dir))

    for file in os.listdir(local_dir):
        local_file = os.path.join(local_dir, file)

        if os.path.isfile(local_file):
            remote_file = os.path.join(remote_dir, file)

            _push(local_file, remote_file)


if __name__ == '__main__':
    main()
