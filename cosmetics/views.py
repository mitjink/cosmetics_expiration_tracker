# flake8: noqa: F401

from django.http import HttpResponse

from homepage.views import page
from models.cosmetics import Cosmetic
from storage import load_cosmetics, load_records, load_users


def cosmetics(request):
    items = ""
    for cosmetic in load_cosmetics("data/cosmetics.json"):
        text = f"{cosmetic.brand} {cosmetic.name} — {cosmetic.get_status()}"
        items += (
            f'<li class="list-group-item">'
            f'<a href="/cosmetics/{cosmetic.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Средства</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Косметика — список", content))


def cosmetic_detail(request, cosmetic_id):
    cosmetics_list = load_cosmetics("data/cosmetics.json")
    cosmetic = next(
        (c for c in cosmetics_list if c.id == cosmetic_id),
        None,
    )
    if cosmetic is None:
        content = """
        <h1 class="text-danger">Средство не найдено</h1>
        <a href="/cosmetics/" class="btn btn-outline-secondary">
        ← к списку средств</a>
        """
        return HttpResponse(
            page("Средство не найдено", content),
            status=404,
        )

    status = cosmetic.get_status()
    badge = "bg-success"
    if Cosmetic.STATUS_EXPIRED in status or \
            Cosmetic.STATUS_EXPIRED_BEFORE in status:
        badge = "bg-danger"
    elif Cosmetic.STATUS_SOON in status:
        badge = "bg-warning"

    deadline = cosmetic.get_deadline()
    deadline_text = deadline.isoformat() if deadline else "—"

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{cosmetic.brand} {cosmetic.name}</h5>
        <p class="card-text"><strong>ID:</strong> {cosmetic.id}</p>
        <p class="card-text"><strong>Годен до вскрытия:</strong>
            {cosmetic.expiry}</p>
        <p class="card-text"><strong>Срок после вскрытия:</strong>
            {cosmetic.months} мес.</p>
        <p class="card-text"><strong>Дата вскрытия:</strong>
            {cosmetic.opened or "не вскрыто"}</p>
        <p class="card-text"><strong>Использовать до:</strong>
            {deadline_text}</p>
        <p class="card-text">Статус:
            <span class="badge {badge}">{status}</span>
        </p>
        <a href="/cosmetics/" class="btn btn-outline-secondary">
        ← к списку средств</a>
      </div>
    </div>
    """
    return HttpResponse(
        page(f"{cosmetic.brand} {cosmetic.name}", content),
    )
