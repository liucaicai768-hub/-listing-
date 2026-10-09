#!/usr/bin/env python3
"""Mechanical checks for the supplied listing SOP; Python standard library only."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

FIELDS = ('item_name', 'item_highlight', 'product_description', 'generic_keyword')
FORBIDDEN = ('perfect gift', 'best gift', 'anniversary gift', 'great gift', 'baby shower gift')


def words(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


def validate(data):
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object')
    for field in FIELDS:
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f'{field} must be a nonempty string')
    bullets = data.get('bullet_points')
    if not isinstance(bullets, list) or not all(isinstance(b, str) and b.strip() for b in bullets):
        raise ValueError('bullet_points must be a list of nonempty strings')
    errors = []
    title, highlight, keywords = (data[k] for k in ('item_name', 'item_highlight', 'generic_keyword'))
    metrics = {'item_name_characters': len(title), 'item_highlight_characters': len(highlight),
               'generic_keyword_utf8_bytes': len(keywords.encode('utf-8')), 'bullet_count': len(bullets)}
    if len(title) > 75:
        errors.append('Item Name exceeds 75 characters')
    if len(title) >= 75:
        errors.append('Item Highlight requires Item Name shorter than 75 characters')
    if len(highlight) > 125:
        errors.append('Item Highlight exceeds 125 characters')
    if len(bullets) != 5:
        errors.append('Exactly five Bullet Points are required')
    normalized_bullets = [' '.join(b.lower().split()) for b in bullets]
    if len(set(normalized_bullets)) != len(bullets):
        errors.append('Identical Bullet Points found')
    for field, value in [(k, data[k]) for k in FIELDS] + [(f'bullet_points[{i+1}]', b) for i, b in enumerate(bullets)]:
        normalized = ' '.join(value.lower().split())
        for phrase in FORBIDDEN:
            if re.search(r'\b' + re.escape(phrase).replace(r'\ ', r'[\s\-]+') + r'\b', normalized):
                errors.append(f'{field}: forbidden phrase {phrase!r}')
        if value.isupper():
            errors.append(f'{field}: all-uppercase text')
    for field in ('item_name', 'item_highlight'):
        repeated = [w for w, n in Counter(words(data[field])).items() if n > 2]
        if repeated:
            errors.append(f'{field}: words occurring more than twice: {", ".join(repeated)}')
    if keywords != keywords.lower():
        errors.append('Generic Keyword must be lowercase')
    if metrics['generic_keyword_utf8_bytes'] > 250:
        errors.append('Generic Keyword exceeds 250 UTF-8 bytes')
    kw = words(keywords)
    duplicates = [w for w, n in Counter(kw).items() if n > 1]
    if duplicates:
        errors.append('Repeated search words: ' + ', '.join(duplicates))
    overlap = sorted(set(kw) & set(words(title)))
    if overlap:
        errors.append('Search words repeated from title: ' + ', '.join(overlap))
    if re.search(r'\bb0[a-z0-9]{8}\b', keywords, re.I):
        errors.append('Possible ASIN in Generic Keyword; verify and remove')
    return {'passed': not errors, 'metrics': metrics, 'errors': errors,
            'manual_review': ['Product facts', 'Semantic repetition', 'Competitor brands and ASINs',
                              'Mobile display', 'Preposition casing and abbreviations', 'Current platform policy',
                              'Other subjective gift phrases', 'Highlight duplicates title information']}


def main():
    if len(sys.argv) != 2:
        print('Usage: validate_listing.py listing.json', file=sys.stderr)
        return 2
    try:
        result = validate(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        print(f'Input error: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
