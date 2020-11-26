# python-kafka-postgresql-project

Driving messages through kafka into a postgresql DB

## Install and initial run

```bash
# setups local virtualenv
make setup
# runs the infra in the background via docker-compose and the two apps in the foreground
make run
```

To stop the local infrastructure (kafak, zookeeper, postgres):

```bash
make stop-infra-local
```

## Maintainance

### Updating or installing new python packages

Add all directly used packages to `requirements.txt`

```bash
make update-packages
```

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
* [] Implement the requirements at the consumer and producer side
  
### Step 3: Implement testing and polish
* [] Implement unittests with mocs
* [] Implement an integration test which spins up new local infra, runs a few minutes and then checks that the expected 
  data is in the DB + the same check with failing websites
* [] Polish the code

### Step 4: Connect to Aiven infra and document  
* [] Figure out how to spin up the infra via `avn` and document it
* [] Run the integration tests agains Aiven Infra

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
