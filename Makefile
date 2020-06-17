
unittest = unittest --color
#unittest = python -m unittest
unittest_discover = unittest --color --working-directory .
#unittest_discover = python -m unittest discover tests --top-level-directory . --start-directory
python = python3

clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build dist *.egg-info

test:
	$(python) -m py_compile filter/*.py
	$(unittest_discover) tests
	MYPY_CACHE_DIR=filter/__mypycache__ mypy -p filter

build:
	gap filter/cli.toml --no-debug-mode --output=filter/cli.py
	$(python) setup.py sdist bdist_wheel

unittest:
	$(unittest_discover) tests --verbose
	$(unittest) tests/generated_syntax_tests.py --verbose

install:
	pipx install --spec . filter

uninstall:
	pipx uninstall filter

