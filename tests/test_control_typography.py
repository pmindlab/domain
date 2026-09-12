from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_clickable_chips_and_ctas_use_regular_weight():
    css = (ROOT / "app/static/product-ui-v1-mianem.css").read_text(encoding="utf-8")

    regular_rule = next(
        rule
        for rule in css.split("}")
        if ".niche-chip.selected" in rule and "font-weight:400" in rule
    )

    assert ".niche-chip" in regular_rule
    assert ".language-chip" in regular_rule
    assert ".language-chip b" in regular_rule
    assert ".primary-small" in regular_rule
    assert ".cta" in regular_rule
