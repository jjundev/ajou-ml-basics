import unittest
from _util import minimal_manifest
from lib.timing import build_timeline

class TimingTest(unittest.TestCase):
    def test_no_drift(self):
        m=minimal_manifest(); proto=m['segments'][0]
        m['segments']=[dict(proto,id=f'seg-{i}') for i in range(1000)]
        audio=[{'id':s['id'],'samples':1001,'rate':24000} for s in m['segments']]
        t=build_timeline(m,audio)
        self.assertEqual(t['total_frames'],(t['total_samples']*30+23999)//24000)
        self.assertEqual(t['segments'][1]['start_sample']-t['segments'][0]['start_sample'],8201)
        self.assertEqual(sum(s['last_frame']-s['first_frame'] for s in t['scenes']),t['total_frames'])
    def test_invalid_audio(self):
        for samples in (0,-1,True):
            with self.assertRaises(ValueError): build_timeline(minimal_manifest(),[{'id':'seg-atp','samples':samples,'rate':24000}])
        with self.assertRaises(ValueError): build_timeline(minimal_manifest(),[])
