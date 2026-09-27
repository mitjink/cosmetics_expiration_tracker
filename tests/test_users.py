from models import User


def test_user_creation():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"


def test_user_to_dict_and_back():
    user = User(1, "Иван Петров", "ivan@example.com")
    data = user.to_dict()
    restored = User.from_dict(data)
    assert restored.id == user.id
    assert restored.name == user.name
    assert restored.email == user.email


def test_user_str():
    user = User(1, "Иван Петров", "ivan@example.com")
    assert "Иван Петров" in str(user)
    assert "ivan@example.com" in str(user)
