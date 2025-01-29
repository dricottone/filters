VERSION=1.0.4
SRC=$(shell find . -type f -name '*.py')

clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc dist build *.egg-info

test:
	python -m py_compile filter/*.py rng/*.py

filter/cli.py: filter/cli.toml
	gap filter/cli.toml --no-debug-mode --output=filter/cli.py

rng/cli.py: rng/cli.toml
	gap rng/cli.toml --no-debug-mode --output=rng/cli.py

PYBUILD_FILES=pyproject.toml README.md LICENSE.md

dist/filters-$(VERSION)-py3-none-any.whl: $(SRC) filter/cli.py rng/cli.py $(PYBUILD_FILES)
	mkdir -p dist
	pyproject-build --wheel --no-isolation

build: dist/filters-$(VERSION)-py3-none-any.whl

install: dist/filters-$(VERSION)-py3-none-any.whl
	pipx install dist/filters-$(VERSION)-py3-none-any.whl

uninstall:
	pipx uninstall filters

.PHONY: clean test build install uninstall
