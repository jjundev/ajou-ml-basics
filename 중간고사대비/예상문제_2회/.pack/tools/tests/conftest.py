def pytest_configure(config):
 config.addinivalue_line('markers', 'pdf: actual PDF validation')
 config.addinivalue_line('markers', 'browser: actual browser report validation')
