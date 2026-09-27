from models.cosmetics import Cosmetic
from models.users import User


class UsageRecord:
    def __init__(
        self,
        record_id: int,
        cosmetic: Cosmetic,
        user: User,
        opened_date: str,
        is_cancelled: bool = False,
    ) -> None:
        self.id = record_id
        self.cosmetic = cosmetic
        self.user = user
        self.opened_date = opened_date
        self.is_cancelled = is_cancelled

    def cancel(self) -> None:
        self.is_cancelled = True

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cosmetic_id": self.cosmetic.id,
            "user_id": self.user.id,
            "opened_date": self.opened_date,
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
        cosmetics: list[Cosmetic],
        users: list[User],
    ) -> "UsageRecord | None":
        cosmetic = next(
            (c for c in cosmetics if c.id == data["cosmetic_id"]),
            None,
        )
        user = next(
            (u for u in users if u.id == data["user_id"]),
            None,
        )
        if cosmetic is None or user is None:
            return None
        return cls(
            record_id=data["id"],
            cosmetic=cosmetic,
            user=user,
            opened_date=data["opened_date"],
            is_cancelled=data.get("is_cancelled", False),
        )

    def __str__(self) -> str:
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"Запись №{self.id}: {self.cosmetic.brand} {self.cosmetic.name} "
            f"({self.user.name}), открыта {self.opened_date} — {status}"
        )
