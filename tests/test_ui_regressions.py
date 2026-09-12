from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_areas_dialog_layout_contract():
    css = (ROOT / 'app/static/ui-regression-v161.css').read_text(encoding='utf-8')
    assert 'grid-auto-rows:max-content' in css
    assert 'align-content:start' in css
    assert 'min-height:0' in css
    assert '100dvh' in css


def test_workshop_direction_choice_contract():
    js = (ROOT / 'app/static/workshop-direction-v161.js').read_text(encoding='utf-8')
    assert 'data-workshop-direction' in js
    assert 'before' in js
    assert 'after' in js
    assert 'bothDirectionsVisible' in js
    assert 'MianemWorkshop.selectPair' in js


def test_product_ui_v1_authority_is_recorded():
    agents = (ROOT / 'AGENTS.md').read_text(encoding='utf-8')
    assert 'PMINDLAB_PRODUCT_UI_V1.md' in agents
    assert 'RESPONSIVE CONTRACT' in agents


def test_workshop_defaults_to_available_domains_only():
    js = (ROOT / 'app/static/workshop-v16.js').read_text(encoding='utf-8')
    assert "==='available'" in js
    assert 'showTakenBest:false' in js
    assert 'showTakenExtensions:false' in js
    assert 'Pokaż zajęte' in js
    assert 'najpierw sens, potem wolne .com' in js
    assert "i+=20" in js
