clean:
	rm -rf .mypy_cache .tox __pycache__

tests:
	pip3 install -r requirements-tests.txt
	pytest

auto-format:
	black periskop

.PHONY: clean tests auto-format