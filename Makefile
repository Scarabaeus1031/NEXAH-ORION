.PHONY: bootstrap check test integration demo adr release-check

bootstrap:
	./scripts/bootstrap-workspace

check:
	./scripts/check-workspace

test:
	./scripts/test

integration:
	./scripts/test-ollama-integration

demo:
	PYTHONPATH=src $${ORION_PYTHON:-python3} -m orion

adr:
	@test -n "$(TITLE)" || (echo "Usage: make adr TITLE='short decision title'"; exit 2)
	./scripts/new-adr "$(TITLE)"

release-check:
	./scripts/release-check --development
