from typing import Protocol, Optional
from user import User
from data_parse import DataRepository, DataRepositoryProtocol


class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):
    def get_by_login(self, login: str) -> Optional[User]:
        ...


class UserRepository(DataRepository[User], UserRepositoryProtocol):
    def __init__(self, file_path: str = 'data/users.json') -> None:
        super().__init__(file_path, User)

    def get_by_login(self, login: str) -> Optional[User]:
        for item in self._load_data():
            if item['login'] == login:
                return User(**item)
        return None
