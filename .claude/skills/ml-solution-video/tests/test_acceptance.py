from fixtures import *
class AcceptanceTests(Sandbox):
    def test_skill_is_discoverable_and_complete(self):
        skill=S/'SKILL.md'; self.assertTrue(skill.is_file()); text=skill.read_text(); self.assertIn('name: ml-solution-video',text)
        self.assertIn('원본',text); self.assertTrue((S/'agents/openai.yaml').is_file())
    def test_fake_pcm_end_to_end_problem_batch(self):
        # Opt-in integration runner produces three sandbox videos, never fake live approval.
        import os
        target=os.environ.get('ML_ACCEPTANCE_BATCH')
        if not target: self.skipTest('run tests/acceptance.py to render actual representative PDF cases')
        batch=Path(target); data=json.loads((batch/'acceptance.json').read_text())
        self.assertEqual([i['problem_id'] for i in data['checks']],['P2','P3','P8'])
        self.assertTrue(data['production_publish_blocked']);self.assertEqual(data['paid_requests'],0);self.assertEqual(data['live_audio'],'unverified')
        for i in data['checks']:
            self.assertTrue(i['technical_complete']);self.assertEqual(i['final_sha256'],hashlib.sha256(Path(i['final']).read_bytes()).hexdigest())
    def test_selected_real_pdf_acceptance_mapping(self):
        import acceptance,video,shutil
        from solution_video.util import read
        shutil.copytree(REPO/'복습노트/1007',self.run/'복습노트/1007')
        batch=video.prepare_batch(self.run,'1007',acceptance.IDS)
        data=read(batch/'batch.json');self.assertEqual([i['id'] for i in data['items']],acceptance.IDS)
        for item in data['items']:
            m,l=acceptance.author(batch/item['run'])
            self.assertEqual(m['problem_id'],item['id']);self.assertTrue(l['pages']['answer-1']['glyphs'])
        self.assertFalse((batch/'usage.json').exists())
