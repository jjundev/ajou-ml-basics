import tempfile, unittest, shutil
from pathlib import Path
from _util import ROOT
from lib.theme import snapshot_theme, scene_shell

class ThemeTest(unittest.TestCase):
    def test_preserves_and_freezes_template(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); pack=root/'pack'
            shutil.copytree(ROOT/'.agents/skills/ml-review-pack/assets',pack/'assets')
            original=(pack/'assets/note-template.html').read_bytes()
            a=snapshot_theme(pack,root/'old')
            self.assertEqual((root/'old/source/templates/note-template.html').read_bytes(),original)
            page=scene_shell('<section class="topic">ATP</section>','note',a)
            self.assertIn('data-theme="dark"',page)
            self.assertNotIn('localStorage',page)
            src=pack/'assets/note-template.html'
            src.write_text(src.read_text(encoding='utf-8').replace('#3182f6','#3388ff'),encoding='utf-8')
            b=snapshot_theme(pack,root/'old'); c=snapshot_theme(pack,root/'new')
            self.assertEqual(a,b)
            self.assertNotEqual(a['templates']['note']['sha256'],c['templates']['note']['sha256'])
            (root/'old/source/template.css').write_text('corrupt')
            with self.assertRaises(ValueError): snapshot_theme(pack,root/'old')
