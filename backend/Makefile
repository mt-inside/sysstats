run-dev:
	# TODO use compose and the override file instead
	docker run --rm --name sysstats_backend -v ${PWD}:/usr/src/app sysstats_backend

local-run: local-run-venv
	python backend

.PHONY: run-dev local-run
