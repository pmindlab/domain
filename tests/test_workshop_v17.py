from app.workshop_v16 import analyze_pair, workshop


def _family(data, key):
    return next(f for f in data['families'] if f['key'] == key)


def test_creative_relation_family_recommends_by_lark_with_meaning():
    data = workshop('lark', '', 24, 'creative')
    relation = _family(data, 'relation')
    by_lark = next(x for x in relation['items'] if x['word'] == 'by')
    for_lark = [x for x in relation['items'] if x['word'] == 'for']

    assert by_lark['recommendation_tier'] == 'recommended'
    assert by_lark['score'] >= 90
    assert 'created by' in by_lark['interpretation_en']
    assert 'autorstwa' in by_lark['interpretation_pl']
    assert not for_lark  # not a strong/valid creative relation in this context


def test_software_context_has_deeper_semantic_and_action_families():
    data = workshop('lark', '', 30, 'software')
    semantic = _family(data, 'semantic-context')
    action = _family(data, 'action')

    semantic_words = {x['word'] for x in semantic['items']}
    action_words = {x['word'] for x in action['items']}
    assert {'signal', 'pulse', 'flow', 'core', 'loop'} <= semantic_words
    assert {'get', 'use', 'try', 'ask'} <= action_words
    assert data['shortlist_minimum'] == 6
    assert data['shortlist_target'] == 8


def test_recommendation_is_independent_from_domain_availability():
    result = analyze_pair('lark', 'with', 'before', '', 'software')
    assert result['recommendation_tier'] == 'recommended'
    assert result['family'] == 'relation'
    assert 'through or using' in result['interpretation_en']
    assert 'przy użyciu' in result['interpretation_pl']
    assert 'domain_status' not in result


def test_every_curated_family_candidate_has_whole_name_en_pl_meaning():
    data = workshop('lark', '', 24, 'product')
    for family in data['families']:
        for item in family['items']:
            assert item['interpretation_en'].strip()
            assert item['interpretation_pl'].strip()
            assert item['recommendation_tier'] in {'recommended', 'good', 'experimental'}
            assert item['phrase'].strip()
            assert item['domain'].endswith('.com')


def test_for_lark_service_is_not_promoted_above_stronger_relation():
    data = workshop('lark', '', 24, 'service')
    relation = _family(data, 'relation')['items']
    with_lark = next(x for x in relation if x['word'] == 'with')
    for_lark = next(x for x in relation if x['word'] == 'for')
    assert with_lark['recommendation_tier'] == 'recommended'
    assert with_lark['score'] > for_lark['score']
