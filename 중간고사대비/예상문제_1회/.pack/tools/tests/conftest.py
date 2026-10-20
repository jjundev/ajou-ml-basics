import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

def pytest_configure(config):
 config.addinivalue_line('markers','pdf: verify actual rendered PDFs')
 config.addinivalue_line('markers','browser: verify real browser rendering')
