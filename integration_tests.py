"""basic integration tests for the checkweb app

# Basic idea
1) Spin up the docker compose stuff in the background with random db name and topic name
2) Spin up the local commandline version of the producer+consumer, but set the wait time to 1sec
3) Kill the producer+consumer after like 10sec
4) Check that there is stuff in the DB
5) Stop the local infra
"""

import os
import shlex
import time
import uuid
from subprocess import Popen, PIPE
from threading import Timer
import datetime

from dotenv import load_dotenv


def run(cmd, timeout_sec=60):
    """Runs a shell command with a timeout"""
    proc = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
    timer = Timer(timeout_sec, proc.terminate)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()
    return stdout, stderr


def main(is_local: bool):
    """Runs Integration tests"""

    # This assumes that the rest of the environment was already set -> run with `make tests` or `make integration-tests`
    if is_local:
        # needed, as otherwise the container will not be recreated
        print('Stopping maybe running local infrastructure...')
        run('docker-compose down')
        print("Spinning up a fresh local infrastructure")
        test_name = 'checkweb_integration_' + str(uuid.uuid4())[:10]
        os.environ['KAFKA_TOPIC'] = test_name
        os.environ['CONSUMER_POSTGRES_USER'] = test_name
        os.environ['CONSUMER_POSTGRES_PASSWORD'] = 'password'
        os.environ['CONSUMER_POSTGRES_DB'] = test_name
    else:
        print("Found CONSUMER_POSTGRES_HOST not on localhost: assuming infrastructure is already running")

    os.environ['PRODUCER_INTERVAL_SECONDS'] = '1'
    os.environ['PRODUCER_MAX_LOOPS'] = '3'

    if is_local:
        print('Starting local infrastructure...')
        run('docker-compose up -d')
        # give postgresql some time until it's up
        # TODO: replace by a something which checks if the DB is already up
        time.sleep(10)

    tstart = datetime.datetime.fromtimestamp(time.time(), tz=datetime.timezone.utc)

    cwd = os.getcwd()
    os.chdir('./src')
    print('Starting the producer for 10sec to do 3 loops...')
    run('../.venv/bin/python3 -m checkweb producer', 10)
    print('Starting the consumer for 10sec...')
    run('../.venv/bin/python3 -m checkweb consumer', 11)
    os.chdir(cwd)
    # wait a bit
    print('Waiting for the apps to do the work...')
    time.sleep(14)

    print('Checking results...')
    query = f"SELECT count(*) FROM public.content WHERE timestamp >= TIMESTAMPTZ $${tstart.strftime('%Y-%m-%d %H:%M:%S%z')}$$;"
    print(f"Query: {query}")
    escaped_query = query.replace("'", r"\'")
    os.environ['PGPASSWORD'] = os.environ['CONSUMER_POSTGRES_PASSWORD']
    ssl_mode = os.environ.get('CONSUMER_POSTGRES_SSL_MODE')
    stdout, stderr = run(f"psql {os.environ['CONSUMER_POSTGRES_DB']} --host {os.environ['CONSUMER_POSTGRES_HOST']} " +
                         f"--port {os.environ['CONSUMER_POSTGRES_PORT']} -U {os.environ['CONSUMER_POSTGRES_USER']} " +
                         (f"--set=sslmode={ssl_mode} " if ssl_mode else "") +
                         f"--tuples-only " +
                         f"-c '{escaped_query}' ", timeout_sec=3)
    if stderr.decode(encoding='utf8').strip():
        print('Stderr: ', stderr)
    try:
        rows = int(stdout.decode(encoding='utf8').strip())
        assert rows == 3, "Didn't find the number of expected rows in the result"
        print('Success: 3 new rows found.')
    except BaseException as e:
        print(f'Got unexpected result: {stdout}')
        print(f"{e!r}")


if __name__ == '__main__':
    env_path = os.environ.get('CHECKWEB_ENV_PATH', 'local.env')
    load_dotenv(dotenv_path=env_path)
    is_local = 'localhost' in os.environ['CONSUMER_POSTGRES_HOST']
    try:
        main(is_local)
    finally:
        if is_local:
            print('Stopping local infrastructure...')
            run('docker-compose down')
