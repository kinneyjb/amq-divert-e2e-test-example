# ansible

Make sure your amq is running and update [inventory/local/host_vars/localhost.yml](inventory/local/host_vars/localhost.yml) accordingly.
Then run the ansible playbook to create the topic, queues and diverts
```sh
$ ansible-playbook site.yml


```
