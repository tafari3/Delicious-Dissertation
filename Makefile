UV ?= uv
.PHONY: bootstrap format lint typecheck test verify app labs-up labs-down migrate secret-scan
bootstrap:
	$(UV) sync --extra dev
	$(UV) run alembic upgrade head
format:
	$(UV) run ruff format .
	$(UV) run ruff check . --fix
lint:
	$(UV) run ruff check .
	$(UV) run ruff format --check .
typecheck:
	$(UV) run mypy src/delicious_scanner
test:
	$(UV) run pytest
secret-scan:
	$(UV) run python scripts/secret_scan.py
verify: lint typecheck test secret-scan
migrate:
	$(UV) run alembic upgrade head
app:
	$(UV) run uvicorn delicious_scanner.app:app --host 127.0.0.1 --port 8000 --reload
labs-up:
	@echo "P2 lab is intentionally not implemented during P1. See issue #3."
labs-down:
	@echo "P2 lab is intentionally not implemented during P1. See issue #3."
