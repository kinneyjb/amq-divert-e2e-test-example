# event-diversion

A simple example of using:

* activemq with topics, queues, and diverts
* qpid proton python to implement simple queue processes
* ansible to automate setting up topcs, queues, and diverts

This example uses Red Hat AMQ 7.2, and Qpid Proton Python.

Find the [ansible playbooks to setup the example here](./ansible/README.md).
Find the [qpid-proton python tests here](./app).


The overall concept is:

```
Given a topic named 'events'
  And many sub processes implemented with queues
When a message is published to the 'events' topic
  And the message has a property defined named 'subject'
  And for each 'subject' an activemq divert is configured to filter messags to related queues
Then the message gets routed to the relevant queue based on subject
  And the qpid proton processes the message
  And the qpid proton published back to the events topic with a new 'subject'
  And all queues are processed
  And all messages are published to the events topic
  And a logger listening to the events topic can capture all events
  And the logger can be used to verify end to end testing by inspecting the messages.
```

## running

### Step 1) create and start a broker

If you have Red Hat AMQ 7.2 locally

```sh
$ ls
amq-broker-7.2.0

$ amq-broker-7.2.0/bin/artemis create broker
# user admin/admin, accept anonymous connections

$ cd broker
$ ./bin/artemis run
```

### Step 2) setup amq

Run the ansible playbook:

```sh
$ cd ansible
$ ansible-playbook site.yml

```

### Step 3) run the pytest

```sh
$ cd app
$ pipenv sync --dev
$ pipenv shell
$ pytest tests
```

### Step 4) browse the messages in the amq console.

e.g. [http://localhost:8161/console/artemis/browseQueue?tab=artemis&nid=root-org.apache.activemq.artemis-%220.0.0.0%22-addresses-%22events%22-queues-%22multicast%22-%22events%22](http://localhost:8161/console/artemis/browseQueue?tab=artemis&nid=root-org.apache.activemq.artemis-%220.0.0.0%22-addresses-%22events%22-queues-%22multicast%22-%22events%22)
