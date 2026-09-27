from datetime import date, timedelta
from typing import Optional


class Cosmetic:
    STATUS_NOT_OPENED = "не вскрыто"
    STATUS_EXPIRED_BEFORE = "просрочено до вскрытия"
    STATUS_OK = "в порядке"
    STATUS_SOON = "скоро истекает"
    STATUS_EXPIRED = "просрочено"

    def __init__(
        self,
        cosmetic_id: int,
        name: str,
        brand: str,
        expiry: str,
        months: int,
        opened: Optional[str] = None,
    ) -> None:
        self.id = cosmetic_id
        self.name = name
        self.brand = brand
        self.expiry = expiry
        self.months = months
        self.opened = opened

    def is_opened(self) -> bool:
        return self.opened is not None

    def is_expired_before_opening(self) -> bool:
        return date.fromisoformat(self.expiry) < date.today()

    def open(self) -> None:
        self.opened = date.today().isoformat()

    def get_deadline(self) -> Optional[date]:
        if self.opened is None:
            return None
        opened_date = date.fromisoformat(self.opened)
        return opened_date + timedelta(days=self.months * 30)

    def get_days_left(self) -> Optional[int]:
        deadline = self.get_deadline()
        if deadline is None:
            return None
        return (deadline - date.today()).days

    def get_status(self) -> str:
        if not self.is_opened():
            if self.is_expired_before_opening():
                return self.STATUS_EXPIRED_BEFORE
            return self.STATUS_NOT_OPENED

        days_left = self.get_days_left()
        if days_left is None:
            return self.STATUS_NOT_OPENED
        if days_left < 0:
            return f"{self.STATUS_EXPIRED} ({-days_left} дн. назад)"
        if days_left <= 14:
            return f"{self.STATUS_SOON} ({days_left} дн.)"
        return f"{self.STATUS_OK} ({days_left} дн.)"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "expiry": self.expiry,
            "months": self.months,
            "opened": self.opened,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Cosmetic":
        return cls(
            cosmetic_id=data["id"],
            name=data["name"],
            brand=data["brand"],
            expiry=data["expiry"],
            months=data["months"],
            opened=data.get("opened"),
        )

    def __str__(self) -> str:
        return f"{self.brand} {self.name} — {self.get_status()}"
