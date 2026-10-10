from pathlib import Path
import json, unittest
SKILL=Path(__file__).resolve().parents[1]
class SkillTests(unittest.TestCase):
    def test_ml_skill_contract(self):
        self.assertIn('name: ml-review-video', (SKILL/'SKILL.md').read_text())
        self.assertIn('머신러닝기초', (SKILL/'agents/openai.yaml').read_text())
        c=json.loads((SKILL/'assets/defaults.json').read_text())
        self.assertEqual((c['voice'], c['width'], c['height'], c['fps'], c['budget_usd']), ('Aoede',1920,1080,30,None))
        self.assertTrue((SKILL/'scripts/video.py').is_file())
