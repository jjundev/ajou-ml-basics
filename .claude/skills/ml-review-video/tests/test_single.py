import tempfile,unittest,json
from pathlib import Path
from _util import minimal_manifest
from test_math_evidence import write_evidence
from lib.cache import atomic_json,file_hash
from lib.verify import verify_run,review_fingerprint,DOMAINS
from lib.single import new_single_run,publish_single
class SingleTests(unittest.TestCase):
 def test_single_delivery_and_previous_preservation(self):
  with tempfile.TemporaryDirectory() as d:
   repo=Path(d)
   def prepare(title,body):
    run=new_single_run(repo,'0930');m=minimal_manifest();m.update(range='0930',title=title)
    atomic_json(run/'manifest.json',m);write_evidence(run,m)
    (run/'review.mp4').write_bytes(body)
    evidence=run/'verification/review.txt';evidence.parent.mkdir();evidence.write_text('fixture')
    key=review_fingerprint(run,m)
    reports={k:{'status':'passed','input_hash':key,'evidence':['verification/review.txt']} for k in DOMAINS}
    return run,verify_run(run,m,reports)
   old,report=prepare('이전 영상',b'old');publish_single(old,report)
   old_hash=file_hash(old/'review.mp4')
   new,report=prepare('사후 예측분포',b'new');final=publish_single(new,report)
   self.assertEqual(final,repo.resolve()/'복습영상/0930/사후 예측분포.mp4')
   self.assertEqual(final.read_bytes(),b'new');self.assertTrue((new/'review.mp4').is_symlink())
   self.assertEqual(file_hash(old/'review.mp4'),old_hash)
   self.assertEqual(len(list((repo/'복습영상/0930').glob('*.mp4'))),1)
   latest=json.loads((repo/'복습영상/0930/0930_제작자료/latest.json').read_text())
   self.assertEqual(latest['sha256'],file_hash(final))
   self.assertEqual(publish_single(new,report),final)
 def test_stale_single_does_not_publish(self):
  with tempfile.TemporaryDirectory() as d:
   run=new_single_run(Path(d),'0930')
   with self.assertRaises(ValueError):publish_single(run,{'complete':False})
 def test_revoice_preserves_sibling_video_and_latest_entry(self):
  with tempfile.TemporaryDirectory() as d:
   repo=Path(d).resolve();old=new_single_run(repo,'0930');materials=old.parents[1];date=materials.parent
   one=date/'첫 주제.mp4';two=date/'둘째 주제.mp4';one.write_bytes(b'old-one');two.write_bytes(b'keep-two')
   (old/'review.mp4').symlink_to(one)
   atomic_json(materials/'latest.json',{'videos':[{'filename':one.name,'sha256':file_hash(one)},{'filename':two.name,'sha256':file_hash(two)}]})
   new=new_single_run(repo,'0930');m=minimal_manifest();m.update(range='0930',title='첫 주제')
   atomic_json(new/'manifest.json',m);write_evidence(new,m)
   atomic_json(new/'source/from-run.json',{'source_run':str(old),'replace_filename':one.name,'source_video_sha256':file_hash(one)})
   (new/'review.mp4').write_bytes(b'new-one');p=new/'verification/review.txt';p.parent.mkdir();p.write_text('fixture')
   key=review_fingerprint(new,m)
   reports={k:{'status':'passed','input_hash':key,'evidence':['verification/review.txt']} for k in DOMAINS}
   publish_single(new,verify_run(new,m,reports))
   self.assertEqual(one.read_bytes(),b'new-one');self.assertEqual(two.read_bytes(),b'keep-two')
   self.assertEqual((old/'review.mp4').read_bytes(),b'old-one')
   latest=json.loads((materials/'latest.json').read_text())
   self.assertEqual({v['filename'] for v in latest['videos']},{one.name,two.name})
