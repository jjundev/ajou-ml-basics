import copy, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from _util import minimal_manifest
from lib.sources import discover
from lib.selection import require_selection, validate_clip_manifest
from lib.batch import prepare_set, resume_set, publish_set, check_scope, budget_path
from lib.cache import atomic_json, digest, file_hash
from lib.verify import review_fingerprint, DOMAINS


def fixture(repo, count=2):
    folder=repo/'복습노트/1001'; folder.mkdir(parents=True)
    (folder/'정리노트_1001_test.md').write_text('# DNA 복제\n역평행\n# 비분리\n분리 실패\n')
    inputs=discover(repo,'1001'); source=inputs['files'][0]
    topics=[{'id':f'r-{i}', 'claim':f'개념 {i}', 'source_id':source['id'],
             'locator':f'#topic-{i}', 'kind':'concept', 'decision':'animate',
             'reason':'분리와 합성 방향의 변화를 보여준다.'} for i in range(count)]
    topics.append({'id':'r-text','claim':'용어 정의','source_id':source['id'],
                   'locator':'#definition','kind':'concept','decision':'text',
                   'reason':'글과 표로 충분하다.'})
    plan={'schema_version':1,'mode':'selective','range':'1001','sources':inputs['files'],
          'source_reviews':[{'source_id':source['id'],'status':'reviewed','reason':'본문과 개념 전체 대조'}],
          'topics':topics,'clips':[{'id':f'clip-{i}','title':f'주제 {i}',
            'learning_question':f'왜 개념 {i}의 변화가 생길까',
            'requirement_ids':[f'r-{i}'],'prerequisite_ids':[],
            'visual_states':['변화 전','변화 후'],'target_duration_seconds':90}
            for i in range(count)]}
    return inputs,plan


def manifest_for(plan,clip):
    m=minimal_manifest(); m['range']=plan['range']; source=plan['sources'][0]
    m['sources']=[dict(source,path='source/inputs/'+source['id']+'.md')]
    required=set(clip['requirement_ids']+clip['prerequisite_ids'])
    m['topics'][0]['requirements']=[{k:r[k] for k in ('id','claim','source_id','locator','kind')}|{'required':True}
                                  for r in plan['topics'] if r['id'] in required]
    ids=[r['id'] for r in m['topics'][0]['requirements']]
    m['segments'][0].update(text='개념을 설명합니다.',requirement_ids=ids,source_ids=[source['id']])
    m['coverage_reviews']=[{'requirement_id':rid,'segment_ids':['seg-atp'],
                           'status':'passed','reason':'의미 대조'} for rid in ids]
    return m


def verified_fixture(run,plan,clip):
    m=manifest_for(plan,clip); atomic_json(run/'manifest.json',m)
    from test_math_evidence import write_evidence
    write_evidence(run,m)
    (run/'review.mp4').write_bytes(('video '+clip['id']).encode())
    evidence=run/'verification/evidence.txt'; evidence.parent.mkdir(exist_ok=True); evidence.write_text('fixture')
    key=review_fingerprint(run,m)
    report={'complete':True,'input_hash':key,'evidence_hashes':{'verification/evidence.txt':file_hash(evidence)}}
    for domain in DOMAINS: report[domain]={'status':'passed','evidence':['verification/evidence.txt'],'errors':[],'input_hash':key}
    atomic_json(run/'verification/report.json',report)


