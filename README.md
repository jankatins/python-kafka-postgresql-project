# checkweb

Checks a website and sends the results as events through kafka into a postgresql DB

## Install and running with local infrastructure

```bash
# setups local virtualenv from requirements.txt.freeze
make setup
# runs the (local) infra in the background via docker-compose and the two apps in the foreground
make run-local
```

To stop the local infrastructure (kafak, zookeeper, postgres):

```bash
make stop-infra-local
```

## Run Tests

Runs the unit tests in pytest and the integration_tests.py against local infrastructure

```bash
make tests
```

## Running against Aiven infrastructure

The makefile targets expect that `avn` is setup with a default project:

```bash
source .venv/bin/activate # gets you avn installed in the virtualenv
avn user login
# create a new project or reuse your current default one
avn project create <project-name>
avn project switch <project-name>
# maybe: switch the current project to a different cloud provider
avn project update --cloud do-fra
```

Creates and configures the needed services, downloads the needed credential files and 
generates the `aiven.env` file which needs to be adjusted:

```bash
# read through the errors, it might be needed to run this twice to add the kafka topic
make setup-infra-aiven
```

Afterwards edit `aiven.env` to adjust the `KAFKA_*/CONSUMER_POSTGRES_*` settings. The 
needed settings are available in the [Aiven UI of the respectiv service](https://console.aiven.io/) 

Afterwards you can run the local producer/consumer against the Aiven infrastructure

```bash
# this also automatically starts the Aiven infra if it was stoped
make run-aiven
```

To run the integration tests against Aiven Infrastructure:

```bash
# Starts up Aiven infra which was stopped
make integration-tests-aiven
```

To stop the aiven infrastructure:

```bash
make stop-infra-aiven
```

Destroying the Infrastructure is only possible in the [Aiven UI](https://console.aiven.io/).

## Maintainance

### Updating or installing new python packages

Add all directly used packages to `requirements.txt` and run:

```bash
make update-packages
```

This installs / updates all packages in `requirements.txt` and puts the currently installed packages into 
`requirements.txt.freeze`.

Ensure that everything still works by running tests

```bash
make tests
```

Afterwards commit `requirements.txt` and `requirements.txt.freeze`.

## Implementation plan

### Step 1: setup local infra + POC 
* [x] Setup a local kafka and postgresql and add makefile to run them in the background
* [x] Build producer: sending a simple message through kafka
* [x] Build consumer: move events into a table

### Step 2: Implement the requirements
* [x] Implement the requirements at the consumer and producer side
  
### Step 3: Implement testing and polish
* [x] Implement unittests with mocks
* [x] Implement an integration test which spins up new local infra, runs a few loops and then checks that the expected 
  data is in the DB + the same check with failing websites
* [x] Polish the code
* [ ] Proper Packaging: dockerfile? setup.py? 

### Step 4: Connect to Aiven infra and document  
* [x] Figure out how to spin up the infra via `avn` and document it
* [x] Run the integration tests agains Aiven Infra

## Sources:

The initial docker setup to use kafka locally + python example: 
* https://towardsdatascience.com/kafka-docker-python-408baf0e1088
* https://medium.com/big-data-engineering/hello-kafka-world-the-complete-guide-to-kafka-with-docker-and-python-f788e2588cfc
* https://medium.com/better-programming/a-simple-apache-kafka-cluster-with-docker-kafdrop-and-python-cf45ab99e2b9
* https://stackoverflow.com/questions/52438822/docker-kafka-w-python-consumer/52440056
* https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka

Makefile / virtualenv stuff:
* https://github.com/mara/mara-example-project-1/blob/master/.scripts/mara-app/install.mk
* https://unix.stackexchange.com/questions/235223/makefile-include-env-file
