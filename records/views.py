from django.http import HttpResponse

from homepage.views import page
from storage import load_cosmetics, load_records, load_users


def _load_all():
    cosmetics = load_cosmetics("data/cosmetics.json")
    users = load_users("data/users.json")
    records = load_records(cosmetics, users, "data/records.json")
    return records


def records(request):
    items = ""
    for record in _load_all():
        text = (
            f"{record.cosmetic.brand} {record.cosmetic.name} "
            f"({record.user.name}), открыта {record.opened_date}"
        )
        status = "отменена" if record.is_cancelled else "активна"
        badge = "bg-secondary" if record.is_cancelled else "bg-success"
        items += (
            f'<li class="list-group-item">'
            f'<a href="/records/{record.id}/">{text}</a> '
            f'<span class="badge {badge}">{status}</span>'
            f'</li>'
        )
    content = f"""
    <h1>Записи об использовании</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Записи об использовании", content))


def record_detail(request, record_id):
    record = next(
        (r for r in _load_all() if r.id == record_id),
        None,
    )
    if record is None:
        content = """
        <h1 class="text-danger">Запись не найдена</h1>
        <a href="/records/" class="btn btn-outline-secondary">
        ← к списку записей</a>
        """
        return HttpResponse(
            page("Запись не найдена", content),
            status=404,
        )

    status = "отменена" if record.is_cancelled else "активна"
    badge = "bg-secondary" if record.is_cancelled else "bg-success"
    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Запись №{record.id}</h5>
        <p class="card-text">Средство:
            {record.cosmetic.brand} {record.cosmetic.name}</p>
        <p class="card-text">Пользователь: {record.user.name}</p>
        <p class="card-text">Дата вскрытия: {record.opened_date}</p>
        <p class="card-text">Статус:
            <span class="badge {badge}">{status}</span>
        </p>
        <a href="/records/" class="btn btn-outline-secondary">
        ← к списку записей</a>
      </div>
    </div>
    """
    return HttpResponse(page(f"Запись №{record.id}", content))
