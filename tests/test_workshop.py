from app.workshop import analyze_pair, workshop


def test_lark_workshop_has_meanings_and_curated_sides():
    data = workshop('lark', 'birds', 8)
    assert data['root']['en'].startswith('a small songbird')
    assert 'skowronek' in data['root']['pl']
    assert [x['word'] for x in data['before'][:3]] == ['dawn', 'silver', 'north']
    assert [x['word'] for x in data['after'][:3]] == ['wing', 'song', 'light']


def test_pair_analysis_builds_domain_and_scores_semantics():
    result = analyze_pair('lark', 'dawn', 'before', 'birds')
    assert result['ok'] is True
    assert result['domain'] == 'dawnlark.com'
    assert result['score'] >= 70
    assert result['risk'] == 'low'


def test_negative_pair_is_blocked_before_domain_check():
    result = analyze_pair('lark', 'toxic', 'before', 'birds')
    assert result['ok'] is False
    assert result['risk'] == 'blocked'
    assert result['score'] == 0
