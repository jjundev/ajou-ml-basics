"""문제설명 템플릿의 테마 스크롤바(토큰 3블록 + 규칙)를 지킨다."""
import re
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / 'assets' / 'note-template.html'
LIGHT = '--scroll: #c9d0db; --scroll-hover: #9aa3b2;'
DARK = '--scroll: #3f414b; --scroll-hover: #5b5e6a;'


def test_tokens_in_every_theme_block():
    text = TEMPLATE.read_text(encoding='utf-8')
    assert len(re.findall(r'--scroll: #[0-9a-f]{6}; --scroll-hover: #[0-9a-f]{6};', text)) == 3
    assert text.count(LIGHT) == 1
    assert text.count(DARK) == 2


def test_rules_cover_both_scroll_containers():
    text = TEMPLATE.read_text(encoding='utf-8')
    for needle in (
        '.content::-webkit-scrollbar, .panel-inner::-webkit-scrollbar { width: 8px; }',
        '.content::-webkit-scrollbar-thumb, .panel-inner::-webkit-scrollbar-thumb { background: var(--scroll);',
        '.content::-webkit-scrollbar-thumb:hover, .panel-inner::-webkit-scrollbar-thumb:hover { background: var(--scroll-hover); }',
        'scrollbar-color: var(--scroll) transparent;',
    ):
        assert needle in text


def test_panel_width_variable_kept():
    assert '--scrollbar: 16px;' in TEMPLATE.read_text(encoding='utf-8')
