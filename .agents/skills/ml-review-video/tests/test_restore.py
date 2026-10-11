import unittest
from pathlib import Path
class RestoreTests(unittest.TestCase):
 def test_complete_ml_source_tree_restored(self):
  s=Path(__file__).resolve().parents[1]
  for name in ('SKILL.md','scripts/video.py','scripts/lib/math_evidence.py','scripts/lib/math_render.py','assets/video-layout.css'):
   self.assertTrue((s/name).is_file(),name)

 def test_restoration_and_render_provenance_hashes(self):
  import json,hashlib
  s=Path(__file__).resolve().parents[1]
  restore=json.loads((s/'assets/restore-provenance.json').read_text())
  self.assertEqual(restore['commit'],'7b2028e82f92962dd12b7f8b76580f6ee7b39682')
  port=json.loads((s/'assets/render-port-provenance.json').read_text())
  current={r['destination']:r['ported_sha256'] for r in port['files']+port['ml_changes']}
  upgrade=json.loads((s/'assets/upgrade-provenance.json').read_text())
  current.update({r['path']:r['sha256'] for r in upgrade['files']})
  for row in upgrade['files']:
   self.assertEqual(hashlib.sha256((s/row['path']).read_bytes()).hexdigest(),row['sha256'],row['path'])
  for row in restore['files']:
   actual=hashlib.sha256((s/row['path']).read_bytes()).hexdigest()
   self.assertEqual(actual,current.get(row['path'],row['source_sha256']),row['path'])
