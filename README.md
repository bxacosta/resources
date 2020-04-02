## Swap File

The following lines create a 1G swap file, tested on ubunto 18.04 minimal

```bash
sudo fallocate -l 1G /swapfile
sudo dd if=/dev/zero of=/swapfile bs=1024 count=1048576
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
sudo mount -a
```

## RabbitMQ

### Docker

Run Rabbitmq on docker with management plugin enabled, for more details check docker hub documentation [here](https://hub.docker.com/_/rabbitmq)

```bash
docker run -d --hostname rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

To use any of the rabbitmq console tools like rabbitmqctl inside the docker use:

```bash
docker exec rabbitmq rabbitmqctl status
```

### Install

The following commands install the latest available version of Rabbitmq and Erlang on ubuntu 18.04 bionic, for more details check documentation [here](https://www.rabbitmq.com/install-debian.html#apt-bintray)

```bash
sudo apt install apt-transport-https
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | sudo apt-key add -
echo 'deb https://dl.bintray.com/rabbitmq-erlang/debian bionic erlang' | sudo tee -a /etc/apt/sources.list.d/bintray.rabbitmq.list
echo 'deb https://dl.bintray.com/rabbitmq/debian bionic main' | sudo tee -a /etc/apt/sources.list.d/bintray.rabbitmq.list
sudo apt update -y
sudo apt install rabbitmq-server -y --fix-missing
sudo systemctl enable rabbitmq-server
```

### Management

#### rabbitmqctl

Display information about the RabbitMQ broker
```bash
rabbitmqctl status
```

Enable management plugin
```bash
rabbitmq-plugins enable rabbitmq_management
```

Remove default virtual hosts
```bash
rabbitmqctl delete_vhost /
```

Remove default guest user
```bash
rabbitmqctl delete_user guest
```

Add virtual hosts
```bash
rabbitmqctl add_vhost [vhost]
```

Add user
```bash
rabbitmqctl add_user [user] [passwrod]
```

Set user tags for management ui access
```bash
rabbitmqctl set_user_tags [user] administrator
```

Set permissions to a user to access a virtual host
```bash
rabbitmqctl set_permissions -p [vhost] [user] ".*" ".*" ".*"
```

List users
```bash
rabbitmqctl list_users
```

List virtual hosts
```bash
rabbitmqctl list_vhosts
```

List permissions
```bash
rabbitmqctl list_permissions -p [vhost]
```

The full list of all available commands can be found [here](https://www.rabbitmq.com/rabbitmqctl.8.html).

#### rabbitmqadmin

Get a list of queues
```bash
rabbitmqadmin list queues vhost name node messages
```

Publish a message
```bash
rabbitmqadmin publish exchange=amq.default routing_key=[queue_name] payload="hello, world"
```

Get messages
```bash
rabbitmqadmin get queue=[queue_name] ackmode=ack_requeue_true
```

Other commands can be found [here](https://www.rabbitmq.com/management-cli.html).


## Heroku

Environment variables
```bash
heroku run printenv
```
