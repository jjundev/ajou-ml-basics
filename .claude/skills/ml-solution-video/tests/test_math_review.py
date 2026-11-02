from fixtures import *
from solution_video.math_review import validate_math_review
from solution_video.contracts import ReviewError
class MathTests(Sandbox):
 def test_math_review_covers_current_order_and_dimensions(self):
  fields=['variables','dimensions','assumptions','derivation','numeric_checks','visual_checks']
  r=dict(status='passed',input_hash='current',steps=[dict(step_id='answer-1::s1',source_refs=['pdf:source/snapshots/a.pdf#page=1'],meaning_review='Compared sign and dimensions.',**{k:dict(applicable=True,evidence='checked '+k) for k in fields})])
  validate_math_review(r,['answer-1::s1'],'current')
  r['steps'][0]['dimensions']['evidence']=''
  with self.assertRaisesRegex(ReviewError,'dimensions'):validate_math_review(r,['answer-1::s1'],'current')
 def test_stale_and_na_without_reason(self):
  with self.assertRaises(ReviewError):validate_math_review(dict(status='passed',input_hash='old',steps=[]),[],'current')
