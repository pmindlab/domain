from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_workshop_from_result_has_back_navigation_and_scroll_restore():
    app_js = (ROOT / "app/static/app.js").read_text(encoding="utf-8")
    patch_js = (ROOT / "app/static/workshop-back-v173.js").read_text(encoding="utf-8")
    patch_css = (ROOT / "app/static/workshop-back-v173.css").read_text(encoding="utf-8")

    assert "/static/workshop-back-v173.js" in app_js
    assert ".workshop-open" in patch_js
    assert "← Wróć do wyników" in patch_js
    assert "scrollY:window.scrollY" in patch_js
    assert "window.scrollTo" in patch_js
    assert "dialog.close()" in patch_js
    assert "font-weight:400" in patch_css
