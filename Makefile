#!make

SHELL := /bin/bash

# Allow access to the local.env variables
# from https://unix.stackexchange.com/questions/235223/makefile-include-env-file
include local.env
export $(shell sed 's/=.*//' local.env)

# default target (=first)
all : run-local

include .scripts/local-setup.mk


run-local: setup run-infra-local
	# spin up apps in parallel in the foreground
	make -j run_producer_local run_consumer_local
	echo "done."

run_%_local:
	source .venv/bin/activate && cd src && python3 -m checkweb $*

run-infra-local:
	docker-compose --env-file local.env up -d

stop-infra-local:
	# spin down the compose stuff
	docker-compose --env-file local.env down

tests: unit-tests

unit-tests: setup
	# unittests -> without infrastructure/IO
	cd src && ../.venv/bin/python -m pytest