class SelectionTest(unittest.TestCase):
    def test_zero_one_and_multiple_are_valid_without_padding(self):
        for count in (0,1,2):
            with self.subTest(count=count), tempfile.TemporaryDirectory() as d:
                inputs,plan=fixture(Path(d),count); require_selection(plan,inputs)

    def test_empty_learning_inventory_can_select_zero_clips(self):
        with tempfile.TemporaryDirectory() as d:
            inputs,plan=fixture(Path(d),0);plan['topics']=[]
            plan['source_reviews'][0]['reason']='원문 전체를 읽었지만 영상화할 학습 개념이 없다.'
            require_selection(plan,inputs)

    def test_unassigned_animation_duplicate_ownership_and_duplicate_titles_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d))
            for change in ('missing','duplicate','title'):
                bad=copy.deepcopy(plan)
                if change=='missing':bad['clips'].pop()
                if change=='duplicate':bad['clips'][1]['requirement_ids']=['r-0']
                if change=='title':bad['clips'][1]['title']=bad['clips'][0]['title']
                with self.subTest(change=change),self.assertRaises(ValueError):require_selection(bad)

    def test_unreviewed_sources_and_changed_source_hash_block_prepare(self):
        with tempfile.TemporaryDirectory() as d:
            inputs,plan=fixture(Path(d));bad=copy.deepcopy(plan);bad['source_reviews']=[]
            with self.assertRaises(ValueError):require_selection(bad,inputs)
            Path(inputs['files'][0]['path']).write_text('변경된 본문')
            with self.assertRaises(ValueError):prepare_set(Path(d),'1001',plan,{})
            self.assertFalse((Path(d)/'복습영상').exists())

    def test_context_can_be_shared_but_clip_manifest_cannot_omit_or_add_concepts(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d));plan['topics'][-1]['decision']='context'
            for clip in plan['clips']:clip['prerequisite_ids']=['r-text']
            require_selection(plan)
            m=manifest_for(plan,plan['clips'][0]);validate_clip_manifest(plan,'clip-0',m)
            bad=copy.deepcopy(m);bad['topics'][0]['requirements'].pop()
            with self.assertRaises(ValueError):validate_clip_manifest(plan,'clip-0',bad)
            bad=copy.deepcopy(m);bad['topics'][0]['requirements'][0]['claim']='다른 주장'
            with self.assertRaises(ValueError):validate_clip_manifest(plan,'clip-0',bad)

    def test_missing_prerequisite_and_unsafe_ids_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d))
            for value in ('../escape','unknown'):
                bad=copy.deepcopy(plan)
                if value.startswith('..'):bad['clips'][0]['id']=value
                else:bad['clips'][0]['prerequisite_ids']=[value]
                with self.assertRaises(ValueError):require_selection(bad)

    def test_explicit_user_duration_can_override_default_range(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d));plan['clips'][0]['target_duration_seconds']=240
            with self.assertRaises(ValueError):require_selection(plan)
            plan['clips'][0]['duration_override_reason']='사용자가 4분 설명을 명시했다.'
            require_selection(plan)


