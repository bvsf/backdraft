# Servidor Base
* Sistema Operativo ubuntu-18.04.2-live-server-amd64.iso
* Configuración básica, sólo OpenSSH

# Docker
```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo docker run hello-world
```

# Compose
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

# Dockerfile & docker-compose.yml
```
http://pawamoy.github.io/2018/02/01/docker-compose-django-postgres-nginx.html
```

# To run everything
```
sudo docker-compose build
sudo docker-compose run --rm backdraft /bin/bash -c "./manage.py makemigrations"
sudo docker-compose run --rm backdraft /bin/bash -c "./manage.py migrate"
sudo docker-compose run backdraft ./manage.py collectstatic --no-input
sudo docker-compose up
```

https://medium.com/nonstopio/jenkins-django-8faddc26ab32
https://medium.com/ordergroove-engineering/continuous-deployment-of-django-applications-part-1-e3bc332bcbaf

