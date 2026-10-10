import tempfile,unittest,json
from pathlib import Path
from _util import ROOT,minimal_manifest
from lib.theme import snapshot_theme
from lib.timing import build_timeline
from lib.composition import assemble

class CompositionTest(unittest.TestCase):
    def test_composition_and_invalid_target(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d); m=minimal_manifest()
            theme=snapshot_theme(ROOT/'.agents/skills/ml-review-pack',run)
            p=run/'source/scene-fragments'; p.mkdir()
            (p/'scene-atp.html').write_text('<section class="topic"><h3 id="scene-atp-count">32 ATP</h3></section>',encoding='utf-8')
            motions=[{'target':'#scene-atp-count','segment_id':'seg-atp','kind':'count','from':{'textContent':0},'to':{'textContent':32},'duration_s':1}]
            (p/'scene-atp.motion.json').write_text(json.dumps(motions))
            t=build_timeline(m,[{'id':'seg-atp','samples':24000,'rate':24000,'path':'assets/voice/test.wav'}])
            parts=assemble(m,t,theme,run)
            page=(run/parts[0]['entry']).read_text(encoding='utf-8')
            self.assertIn('data-theme="dark"',page); self.assertIn('scene-atp-count',page)
            self.assertNotIn('video-caption',page)
            self.assertNotIn('caption-seg-atp',page)
            self.assertIn('id="audio-seg-atp"',(run/'index.html').read_text(encoding='utf-8'))
            self.assertEqual(parts[0]['frames'],78)
            motions[0]['target']='#missing'
            (p/'scene-atp.motion.json').write_text(json.dumps(motions))
            with self.assertRaises(ValueError): assemble(m,t,theme,run)
    def test_rejects_executable_fragment(self):
        from lib.composition import validate_fragment
        for fragment in ('<img src="https://example.com/x">','<svg onload="alert(1)"></svg>','<script>bad()</script>'):
            with self.assertRaises(ValueError): validate_fragment(fragment,'scene-x')

    def test_math_requires_complete_local_assets(self):
        import shutil
        from lib.composition import stage_assets
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);assets=root/'assets'
            shutil.copytree(Path(__file__).resolve().parents[1]/'assets/runtime',assets)
            (assets/'vendor/katex/auto-render.min.js').unlink()
            with self.assertRaises(ValueError):stage_assets(assets,root/'run')

    def test_math_is_in_editable_source_not_only_standalone(self):
        import shutil
        from lib.composition import stage_assets
        with tempfile.TemporaryDirectory() as d:
            run=Path(d);m=minimal_manifest();sid=m['scenes'][0]['id']
            theme=snapshot_theme(ROOT/'.agents/skills/ml-review-pack',run)
            stage_assets(Path(__file__).resolve().parents[1]/'assets/runtime',run)
            fragments=run/'source/scene-fragments';fragments.mkdir()
            (fragments/(sid+'.html')).write_text('<section class="topic"><h3 id="'+sid+'-formula">$\\frac{1}{2}$</h3></section>')
            (fragments/(sid+'.motion.json')).write_text(json.dumps([{'target':'#'+sid+'-formula','segment_id':'seg-atp','kind':'highlight','from':{'opacity':0},'to':{'opacity':1},'duration_s':1}]))
            timeline=build_timeline(m,[{'id':'seg-atp','samples':24000,'rate':24000}])
            assemble(m,timeline,theme,run)
            for relative in [sid+'.html','source/compositions/'+sid+'.html']:
                text=(run/relative).read_text()
                self.assertIn('class="katex"',text)
                self.assertNotIn('$\\frac',text)

    def test_math_with_entities_and_less_than(self):
        from lib.math_render import render_math_fragment
        from _util import SKILL
        for fragment in ['<p>$x &lt; 1$</p>','<p>$x < 1$</p>','<p>$$\\begin{aligned}x&amp;=1\\end{aligned}$$</p>']:
            rendered=render_math_fragment(fragment,SKILL/'assets/runtime/vendor/katex')
            self.assertIn('class="katex',rendered)
            self.assertNotIn('$x',rendered)
        self.assertEqual(render_math_fragment('<p>A &amp; B</p>',SKILL/'assets/runtime/vendor/katex'),'<p>A &amp; B</p>')
