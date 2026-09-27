class User:

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
        )

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
