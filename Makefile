ifndef VERBOSE
	MAKEFLAGS += --no-print-directory
endif

.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'



.check:
ifeq (, $(shell terraform --version))
	$(error "You must have terraform present on your desktop")
endif

start_carousel: ## start carousel
	@python app.py
