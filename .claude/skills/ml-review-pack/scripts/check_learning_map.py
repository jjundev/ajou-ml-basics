#!/usr/bin/env python3
"""Check the visible, first-topic learning map structure; teaching quality still needs review."""
from html.parser import HTMLParser
from pathlib import Path
import argparse

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
ROLES = {'goal','bridge','result','formula','pitfall'}
class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag=tag; self.attrs=dict(attrs); self.parent=parent; self.children=[]; self.text=''
    def walk(self):
        yield self
        for child in self.children: yield from child.walk()
    def content(self):
        return self.text + ''.join(c.content() for c in self.children)
class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.root=Node(); self.stack=[self.root]
    def handle_starttag(self, tag, attrs):
        n=Node(tag, attrs, self.stack[-1]); self.stack[-1].children.append(n)
        if tag not in VOID: self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag,attrs)
        if tag not in VOID: self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag: self.stack=self.stack[:i]; break
    def handle_data(self, data): self.stack[-1].text+=data

def check_source(source):
    p=Parser(); p.feed(source); nodes=list(p.root.walk())
    topics=[n for n in nodes if n.tag=='article' and 'topic' in n.attrs.get('class','').split()]
    maps=[n for n in nodes if 'data-learning-map' in n.attrs]
    if len(maps)!=1: return ['exactly one learning map required']
    m=maps[0]; ancestors=[]; n=m
    while n: ancestors.append(n); n=n.parent
    errors=[]
    if not topics or topics[0] not in ancestors: errors.append('learning map must be in the first topic')
    for n in ancestors:
        style=n.attrs.get('style','').lower().replace(' ','')
        if 'hidden' in n.attrs or n.attrs.get('aria-hidden')=='true' or n.tag=='details' and 'open' not in n.attrs or 'display:none' in style or 'visibility:hidden' in style:
            errors.append('learning map must be visible without opening a control'); break
    body=list(m.walk())
    for role in sorted(ROLES):
        matches=[n for n in body if n.attrs.get('data-map')==role]
        if len(matches)!=1 or not matches[0].content().strip(): errors.append('missing or empty role: '+role)
    if not any(n.tag in ('table','ul','ol') for n in body): errors.append('concept relationship table or list required')
    return errors

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('files',nargs='+');args=ap.parse_args();failed=0
    for f in args.files:
        errors=check_source(Path(f).read_text(encoding='utf-8'));failed+=len(errors)
        for e in errors: print(f+': '+e)
    print('OK' if not failed else f'FAIL ({failed})');return int(bool(failed))
if __name__=='__main__': raise SystemExit(main())
