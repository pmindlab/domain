from fastapi.testclient import TestClient

from app.main import app, service
from app.providers.brand import BrandResult
from app.providers.domain import DomainResult


async def fake_domains(domains):
    return {d.lower(): DomainResult(d, 'available', 'test') for d in domains}


async def fake_brand(name):
    return BrandResult(status='clear', notes=['test'])


def test_workshop_check_available_pair(monkeypatch):
    monkeypatch.setattr(service.domain, 'check_many', fake_domains)
    monkeypatch.setattr(service.brand, 'screen', fake_brand)
    client = TestClient(app)
    r = client.post('/api/workshop/check', json={
        'root': 'lark',
        'partner': 'dawn',
        'position': 'before',
        'niche': 'birds',
    })
    assert r.status_code == 200
    data = r.json()
    assert data['domain'] == 'dawnlark.com'
    assert data['domain_status'] == 'available'
    assert data['brand_status'] == 'clear'
