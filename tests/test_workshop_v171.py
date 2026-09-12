from pathlib import Path

from app.workshop_v16 import analyze_pair, workshop

ROOT = Path(__file__).resolve().parents[1]


def _family(data, key):
    return next(f for f in data['families'] if f['key'] == key)


def test_software_workshop_has_a_large_curated_strong_pool():
    data = workshop('lark', '', 30, 'software')
    semantic = _family(data, 'semantic-context')['items']
    strong = [x for x in semantic if x['recommendation_tier'] in {'recommended', 'good'}]
    words = {x['word'] for x in strong}

    assert len(strong) >= 35
    assert {'agent', 'query', 'logic', 'sync', 'bridge', 'beacon', 'scope', 'stack'} <= words


def test_deep_pool_candidate_keeps_whole_name_meaning_contract():
    result = analyze_pair('lark', 'agent', 'after', '', 'software')

    assert result['ok'] is True
    assert result['domain'] == 'larkagent.com'
    assert result['recommendation_tier'] == 'recommended'
    assert 'software agent' in result['interpretation_en']
    assert 'agenta programowego' in result['interpretation_pl']
    assert result['semantic_class'] == 'brandable'


def test_v171_modal_patch_is_loaded_and_enforces_single_scroll_surface():
    app_js = (ROOT / 'app/static/app.js').read_text(encoding='utf-8')
    patch_js = (ROOT / 'app/static/workshop-v171.js').read_text(encoding='utf-8')
    patch_css = (ROOT / 'app/static/workshop-v171.css').read_text(encoding='utf-8')

    assert "/static/workshop-v171.js" in app_js
    assert 'MutationObserver' in patch_js
    assert "attributeFilter:['open']" in patch_js
    assert '.workshop-dialog' in patch_css and 'overflow:hidden' in patch_css
    assert 'html.workshop-modal-open body' in patch_css
    assert 'overflow-y:auto' in patch_css
