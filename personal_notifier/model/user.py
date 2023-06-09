class User:
    def __init__(
        self,
        id: int,
        name: str,
        nickname: str
    ) -> None:
        self.id = id
        self.name = name
        self.nickname = nickname

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'nickname': self.nickname
        }

    @staticmethod
    def from_json(json: dict):
        return User(
            id=json['id'],
            name=json['name'],
            nickname=json['nickname'],
        )
