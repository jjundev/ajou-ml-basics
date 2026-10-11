import unittest,copy
from solution_video.bundle_timeline import reset_page_entry_moves
class PageEntryTests(unittest.TestCase):
 def test_new_page_pencil_is_inside_the_current_camera(self):
  move={'kind':'move','page_id':'answer-2','id':'answer-2::badge','from_id':'answer-1::last','from_bbox':[977.6477588789014,346.9387801888573,980.2099570337334,369.789274039946],'clip_bbox':[504.75,70.5,518.25,84.75],'start_frame':4754,'end_frame':4762,'lifted':True}
  camera=[183.06509708431028,-80.84514709754978,676.1556065721171,380.33752869681587]
  def screen(b):
   scale=1920/camera[2];return ((b[2]-camera[0])*scale,(b[1]+.8*(b[3]-b[1])-camera[1])*scale)
  old=screen(move['from_bbox']);self.assertTrue(old[0]>1920 or old[1]>900)
  t={'writing_spans':[move]};reset_page_entry_moves(t);point=screen(move['from_bbox']);self.assertTrue(0<=point[0]<=1920 and 0<=point[1]<=900);self.assertEqual((move['start_frame'],move['end_frame']),(4754,4762))
 def test_same_page_geometry_and_non_move_spans_are_preserved(self):
  spans=[{'kind':'move','page_id':'answer-1','id':'answer-1::next','from_id':'answer-1::prev','from_bbox':[1,2,3,4],'clip_bbox':[5,6,7,8]}, {'kind':'draw','page_id':'answer-2','id':'answer-2::next','from_id':'answer-1::prev','from_bbox':[1,2,3,4],'clip_bbox':[5,6,7,8]}];old=copy.deepcopy(spans);reset_page_entry_moves({'writing_spans':spans});self.assertEqual(spans,old)

 def test_first_move_without_a_previous_glyph_is_preserved(self):
  t={"writing_spans":[{"kind":"move","page_id":"answer-1","from_id":None}]};old=copy.deepcopy(t);reset_page_entry_moves(t);self.assertEqual(t,old)
