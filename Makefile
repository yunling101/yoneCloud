SHELL=/usr/bin/env bash -o pipefail
VERSION?=$(shell cat VERSION | tr -d " \t\n\r")

dev:
	@cd webserver && python manage.py runserver 0.0.0.0:8091

dev-ui:
	@gulp watch

dev-ssh:
	@cd webserver && daphne -b 0.0.0.0 -p 8001 webserver.asgi:application

docker-build:
	@bash config-generate.sh docker
	@docker build -f Dockerfile -t yunling101/yonecloud-bilingual:${VERSION} .
	@bash config-generate.sh docker-rm
