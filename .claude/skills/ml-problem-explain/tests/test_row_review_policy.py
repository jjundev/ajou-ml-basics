from mpe_review_policy import carry_reviews

def test_approval_before_row_convention_review_is_not_reused():
    stored = {'review_policy_version': 'problem-explain-2026-10-15',
              'content': {'status': 'pass'}, 'independent': {'status': 'pass'}}
    fresh = {'content': {'status': 'not_run'}, 'independent': {'status': 'not_run'}}
    result = carry_reviews(stored, fresh, [], True)
    assert result['content']['status'] == 'not_run'
    assert result['independent']['status'] == 'not_run'
