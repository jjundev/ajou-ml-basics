from fixtures import *
import importlib
from solution_video.contracts import InputError

class ShapeTimingTests(Sandbox):
    def allocate(self,widths,width=None,height=10,interval=4):
        try:api=importlib.import_module('solution_video.shape_timing').allocate_shape_frames
        except ModuleNotFoundError:self.fail('shape budget allocator missing')
        edge=0;units=[]
        for i,w in enumerate(widths):
            units.append(dict(id='u'+str(i),step_id='s',pieces=[dict(kind='shape',id='box',clip_bbox=[edge,0,edge+w,0])]))
            edge+=w
        return api(units,dict(shapes=[dict(id='box',bbox=[0,0,edge if width is None else width,0])]),'s',height,interval)
    def test_split_invariance(self):
        self.assertEqual(sum(self.allocate([120]).values()),48)
        self.assertEqual(sum(self.allocate([5]*24).values()),48)
    def test_unequal_widths(self):self.assertEqual(list(self.allocate([10,30]).values()),[5,13])
    def test_minimum_and_overfragmentation(self):
        a=self.allocate([.1,39.9]);self.assertEqual(sum(a.values()),18);self.assertGreaterEqual(min(a.values()),1)
        with self.assertRaisesRegex(InputError,'box.*19.*18'):self.allocate([1]*19)
    def test_vertical_and_zero_height(self):
        self.assertEqual(list(self.allocate([0]).values()),[18])
        self.assertEqual(sum(self.allocate([60,60]).values()),48)
    def test_invalid_height_interval(self):
        for h,i in [(0,4),(float('nan'),4),(10,True),(10,0)]:
            with self.assertRaises(InputError):self.allocate([120],height=h,interval=i)
    def test_identity_scope(self):
        api=importlib.import_module('solution_video.shape_timing').allocate_shape_frames
        units=[dict(id='u',step_id='other',pieces=[dict(kind='shape',id='box',clip_bbox=[0,0,10,0])])]
        self.assertEqual(api(units,dict(shapes=[]),'s',10,4),{})

    def test_wide_answer_box_is_bounded(self):
        self.assertEqual(sum(self.allocate([900/24]*24,height=7).values()),90)
