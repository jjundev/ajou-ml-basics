"""Versioned review reuse; missing or changed evidence never inherits approval."""
from copy import deepcopy

POLICY_VERSION = 'problem-explain-2026-10-20-row-derivatives'

def carry_reviews(stored, fresh, references, reusable):
    result = deepcopy(fresh)
    result['review_policy_version'] = POLICY_VERSION
    result['references'] = references
    if reusable and stored.get('review_policy_version') == POLICY_VERSION:
        for key in ('content', 'independent'):
            if stored.get(key, {}).get('status') == 'pass':
                result[key] = deepcopy(stored[key])
    return result
