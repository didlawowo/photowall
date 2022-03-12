ifndef VERBOSE
	MAKEFLAGS += --no-print-directory
endif

.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) |  awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.check:
ifeq (, $(shell docker --version))
	$(error "You must have docker present on your desktop")
endif

start-dev: ## start carousel
	@python app.py

start-docker: ## start docker-compose
	docker-compose up -d 

stop-docker: ## stop docker-compose
	docker-compose stop

run-docker: ## run container
	 docker run -ti fizzbuzz2/photowall:1.1.0 bash

build-image:  ## build dev image
	@echo "Build prod image"
	@docker buildx build  --platform linux/amd64 --push -t fizzbuzz2/photowall:1.1.0 .
