from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_selected_construction_can_switch_direction_without_reversing_fixed_grammar():
    app_js = (ROOT / 'app/static/app.js').read_text(encoding='utf-8')
    patch_js = (ROOT / 'app/static/workshop-v172.js').read_text(encoding='utf-8')
    patch_css = (ROOT / 'app/static/workshop-v172.css').read_text(encoding='utf-8')

    assert "/static/workshop-v172.js" in app_js
    assert "pairDirectionSwitch" in patch_js
    assert "data-pair-position=\"before\"" in patch_js
    assert "data-pair-position=\"after\"" in patch_js
    assert "window.MianemWorkshop.selectPair(selected.partner,position)" in patch_js

    # Fixed construction families retain their canonical grammar and do not get
    # an automatic reverse option such as `Lark By`.
    for label in (
        "Forma marki",
        "Relacja / przyimek",
        "Akcja / produkt",
        "Kontakt / komunikacja",
        "Przynależność",
        "Deskryptor po rdzeniu",
    ):
        assert label in patch_js
    assert "Ten typ konstrukcji ma ustalony naturalny szyk" in patch_js

    # The switch is part of the selected-construction panel and follows PMindLab
    # action tokens instead of inventing a local primary colour.
    assert ".pair-direction-switch" in patch_css
    assert "var(--pmind-action)" in patch_css
    assert "font-weight:400" in patch_css
