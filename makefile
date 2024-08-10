install:
	@echo "Installing app"
	@poetry install
	@poetry run pre-commit install --install-hooks
	@pip install -e .

test:
	@echo "Running tests"
	@pre-commit run --all-files
