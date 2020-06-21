
unittest = unittest --color
#unittest = python -m unittest
unittest_discover = unittest --color --working-directory .
#unittest_discover = python -m unittest discover tests --top-level-directory . --start-directory
python = python3

clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build dist filters.egg-info

test:
	$(python) -m py_compile filter/*.py rng/*.py
	#$(unittest_discover) tests

build:
	gap filter/cli.toml --no-debug-mode --output=filter/cli.py
	gap rng/cli.toml --no-debug-mode --output=rng/cli.py
	$(python) setup.py sdist bdist_wheel

unittest:
	$(unittest_discover) tests --verbose
	$(unittest) tests/generated_syntax_tests.py --verbose

reinstall: uninstall install

install:
	pipx install .

uninstall:
	pipx uninstall filters


