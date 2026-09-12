from app.workshop_v16 import analyze_pair, workshop


def test_unknown_taxon_is_explained_not_fake_translated():
    data = workshop('krogia', 'lichens', 8, 'neutral')
    assert 'not a standard English dictionary word' in data['root']['en']
    assert 'nie ma prostego tłumaczenia' in data['root']['pl']


def test_workshop_has_ranked_best_and_brand_extensions():
    data = workshop('lark', 'birds', 8, 'creative')
    assert data['best']
    ext = {x['word']: x for x in data['extensions']}
    assert 'the' in ext
    assert 'one' in ext
    assert 'studio' in ext
    assert ext['the']['domain'] == 'thelark.com'
    assert ext['studio']['domain'] == 'larkstudio.com'


def test_brand_extension_keeps_brand_form_semantics():
    result = analyze_pair('lark', 'the', 'before', 'birds', 'creative')
    assert result['ok'] is True
    assert result['domain'] == 'thelark.com'
    assert result['semantic_class'] == 'brand-form'
    assert 'format marki' in result['semantic_alert']


def test_abstract_pair_gets_explicit_warning():
    result = analyze_pair('krogia', 'clear', 'before', 'lichens', 'neutral')
    assert result['ok'] is True
    assert result['semantic_class'] in {'abstract', 'brandable'}
    if result['semantic_class'] == 'abstract':
        assert 'Abstrakcyjne' in result['semantic_alert']
