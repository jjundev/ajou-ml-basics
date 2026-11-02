"""Render text-node formulas once so standalone and nested scenes agree."""
import html
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

_PATTERN=re.compile(r'\$\$(.+?)\$\$|\$([^$\n]+?)\$',re.S)


def require_katex(vendor):
    vendor=Path(vendor)
    for name in ('katex.min.js','katex.min.css','auto-render.min.js'):
        if not (vendor/name).is_file(): raise ValueError('incomplete local KaTeX assets: '+name)
    css=(vendor/'katex.min.css').read_text(encoding='utf-8')
    for relative in re.findall(r'url\([\"\']?([^\)\"\']+)',css):
        path=(vendor/relative).resolve()
        if not path.is_relative_to(vendor.resolve()) or not path.is_file():
            raise ValueError('missing local KaTeX font')


class MathText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts=[]; self.formulas=[]; self.text=[]
    def flush_text(self):
        data=html.unescape(''.join(self.text));self.text=[];last=0
        for match in _PATTERN.finditer(data):
            self.parts.append(html.escape(data[last:match.start()],quote=False))
            self.parts.append(len(self.formulas))
            self.formulas.append({'tex':match.group(1) or match.group(2),'display':match.group(1) is not None})
            last=match.end()
        self.parts.append(html.escape(data[last:],quote=False))
    def handle_starttag(self,tag,attrs):
        self.flush_text();self.parts.append(self.get_starttag_text())
    def handle_startendtag(self,tag,attrs):
        self.flush_text();self.parts.append(self.get_starttag_text())
    def handle_endtag(self,tag):
        self.flush_text();self.parts.append('</'+tag+'>')
    def handle_comment(self,data):
        self.flush_text();self.parts.append('<!--'+data+'-->')
    def handle_data(self,data):self.text.append(data)
    def handle_entityref(self,name):self.text.append('&'+name+';')
    def handle_charref(self,name):self.text.append('&#'+name+';')


def render_math_fragment(fragment, vendor):
    parser=MathText();parser.feed(fragment);parser.close();parser.flush_text()
    if not parser.formulas:return fragment
    require_katex(vendor)
    js="const fs=require('fs'),k=require(process.argv[1]);const a=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(a.map(x=>k.renderToString(x.tex,{displayMode:x.display,throwOnError:true,trust:false,strict:'error'}))));"
    try:
        result=subprocess.run(['node','-e',js,str((Path(vendor)/'katex.min.js').resolve())],
            input=json.dumps(parser.formulas),capture_output=True,text=True,timeout=30)
        if result.returncode:raise ValueError('formula rendering failed; check original TeX')
        formulas=json.loads(result.stdout)
    except (OSError,subprocess.TimeoutExpired,json.JSONDecodeError):
        raise ValueError('local KaTeX renderer unavailable') from None
    return ''.join(formulas[p] if type(p) is int else p for p in parser.parts)


def katex_css(vendor):
    require_katex(vendor)
    return (Path(vendor)/'katex.min.css').read_text(encoding='utf-8').replace('url(fonts/','url(assets/vendor/katex/fonts/')
