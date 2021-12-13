ifndef VERBOSE
	MAKEFLAGS += --no-print-directory
endif

.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.check:
ifeq (, $(shell docker --version))
	$(error "You must have terraform present on your desktop")
endif

start_app: ## start carousel
	@python app.py

build-image:  ## build dev image
	@echo "Build prod image"
	@docker buildx build  --platform linux/amd64 --push -t fizzbuzz2/photowall:1.0.0 .

push-tag: ## tag local en push
	@docker push fizzbuzz2/photowall:1.0.0