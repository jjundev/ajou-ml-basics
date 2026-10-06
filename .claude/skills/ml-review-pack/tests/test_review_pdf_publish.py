from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from _util import SCRIPTS
from review_pdf_publish import publish_files, publication_lock
from review_pdf_types import ReviewPdfError

class TestPublish(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.d=Path(self.tmp.name)
        self.dest=self.d/'out';self.dest.mkdir();self.stage=self.d/'stage';self.stage.mkdir()
        self.mapping={}
        for i in range(3):
            src=self.stage/f'{i}';src.write_bytes(f'new{i}'.encode());dst=self.dest/f'{i}'
            if i<2:dst.write_bytes(f'old{i}'.encode())
            self.mapping[dst]=src
    def test_success_and_backup(self):
        publish_files(self.mapping,self.d/'backup')
        self.assertEqual((self.dest/'0').read_bytes(),b'new0')
        self.assertIn(b'old0',[p.read_bytes() for p in (self.d/'backup').rglob('*') if p.is_file()])
    def test_failure_restores_existing_and_removes_new(self):
        import os
        original=os.replace;counter=0
        def fail(src,dst):
            nonlocal counter
            counter+=1
            if counter==3:raise OSError('injected third replacement failure')
            return original(src,dst)
        with patch('review_pdf_publish.os.replace',fail):
            with self.assertRaises(OSError):publish_files(self.mapping,self.d/'backup')
        self.assertEqual((self.dest/'0').read_bytes(),b'old0');self.assertEqual((self.dest/'1').read_bytes(),b'old1');self.assertFalse((self.dest/'2').exists())
    def test_missing_stage_publishes_neither(self):
        list(self.mapping.values())[1].unlink()
        with self.assertRaises(ReviewPdfError):publish_files(self.mapping,self.d/'backup')
        self.assertEqual((self.dest/'0').read_bytes(),b'old0')
    def test_same_pack_concurrent_publish(self):
        with publication_lock(self.mapping):
            with self.assertRaisesRegex(ReviewPdfError,'locked'):publish_files(self.mapping,self.d/'backup')
        self.assertEqual((self.dest/'0').read_bytes(),b'old0')
        self.assertEqual((self.stage/'0').read_bytes(),b'new0')
