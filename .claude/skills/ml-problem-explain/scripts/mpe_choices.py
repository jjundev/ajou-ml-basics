"""Read explicit interaction data; never infer answer keys from explanations."""
import json
from dataclasses import replace
from mpe_types import ChoiceModel
from mpe_shared import Node, parse

def choice_models(html_text, statements):
    scripts = list(parse(html_text).find_all(lambda n: n.tag == 'script' and n.attrs.get('id') == 'review-interaction-model' and n.attrs.get('type') == 'application/json'))
    if len(scripts) != 1:
        return {}
    try:
        cards = json.loads(scripts[0].text())['cards']
    except (ValueError, KeyError, TypeError):
        return {}
    if not isinstance(cards, dict):
        return {}
    result = {}
    for id_, statement in statements.items():
        card = cards.get(id_)
        if not isinstance(card, dict):
            continue
        lists = list(parse(statement).find_all(lambda n: n.tag in ('ul','ol') and 'choices' in n.classes))
        options = card.get('options')
        if len(lists) != 1 or not isinstance(options, list) or not options or not all(isinstance(o, dict) for o in options):
            continue
        count = sum(isinstance(c,Node) and c.tag == 'li' for c in lists[0].children)
        ids, indexes = [o.get('id') for o in options], [o.get('index') for o in options]
        if (len(options) != count or not all(isinstance(i,str) and i.strip() for i in ids)
            or len(set(ids)) != len(ids) or card.get('answer') not in ids
            or card.get('mode') not in ('single','ambiguous')
            or not all(type(i) is int for i in indexes) or sorted(indexes) != list(range(count))):
            continue
        result[id_] = ChoiceModel(card['answer'],card['mode'],tuple(o['id'] for o in sorted(options,key=lambda o:o['index'])))
    return result

def with_choices(path, problems):
    models = choice_models(path.read_text(encoding='utf-8'), {p.id:p.conditions_html + p.ask_html for p in problems})
    return tuple(replace(p,choice=models.get(p.id)) for p in problems)
