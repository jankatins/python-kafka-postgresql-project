#!make

SHELL := /bin/bash

# default target (=first)
run : run-local

include .scripts/local-setup.mk
include .scripts/aiven-setup.mk


run-local: setup-local start-infra-local
	# spin up apps in parallel in the foreground
	make -j run-producer-local run-consumer-local


run-%-local:
	source .venv/bin/activate && cd src && CHECKWEB_ENV_PATH=../local.env python3 -m checkweb $*

start-infra-local:
	docker-compose --env-file local.env up -d

stop-infra-local:
	# spin down the compose stuff
	docker-compose --env-file local.env down

tests: unit-tests integration-tests

unit-tests: setup
	# unittests -> without infrastructure/IO
	cd src && ../.venv/bin/python3 -m pytest

integration-tests: integration-tests-local

integration-tests-local: setup-local
	# spins up new local infra and runs 10 seconds of tests on it
	.venv/bin/python3 ./integration_tests.py


start-infra-aiven:
	avn service update checkweb-postgres --power-on
	avn service update checkweb-kafka --power-on

stop-infra-aiven:
	avn service update checkweb-postgres --power-off
	avn service update checkweb-kafka --power-off

list-infra-aiven:
	avn service list

run-aiven: start-infra-aiven
	make -j run-producer-aiven run-consumer-aiven

run-%-aiven: aiven.env
	source .venv/bin/activate && cd src && CHECKWEB_ENV_PATH=../aiven.env python3 -m checkweb $*
