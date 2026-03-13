.PHONY: clean build test test-contracts publish publish-test help

PYTHON ?= python
PIP ?= pip

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

clean: ## Remove all build artifacts and stale .so files
	rm -rf build/ dist/ *.egg-info pyrion/*.egg-info
	find pyrion -name '*.so' -delete
	find pyrion -name '*.o' -delete
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned build artifacts and stale .so files"

build: clean ## Clean-build the package (recompiles all C extensions)
	$(PIP) install -e .
	@echo "Build complete — C extensions compiled from source"

test: ## Run full test suite
	$(PYTHON) -m pytest tests/ -v

test-contracts: ## Run only C extension contract tests (fast pre-publish check)
	$(PYTHON) -m pytest tests/test_c_extension_contracts.py -v

sdist: clean ## Build source distribution
	$(PYTHON) -m build --sdist
	@echo "sdist built in dist/"

wheel: clean ## Build wheel (recompiles C extensions)
	$(PYTHON) -m build --wheel
	@echo "wheel built in dist/"

dist: clean ## Build both sdist and wheel
	$(PYTHON) -m build
	@echo "sdist + wheel built in dist/"

publish-test: dist ## Build and upload to TestPyPI (dry run)
	@echo "=== Running contract tests before upload ==="
	$(PYTHON) -m pytest tests/test_c_extension_contracts.py -v --tb=short
	@echo ""
	@echo "=== Uploading to TestPyPI ==="
	$(PYTHON) -m twine upload --repository testpypi dist/*
	@echo ""
	@echo "Install from TestPyPI with:"
	@echo "  pip install -i https://test.pypi.org/simple/ pyrion"

publish: dist ## Build and upload to PyPI (PRODUCTION)
	@echo "=== Running contract tests before upload ==="
	$(PYTHON) -m pytest tests/test_c_extension_contracts.py -v --tb=short
	@echo ""
	@echo "=== Running full test suite ==="
	$(PYTHON) -m pytest tests/ --tb=short -q
	@echo ""
	@read -p "Upload pyrion $$($(PYTHON) -c 'from pyrion._version import __version__; print(__version__)') to PyPI? [y/N] " confirm && \
		[ "$$confirm" = "y" ] || (echo "Aborted." && exit 1)
	$(PYTHON) -m twine upload dist/*
	@echo "Published!"
