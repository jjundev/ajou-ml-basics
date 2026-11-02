from fixtures import *
from ml_fixtures import make_bundle_run
from solution_video.util import read
from solution_video.bundle_layers import extract_bundle
from solution_video.source_integrity import validate_bundle_sources
from solution_video.contracts import ReviewError
class SourceIntegrity(Sandbox):
 def test_frozen_pdf_page_and_glyph_identity_required(self):
  run=make_bundle_run(self.run);bundle=read(run/'source/pair.json');layers=extract_bundle(read(run/'layers/candidates.json'),read(run/'source/map.json'));validate_bundle_sources(bundle,layers,run)
  page=layers['pages']['answer-1'];page['glyphs'][0]['text']='z'
  with self.assertRaisesRegex(ReviewError,'glyph'):validate_bundle_sources(bundle,layers,run)
 def test_wrong_page_or_external_svg_rejected(self):
  run=make_bundle_run(self.run);bundle=read(run/'source/pair.json');layers=extract_bundle(read(run/'layers/candidates.json'),read(run/'source/map.json'));layers['pages']['answer-1']['metadata']['page_index']=1
  with self.assertRaisesRegex(ReviewError,'page'):validate_bundle_sources(bundle,layers,run)
