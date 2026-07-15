.PHONY: build serve watch _rebuild

PORT ?= 3000
PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

build:
	$(PYTHON) website/build.py

serve: build
	python3 -m http.server $(PORT) -d docs

watch: build
	@python3 -m http.server $(PORT) -d docs & \
	SERVER_PID=$$!; \
	cleanup() { kill $$SERVER_PID 2>/dev/null; exit 0; }; \
	trap cleanup INT TERM; \
	echo "Server on http://localhost:$(PORT) (PID $$SERVER_PID)"; \
	while find website \( -name '*.html' -o -name '*.css' -o -name '*.js' -o -name '*.py' \) | entr -d $(MAKE) _rebuild; do :; done; \
	cleanup

_rebuild:
	$(PYTHON) website/build.py
