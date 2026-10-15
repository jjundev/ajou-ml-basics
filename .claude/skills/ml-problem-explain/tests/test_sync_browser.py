"""Synthetic stage acceptance; no calls to publish or real course output paths."""
import functools
import http.server
import threading
from dataclasses import replace
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from test_sync import synthetic
from mpe_render import build_explanation,check_artifacts


def make_stage(root):
    repo,pack,fragments=synthetic(root)
    pack.path.parent.mkdir(parents=True,exist_ok=True)
    if pack.path.suffix=='.html':
        pack.path.write_text('<html><body id="p1"><div id="p2"></div></body></html>',encoding='utf-8')
    p=pack.problems[0]
    conditions=('<p>$A=1$</p><pre><code>if (x &lt; 2) { printf("value", x); }</code></pre>'
                '<svg viewBox="0 0 100 40" role="img" aria-label="합성 그림"><path d="M1 1L90 30" stroke="currentColor"/></svg>')
    from mpe_types import ChoiceModel
    conditions += '<ul class="choices"><li>A</li><li>B</li></ul>'
    p=replace(p,choice=ChoiceModel('B','single',('A','B')))
    p=replace(p,conditions_html=conditions)
    p2=replace(p,id='p2',number=2,title='두 번째 문항',original_html='')
    pack=replace(pack,problems=(p,p2))
    fragments={q.id:fragments['p1'] for q in pack.problems}
    a=build_explanation(pack,fragments,root/'stage',repo)
    assert check_artifacts(pack,a)==[]
    return a


@pytest.fixture(scope='module')
def stage_url(tmp_path_factory):
    root=tmp_path_factory.mktemp('explain-browser')
    a=make_stage(root)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args): pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    yield f'http://127.0.0.1:{server.server_port}/stage/{a.html.name}#p1'
    server.shutdown();thread.join();server.server_close()


@pytest.fixture(scope='module')
def browser():
    with sync_playwright() as pw:
        b=pw.chromium.launch()
        yield b
        b.close()


@pytest.mark.parametrize('width,height',[(1024,900),(1280,900),(375,812)])
@pytest.mark.parametrize('theme',['light','dark'])
def test_panel_tabs_choices_zoom_print_and_resources(browser,stage_url,width,height,theme):
    context=browser.new_context(viewport={'width':width,'height':height},color_scheme=theme)
    page=context.new_page();errors=[];failed=[];external=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    page.on('requestfailed',lambda r:failed.append(r.url))
    page.on('response',lambda r:failed.append(r.url) if r.status>=400 else None)
    page.on('request',lambda r:external.append(r.url) if not r.url.startswith(stage_url.split('/stage/')[0]) else None)
    try:
        page.goto(stage_url,wait_until='networkidle')
        if width>=1024:
            assert page.locator('#panel-left').is_visible()
            assert page.locator('#panel-prob').is_visible()
            page.locator('#tab-original').click()
            assert page.locator('#tabpanel-original [data-original-problem="p1"]').is_visible()
            page.locator('#pager-next').click()
            assert page.locator('#tab-original').is_hidden()
            page.locator('#pager-prev').click()
            page.locator('#tab-problem').click()
        else:
            assert page.locator('#panel-prob').is_hidden()
            assert page.locator('#p1 .problem-toggle').is_visible()
            page.locator('#p1 .problem-toggle').click()
        pane=page.locator('[data-problem-for="p1"]')
        assert pane.is_visible()
        assert 'printf("value", x)' in pane.locator('pre code').inner_text()
        pane.locator('.review-choice[data-choice-id="A"]').click()
        assert pane.locator('[data-choice-id="A"]').get_attribute('data-result')=='selected'
        pane.locator('.review-reset').click()
        pane.locator('.review-choice[data-choice-id="B"]').click()
        assert pane.locator('[data-choice-id="B"]').get_attribute('data-result')=='correct'
        pane.locator('svg.zoomable').click()
        assert page.locator('dialog.figure-sheet[open]').is_visible()
        page.locator('.figure-sheet .sheet-close').click()
        page.evaluate('window.dispatchEvent(new Event("beforeprint"))')
        assert page.locator('#p1 > [data-problem-for="p1"]').is_visible()
        assert page.locator('#p2 > [data-problem-for="p2"]').count()==1
        page.evaluate('window.dispatchEvent(new Event("afterprint"))')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        assert page.locator('.katex-error').count()==0
        assert not errors and not failed and not external,(errors,failed,external)
    finally:
        context.close()


def test_breakpoint_and_saved_closed_toc(browser,stage_url):
    context=browser.new_context(viewport={'width':1023,'height':900})
    page=context.new_page()
    try:
        page.goto(stage_url,wait_until='networkidle')
        assert page.locator('#panel-prob').is_hidden()
        page.set_viewport_size({'width':1024,'height':900})
        page.wait_for_timeout(150)
        assert page.locator('#panel-left').is_visible()
        assert page.locator('#panel-prob').is_visible()
        page.locator('#toggle-left').click()
        page.reload(wait_until='networkidle')
        assert page.locator('#panel-left').is_hidden()
        assert page.locator('#panel-prob').is_visible()
    finally:
        context.close()


def test_dock_float_drag_resize_and_restore(browser,stage_url):
    context=browser.new_context(viewport={'width':1280,'height':900})
    page=context.new_page()
    try:
        page.goto(stage_url,wait_until='networkidle')
        page.locator('.prob-dock [data-dock="right"]').click()
        page.locator('#toggle-right').click()
        assert page.locator('#panel-prob').is_visible() and page.locator('#panel-right').is_visible()
        page.locator('.prob-dock [data-dock="float"]').click()
        panel=page.locator('#panel-prob');before=panel.bounding_box()
        mover=page.locator('.float-move').bounding_box()
        x,y=mover['x']+mover['width']/2,mover['y']+mover['height']/2
        page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+40,y+30,steps=6);page.mouse.up()
        after=panel.bounding_box()
        assert abs(after['x']-before['x'])>10 or abs(after['y']-before['y'])>10
        handle=page.locator('.float-resize').bounding_box()
        x,y=handle['x']+6,handle['y']+6
        page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+30,y-30,steps=6);page.mouse.up()
        assert panel.bounding_box()['height']!=after['height']
        page.reload(wait_until='networkidle')
        assert page.locator('.layout').get_attribute('data-prob-dock')=='float'
        page.locator('.prob-dock [data-dock="left"]').click()
        assert page.locator('.layout').get_attribute('data-prob-dock')=='left'
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    finally:
        context.close()
