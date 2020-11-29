"""basic integration tests for the checkweb app

# Basic idea
1) Spin up the docker compose stuff in the background with random db name and topic name
2) Spin up the local commandline version of the producer+consumer, but set the wait time to 1sec
3) Kill the producer+consumer after like 10sec
4) Check that there is stuff in the DB
5) Stop the local infra
"""

import shlex
import os
import time
from subprocess import Popen, PIPE
from threading import Timer

import uuid


def run(cmd, timeout_sec=600):
    """Runs a shell command with a timeout"""
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.terminate)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()
    return stdout, stderr


def main():
    """Runs Integration tests"""

    # This assumes that the rest of the environment was already set -> run with `make tests` or `make integration-tests`
    test_name = 'checkweb_integration_' + str(uuid.uuid4())[:10]
    os.environ['KAFKA_TOPIC'] = test_name
    os.environ['PRODUCER_INTERVAL_SECONDS'] = '1'
    os.environ['PRODUCER_MAX_LOOPS'] = '3'
    os.environ['CONSUMER_POSTGRES_USER'] = test_name
    os.environ['CONSUMER_POSTGRES_PASSWORD'] = 'password'
    os.environ['CONSUMER_POSTGRES_DB'] = test_name

    print('Starting local infrastructure...')
    run('docker-compose up -d')
    # give postgresql some time until it's up
    # TODO: replace by a something which checks if the DB is already up
    time.sleep(10)

    cwd = os.getcwd()
    os.chdir('./src')
    print('Starting the producer for 10sec to do 3 loops...')
    run('../.venv/bin/python3 -m checkweb producer', 10)
    print('Starting the consumer for 10sec...')
    run('../.venv/bin/python3 -m checkweb consumer', 11)
    os.chdir(cwd)
    # wait a bit
    print('Waiting for the app to work...')
    time.sleep(14)

    print('Checking results...')
    os.environ['PGPASSWORD'] = os.environ['CONSUMER_POSTGRES_PASSWORD']
    stdout, stderr = run(f"psql {test_name} --host {os.environ['CONSUMER_POSTGRES_HOST']} " +
                         f"--port {os.environ['CONSUMER_POSTGRES_PORT']} -U {test_name} " +
                         f"-c 'SELECT count(*) FROM public.content;' ")
    print('Expecting to see a "3" (count of rows in the table) in the output and a "1 row"', stdout, stderr)
    print('Stopping local infrastructure...')
    run('docker-compose down')
    assert b'3' in stdout, "Didn't find the number of expected rows in the result"
    print('Done...')


if __name__ == '__main__':
    main()
