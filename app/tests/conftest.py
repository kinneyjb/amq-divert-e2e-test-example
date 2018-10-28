import pytest
import yaml
from subprocess import Popen
from proton.utils import BlockingConnection


@pytest.fixture
def config():
    path = '../ansible/inventory/local/host_vars/localhost.yml'
    with open(path, 'r') as file:
        data = yaml.load(file)

    return data


@pytest.fixture
def broker_url(config):
    broker = config['broker']
    return f"{broker['host']}:{broker['port']}"


@pytest.fixture
def event_topic_name(config):
    return config['topics'][0]['name']


@pytest.fixture
def blocking_connection(broker_url):
    conn = BlockingConnection(broker_url)
    yield conn
    conn.close()


@pytest.fixture
def blocking_sender(blocking_connection):
    sender = blocking_connection.create_sender(None)
    yield sender


@pytest.fixture
def blocking_receiver_for_events(blocking_connection, event_topic_name):
    receiver = blocking_connection.create_receiver(event_topic_name)
    yield receiver


@pytest.fixture
def queue_names(config):
    names = []
    for queue in config['queues']:
        names.append(queue['name'])
    return names


@pytest.fixture
def protons(broker_url, event_topic_name, queue_names):
    processes = []

    # run the apps
    for queue_name, publish_subject in zip(queue_names, queue_names[1:]):
        print(queue_name, event_topic_name, publish_subject)
        argv = [
            './app.py',
            '-b', broker_url,
            '-s', queue_name,
            '-p', event_topic_name,
            '-ps', publish_subject
        ]
        print(argv)
        processes.append(Popen(argv))
    # yield back to the test
    yield True

    # now clean up
    for process in processes:
        process.terminate()
