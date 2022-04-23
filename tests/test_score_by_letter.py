from wordinfo.scoring import get_score_by_letter


def test_does_get_score_by_letter():
    letter_scores = get_score_by_letter(['test', 'word', 'top'])

    assert letter_scores['t'] == 3
    assert letter_scores['o'] == 2
    assert letter_scores['e'] == 1


