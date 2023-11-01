from click import group, argument

from .__init__ import push as push_, add as add_, sync as sync_


@group()
def main():
    pass


@main.command()
@argument('local_path', type = str)
@argument('remote_path', type = str, required = False)
def push(local_path: str, remote_path: str):
    print(
        push_(local_path, remote_path)
    )


@main.command()
@argument('local_path', type = str)
@argument('remote_dir', type = str)
def add(local_path: str, remote_dir: str):
    print(
        add_(local_path, remote_dir)
    )


@main.command()
@argument('local_dir', type = str)
@argument('remote_dir', type = str)
def sync(local_dir: str, remote_dir: str):
    for result in sync_(local_dir, remote_dir):
        print(result)


if __name__ == '__main__':
    main()
