from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_search_setting_labels_keep_visible_line_box():
    css = (ROOT / 'app/static/setting-label-v166.css').read_text(encoding='utf-8')
    app_js = (ROOT / 'app/static/app.js').read_text(encoding='utf-8')
    assert '.setting-row small,.setting-label' in css
    assert 'line-height:1.4' in css
    assert 'min-height:1.4em' in css
    assert 'overflow:visible' in css
    assert "'/static/setting-label-v166.css'" in app_js
