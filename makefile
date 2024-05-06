install:
	@echo "Installing app"
	@poetry install
	@poetry run pre-commit install
	@pip install -e .

run:
	@echo "Running app"
	@poetry run python -m src.markets.app

test:
	@echo "Running tests"
	@pre-commit run --all-files

clean:
	@echo "Cleaning project"
	@find . -type d \
		\( -name '.venv' -o \
		-name '.*_cache' -o \
		-name '__pycache__' \) \
		-exec rm -rf {} + \
		2>/dev/null || true
