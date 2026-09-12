from pathlib import Path
from app.providers.language import LanguageProvider


def test_language_provider_transliterates_and_preserves_pinyin():
    provider = LanguageProvider(Path(__file__).parents[1] / "data" / "language_words.json")
    hits, warnings = provider.discover(["pl", "fr", "zh-pinyin"], 100)
    assert not warnings
    by_name = {h.name: h for h in hits}
    assert "swiatlo" in by_name
    assert by_name["swiatlo"].key == "światło"
    assert "eclat" in by_name
    assert "mingyue" in by_name
    assert by_name["mingyue"].key == "明月"
