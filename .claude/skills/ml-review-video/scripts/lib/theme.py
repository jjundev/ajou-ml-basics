"""Snapshot the actual review-pack HTML; never maintain a second palette."""
from pathlib import Path
import hashlib, json, re, shutil
from html.parser import HTMLParser
from .cache import atomic_json

ASSETS=Path(__file__).resolve().parents[2]/'assets'

class Styles(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False); self.active=False; self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag=='style': self.active=True
    def handle_endtag(self,tag):
        if tag=='style': self.active=False
    def handle_data(self,data):
        if self.active: self.parts.append(data)

def _hash(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def snapshot_theme(pack,run):
    run=Path(run); record=run/'source/theme.json'
    if record.exists():
        theme=json.loads(record.read_text(encoding='utf-8'))
        for relative,expected in theme['hashes'].items():
            p=run/relative
            if not p.is_file() or _hash(p)!=expected: raise ValueError('theme snapshot corrupt: '+relative)
        return theme
    dest=run/'source/templates'; dest.mkdir(parents=True,exist_ok=True)
    theme={'templates':{},'hashes':{},'tokens':{}}
    for kind,name in (('note','note-template.html'),('review','review-template.html')):
        src=Path(pack)/'assets'/name
        raw=src.read_bytes(); text=raw.decode('utf-8-sig')
        if ':root[data-theme="dark"]' not in text or '.topic' not in text:
            raise ValueError('incompatible review-pack template: '+name)
        saved=dest/name; saved.write_bytes(raw)
        parser=Styles(); parser.feed(text)
        css='\n'.join(parser.parts)
        css_path=run/'source'/('template.css' if kind=='note' else 'review-template.css')
        css_path.write_text(css,encoding='utf-8')
        match=re.search(r':root\[data-theme="dark"\]\s*\{([^}]+)\}',css)
        theme['tokens'][kind]=dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+)',match[1]))
        theme['templates'][kind]={'path':saved.relative_to(run).as_posix(),'sha256':_hash(saved),
                                  'css_path':css_path.relative_to(run).as_posix()}
        for p in (saved,css_path): theme['hashes'][p.relative_to(run).as_posix()]=_hash(p)
    layout=run/'source/video-layout.css'
    shutil.copyfile(ASSETS/'video-layout.css',layout)
    theme['hashes'][layout.relative_to(run).as_posix()]=_hash(layout)
    atomic_json(record,theme)
    return theme

def scene_shell(fragment,kind,theme):
    if kind not in ('note','review'): raise ValueError('unknown template kind')
    css=theme['templates'][kind]['css_path']
    return ('<!doctype html><html lang="ko" data-theme="dark"><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="'+css+'">'
            '<link rel="stylesheet" href="source/video-layout.css">'
            '<link rel="stylesheet" href="assets/fonts/fonts.css">'
            '<script src="assets/vendor/gsap.min.js"></script></head><body>'
            +fragment+'</body></html>')
