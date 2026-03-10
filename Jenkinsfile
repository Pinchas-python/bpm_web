steps:
  - name: Set up Python
    uses: actions/setup-python@v2
    with:
      python-version: 3.8
  - name: Install dependencies
    run: |
      python -m pip install --upgrade pip
      pip install playwright
      pip install -e .
  - name: Ensure browsers are installed
    run: python -m playwright install --with-deps
  - name: Run your tests
    run: pytest