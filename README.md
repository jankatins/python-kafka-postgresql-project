# python-kafka-postgresql-project
Driving messages through kafka into a postgresql DB

## Implementation plan

### Step 1: setup local infra + POC 
* [] Setup a local kafka and postgresql and add makefile to run them in the background
* [] Build producer: sending a simple message through kafka
* [] Build consumer: move events into a table

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

