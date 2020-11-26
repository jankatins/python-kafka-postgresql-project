#!make

# Allow access to the local.env variables
# from https://unix.stackexchange.com/questions/235223/makefile-include-env-file
include local.env
export $(shell sed 's/=.*//' local.env)

# default target (=first)
all : run-local

include .scripts/local-setup.mk


run-local: setup run-infra-local
	# spin up both apps in parallel in the foreground
	echo "done."

run-infra-local:
	docker-compose --env-file local.env up -d

stop-infra-local:
	# spin down the compose stuff
	docker-compose --env-file local.env down

test: setup
	.venv/bin/pytest
