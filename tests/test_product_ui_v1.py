from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_brand_tokens_are_local():
    css = (ROOT / 'app/static/pmindlab-tokens.css').read_text(encoding='utf-8')
    assert '--pmind-brand-blue: #3B72B5' in css
    assert '--pmind-brand-navy: #16325C' in css
    assert '--pmind-brand-blue-on-dark: #6A9DD8' in css
    assert '--pmind-brand-lab-on-dark: #C3D9F0' in css
    assert '--pmind-bg: #101216' in css
    assert '--pmind-surface: #171A1F' in css
    assert '--pmind-surface-2: #1D2127' in css


def test_mianem_uses_action_colour_separately_from_wordmark_colour():
    css = (ROOT / 'app/static/product-ui-v1-mianem.css').read_text(encoding='utf-8')
    assert '--pmind:var(--pmind-brand-blue)' in css
    assert '--lab:var(--pmind-action)' in css
    assert 'background:var(--pmind-action)' in css


def test_dark_logo_is_exact_colour_adaptation_of_light_geometry():
    js = (ROOT / 'app/static/product-ui-v1.js').read_text(encoding='utf-8')
    assert "replaceAll('rgb(59,114,181)','#6A9DD8')" in js
    assert "replaceAll('rgb(22,50,92)','#C3D9F0')" in js
    assert 'MutationObserver' in js
    assert 'PMINDLAB_PRODUCT_UI_VERSION=1' in js
