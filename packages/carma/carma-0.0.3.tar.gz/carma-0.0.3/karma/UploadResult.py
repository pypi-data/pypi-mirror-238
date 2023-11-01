from enum import Enum
from datetime import datetime
from dataclasses import dataclass


TIME_FORMAT = '%d-%m-%Y %H:%M:%S'


class Status(Enum):
    SUCCESS = 200
    FILE_EXISTS = 'file-exists'
    FAILURE = None

    @classmethod
    def from_code(cls, code: int):
        if code == cls.SUCCESS.value:
            return cls.SUCCESS

        return cls.FAILURE


@dataclass
class UploadResult:
    username: str
    path: str
    time: datetime
    status: int

    message: str

    def __init__(self, status: int = None, username: str = None, path: str = None, time: str = None, message: str = None):
        self.username = username
        self.path = path
        self.time = time
        self.status = status
        self.message = message

    @classmethod
    def from_response(cls, response: dict):
        status = Status.from_code(response.get('status'))

        if status == Status.SUCCESS:
            return cls(
                username = response['email'],
                path = response['body'],
                time = datetime.fromtimestamp(response['time'] / 1_000),
                status = status
            )

        return response

    @classmethod
    def file_exists(cls, file: str):
        return cls(
            status = Status.FILE_EXISTS,
            message = file
        )

    def __repr__(self):
        if self.status == Status.SUCCESS:
            # return f'🟢 Uploaded successfully as {self.path} @ {self.time.strftime(TIME_FORMAT)} for {self.username}'
            return f'🟢 Uploaded successfully as {self.path}'
        if self.status == Status.FILE_EXISTS:
            return f'🟡 File {self.message} already exists. Can\'t upload'
        return f'{self}'
