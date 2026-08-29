# One command: `make`. It reads data/, checks the contracts, writes the page.
# No build system, no virtualenv, no dependencies. Python 3.13 and this file.
#
# Without make:  python3 src/build.py

PYTHON ?= python3
PAGE = out/ares_interface_map.html

.DEFAULT_GOAL := page
.PHONY: page check test clean

page: ## Regenerate the interactive page from data/ into out/
	$(PYTHON) src/build.py
	@echo "Open $(PAGE) in a browser."

check: ## Validate the partner contracts and exit non-zero on any violation
	$(PYTHON) src/build.py --check-only

test: ## Run the test suite
	$(PYTHON) -m unittest discover --top-level-directory . --start-directory tests --verbose

clean: ## Remove generated output
	rm -rf out __pycache__ src/__pycache__ tests/__pycache__
