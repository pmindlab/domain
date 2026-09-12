from fastapi.testclient import TestClient
from app.main import app


def test_health():
    client = TestClient(app)
    r = client.get('/api/health')
    assert r.status_code == 200
    assert r.json()['ok'] is True
    assert r.json()['app'] == 'Mianem'
    assert r.json()['version'] == '1.4.1'
    assert r.json()['niche_count'] >= 60


def test_languages():
    client = TestClient(app)
    r = client.get('/api/languages')
    assert r.status_code == 200
    keys = {x['key'] for x in r.json()['languages']}
    assert {'en','pl','es','fr','la','zh-pinyin'} <= keys
