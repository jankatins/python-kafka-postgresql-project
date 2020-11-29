#!make

SHELL := /bin/bash

# default target (=first)
all : run-local

include .scripts/local-setup.mk


run-local: setup run-infra-local
	# spin up apps in parallel in the foreground
	make -j run_producer_local run_consumer_local
	echo "done."

run_%_local:
	source .venv/bin/activate && cd src && CHECKWEB_ENV_PATH=../local.env python3 -m checkweb $*

run-infra-local:
	docker-compose --env-file local.env up -d

stop-infra-local:
	# spin down the compose stuff
	docker-compose --env-file local.env down

tests: unit-tests integration-tests

unit-tests: setup
	# unittests -> without infrastructure/IO
	cd src && ../.venv/bin/python3 -m pytest

integration-tests: setup
	# spins up new local infra and runs 10 seconds of tests on it
	.venv/bin/python3 ./integration_tests.py
