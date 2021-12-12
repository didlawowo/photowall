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

start_app: ## start carousel
	@python app.py

build-image: .dc_override .out_docker ## build dev image
	@echo "Build prod image"
	docker-compose -f build/docker-compose.yml   . build

push-tag-local: ## tag local en push
	docker tag fidforward_back fizzbuzz2/gigawall:1.0.0
 	docker push