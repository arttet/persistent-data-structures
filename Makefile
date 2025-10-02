.DEFAULT_GOAL := help

################################################################################

TEST_EXTRA_ARGS ?=

export PYTHONPATH=src

################################################################################

# Note: use Makefile.local for customization
-include Makefile.local

################################################################################

## ▸▸▸ Development commands ◂◂◂

.PHONY: help
help:			## Show this help
	@fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/## //'

.PHONY: venv
venv:			## Create a virtual environment
	uv venv --clear

.PHONY: deps
deps:			## Install dependencies
	uv sync --frozen

.PHONY: audit
audit:			## Audit dependencies
	uv run pip-audit --strict --fix ${CURDIR}

.PHONY: fmt
fmt:			## Format code
	uv run isort .
	uv run ruff format

.PHONY: lint
lint:			## Lint code
	uv pip check
	uv lock --check
	uv run ty check --error-on-warning
	uv run ruff check --fix

.PHONY: test
test:			## Run tests with coverage
	uv run pytest --cov=persistent_data_structures --cov-report=term-missing ${TEST_EXTRA_ARGS}

.PHONY: clean
clean:			## Remove generated artifacts
	rm -rf .pytest_cache
	rm -rf .venv
	rm -rf .ruff_cache
	rm -rf .coverage

#######################################################################################################################
