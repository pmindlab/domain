from pathlib import Path
from app.scoring import PreferenceProfile, score_name, valid_candidate

PROFILE = PreferenceProfile.from_file(Path(__file__).parents[1] / "data" / "profile.json")

def test_length_and_single_word_filter():
    assert valid_candidate("dixeia")
    assert not valid_candidate("two words")
    assert not valid_candidate("abc")

def test_brandable_name_scores_well():
    score, parts, _ = score_name("dixeia", "butterflies", PROFILE)
    assert score >= 70
    assert parts["phone_test"] >= 10

def test_heavy_taxon_is_penalized():
    good, _, _ = score_name("acisoma", "dragonflies", PROFILE)
    heavy, _, _ = score_name("xiphorhynchus", "tropical birds", PROFILE)
    assert good > heavy
