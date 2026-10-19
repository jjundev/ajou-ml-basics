def pytest_configure(config):
 config.addinivalue_line('markers','pdf: verify actual rendered PDFs')
 config.addinivalue_line('markers','browser: verify real browser rendering')