class BatchTest(unittest.TestCase):
    def test_scope_checks_actual_source_bytes_and_budget_is_shared(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d));batch=prepare_set(Path(d),'1001',plan,{})
            recs=read_batch(batch)['clips'];runs=[batch/r['run'] for r in recs]
            m=manifest_for(plan,plan['clips'][0]);check_scope(runs[0],m)
            self.assertEqual(budget_path(runs[0]),budget_path(runs[1]))
            p=runs[0]/m['sources'][0]['path'];p.write_text('자료가 바뀌었다.')
            with self.assertRaises(ValueError):check_scope(runs[0],m)

    def test_prepare_and_resume_preserve_completed_sibling_without_network(self):
        with tempfile.TemporaryDirectory() as d, patch('urllib.request.urlopen',side_effect=AssertionError('network forbidden')):
            _,plan=fixture(Path(d));batch=prepare_set(Path(d),'1001',plan,{})
            data=json.loads((batch/'batch.json').read_text());run=batch/data['clips'][0]['run']
            verified_fixture(run,plan,plan['clips'][0])
            result=resume_set(batch)
            self.assertEqual([c['status'] for c in result['clips']],['verified','pending'])
            self.assertEqual(result['clips'][1]['next'],'coverage')
            (run/'review.mp4').write_bytes(b'tampered')
            self.assertEqual(resume_set(batch)['clips'][0]['status'],'pending')

    def test_failed_sibling_prevents_publication_and_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d));batch=prepare_set(Path(d),'1001',plan,{})
            data=json.loads((batch/'batch.json').read_text());run=batch/data['clips'][0]['run']
            verified_fixture(run,plan,plan['clips'][0])
            old=Path(d)/'복습영상/1001/기존.mp4';old.write_bytes(b'previous')
            with self.assertRaises(ValueError):publish_set(batch)
            self.assertEqual(old.read_bytes(),b'previous')
            self.assertFalse((old.parent/'주제 0.mp4').exists())

    def test_all_verified_clips_publish_with_single_materials_folder_and_valid_links(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);_,plan=fixture(root);batch=prepare_set(root,'1001',plan,{})
            data=json.loads((batch/'batch.json').read_text());date=root/'복습영상/1001'
            old=date/'기존.mp4';old.write_bytes(b'previous')
            legacy=date/'기존_제작자료';legacy.mkdir();(legacy/'review.mp4').symlink_to('../기존.mp4')
            for rec,clip in zip(data['clips'],plan['clips']):verified_fixture(batch/rec['run'],plan,clip)
            result=publish_set(batch)
            self.assertEqual(result['status'],'complete')
            self.assertEqual(sorted(p.name for p in date.iterdir()),['1001_제작자료','주제 0.mp4','주제 1.mp4'])
            for rec in data['clips']:
                run=batch/rec['run'];self.assertTrue((run/'review.mp4').is_symlink())
                self.assertTrue((run/'review.mp4').resolve().is_file())
            archived=list((date/'1001_제작자료/이전버전').rglob('기존.mp4'));self.assertEqual(len(archived),1)
            link=next((date/'1001_제작자료/이전버전').rglob('review.mp4'))
            self.assertEqual(link.read_bytes(),b'previous')
            self.assertEqual(publish_set(batch)['status'],'complete')

    def test_zero_clips_publish_selection_only_and_changed_plan_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            _,plan=fixture(Path(d),0);batch=prepare_set(Path(d),'1001',plan,{})
            self.assertEqual(publish_set(batch)['status'],'complete')
            self.assertFalse(list((Path(d)/'복습영상/1001').glob('*.mp4')))
            p=batch/'selection.json';changed=json.loads(p.read_text());changed['topics'][0]['claim']='changed';atomic_json(p,changed)
            with self.assertRaises(ValueError):resume_set(batch)

    def test_new_set_preserves_earlier_batch_videos_and_blocks_old_republication(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);_,plan=fixture(root,1);first=prepare_set(root,'1001',plan,{})
            rec=read_batch(first)['clips'][0];run=first/rec['run'];verified_fixture(run,plan,plan['clips'][0])
            publish_set(first);old_hash=file_hash(run/'review.mp4')
            plan['clips'][0]['title']='새 제목';second=prepare_set(root,'1001',plan,{})
            rec2=read_batch(second)['clips'][0];verified_fixture(second/rec2['run'],plan,plan['clips'][0])
            publish_set(second)
            self.assertEqual(file_hash(run/'review.mp4'),old_hash)
            self.assertEqual(resume_set(first)['clips'][0]['status'],'verified')
            with self.assertRaises(ValueError):publish_set(first)

    def test_cli_plan_check_prepare_set_and_resume_set(self):
        from video import main
        with tempfile.TemporaryDirectory() as d,patch('urllib.request.urlopen',side_effect=AssertionError('network forbidden')):
            root=Path(d);_,plan=fixture(root);p=root/'selection.json';atomic_json(p,plan)
            self.assertEqual(main(['plan-check','1001','--repo',d,'--selection',str(p)]),0)
            self.assertEqual(main(['prepare-set','1001','--repo',d,'--selection',str(p)]),0)
            batch=next((root/'복습영상/1001/1001_제작자료/실행').iterdir())
            self.assertEqual(main(['resume-set','--batch',str(batch)]),0)

    def test_publication_retries_after_partial_export_without_losing_old_video(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            root=Path(d).resolve();_,plan=fixture(root);batch=prepare_set(root,'1001',plan,{})
            data=read_batch(batch);date=root/'복습영상/1001'
            (date/'주제 0.mp4').write_bytes(b'old version')
            for rec,clip in zip(data['clips'],plan['clips']):verified_fixture(batch/rec['run'],plan,clip)
            replace=os.replace
            def fail_second(source,dest):
                if Path(dest)==date/'주제 1.mp4':raise OSError('simulated publication interruption')
                return replace(source,dest)
            with patch('lib.batch.os.replace',side_effect=fail_second),self.assertRaises(OSError):publish_set(batch)
            self.assertEqual(publish_set(batch)['status'],'complete')
            archived=list((date/'1001_제작자료/이전버전').rglob('주제 0.mp4'))
            self.assertEqual([p.read_bytes() for p in archived],[b'old version'])


def read_batch(batch):return json.loads((batch/'batch.json').read_text())
