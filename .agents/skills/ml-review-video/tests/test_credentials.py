import os, stat, tempfile, unittest, subprocess, sys
from pathlib import Path
from unittest.mock import patch
from _util import SKILL
from lib.credentials import copy_env_file, CredentialError
from lib.vertex_tts import load_key, VertexError
class CredentialTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
  self.root=Path(self.temp.name); self.src=self.root/'source';self.dst=self.root/'.env'
  self.src.write_text('GEMINI_API_KEY=TEST_ONLY_FILE_KEY\n')
 def test_copy_mode_0600(self):
  self.assertEqual(copy_env_file(self.src,self.dst),'copied')
  self.assertEqual(self.src.read_bytes(),self.dst.read_bytes())
  self.assertEqual(stat.S_IMODE(self.dst.stat().st_mode),0o600)
 def test_reuse_identical(self):
  self.dst.write_bytes(self.src.read_bytes()); self.dst.chmod(0o644)
  self.assertEqual(copy_env_file(self.src,self.dst),'reused')
  self.assertEqual(stat.S_IMODE(self.dst.stat().st_mode),0o600)
 def test_conflict_preserves_destination(self):
  self.dst.write_text('KEEP')
  with self.assertRaises(CredentialError):copy_env_file(self.src,self.dst)
  self.assertEqual(self.dst.read_text(),'KEEP')
 def test_missing_and_symlink_rejected(self):
  with self.assertRaises(CredentialError):copy_env_file(self.root/'missing',self.dst)
  link=self.root/'link';link.symlink_to(self.src)
  with self.assertRaises(CredentialError):copy_env_file(link,self.dst)
  self.dst.symlink_to(self.src)
  with self.assertRaises(CredentialError):copy_env_file(self.src,self.dst)
 def test_explicit_file_precedes_environment(self):
  with patch.dict(os.environ,{'GOOGLE_API_KEY':'TEST_ONLY_ENV_KEY'},clear=True):
   self.assertEqual(load_key(self.src),'TEST_ONLY_FILE_KEY')
   self.src.write_text('# no key')
   with self.assertRaises(VertexError):load_key(self.src)
 def test_environment_fallback_without_file(self):
  with patch.dict(os.environ,{'GOOGLE_API_KEY':'TEST_ONLY_ENV_KEY'},clear=True):
   self.assertEqual(load_key(),'TEST_ONLY_ENV_KEY')
 def test_cli_never_prints_secret(self):
  command=[sys.executable,str(SKILL/'scripts/setup_env.py'),'--source',str(self.src),'--destination',str(self.dst)]
  for expected in (0,1):
   if expected:self.dst.write_text('OTHER_TEST_SECRET')
   result=subprocess.run(command,capture_output=True,text=True)
   self.assertEqual(result.returncode,expected)
   self.assertNotIn('TEST_ONLY_FILE_KEY',result.stdout+result.stderr)
   self.assertNotIn('OTHER_TEST_SECRET',result.stdout+result.stderr)
