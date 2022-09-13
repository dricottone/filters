VERSION=1.0.2

PY_COMPILE_BIN=python -m py_compile

#BUILD_BIN=python -m build
BUILD_BIN=pyproject-build

#UNITTEST_FILE_BIN=python -m unittest
#UNITTEST_DIR_BIN=python -m unittest discover --top-level-directory .
UNITTEST_FILE_BIN=unittest --color
UNITTEST_DIR_BIN=unittest --color --working-directory .

#MYPY_BIN=python -m mypy
MYPY_BIN=MYPY_CACHE_DIR=gap/__mypycache__ mypy

#PIPX_BIN=python -m pipx
PIPX_BIN=pipx

.PHONY: clean
clean:
	rm -rf **/__pycache__ **/__mypycache__ **/*.pyc build *.egg-info

.PHONY: test
test:
	$(PY_COMPILE_BIN) filter/*.py rng/*.py

filter/cli.py: filter/cli.toml
	gap filter/cli.toml --no-debug-mode --output=filter/cli.py

rng/cli.py: rng/cli.toml
	gap rng/cli.toml --no-debug-mode --output=rng/cli.py

PY_FILES=rng/__main__.py rng/cli.py rng/internals.py rng/normal.py rng/notrandom.py rng/uniform.py filter/__main__.py filter/ab.py filter/cli.py filter/convolve.py filter/internals.py filter/kalman.py
PYBUILD_FILES=pyproject.toml README.md LICENSE.md

build/filters-$(VERSION)-py3-none-any.whl: $(PY_FILES) $(PYBUILD_FILES)
	mkdir -p build
	$(BUILD_BIN) --wheel --no-isolation --outdir build/

.PHONY: build
build: build/filters-$(VERSION)-py3-none-any.whl

.PHONY: reinstall
reinstall: uninstall install

.PHONY: install
install: build/filters-$(VERSION)-py3-none-any.whl
	pipx install build/filters-$(VERSION)-py3-none-any.whl

.PHONY: uninstall
uninstall:
	pipx uninstall filters

