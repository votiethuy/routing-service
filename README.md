# Routing Service

You are provided data on the stations and lines of Singapore's urban rail system, including planned additions over the next few years. Your task is to use this data to build a routing service, to help users find routes from any station to any other station on this future network.

[![Build Status](https://travis-ci.org/votiethuy/routing-service.svg?branch=master)](https://travis-ci.org/votiethuy/routing-service)


## Dependency

- Python 3.6.8

## Instruction

### Virtualenv

Install pyenv

```
brew install pyenv
brew install pyenv-virtualenv
```

Create virtualenv python 3.6.8 

```
pyenv install 3.6.8
pyenv local 3.6.8
pyenv virtualenv 3.6.8 athena
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Activate

```bash
pyenv activate athena
```

Install requirement

```bash
pip3 install -r requirements.txt
```

For deactivate

```bash
pyenv deactivate athena
```

### Docker Build

Follow instruction to install docker: https://docs.docker.com/install/linux/docker-ce/ubuntu/

Docker build image

```bash
docker build -t athena:latest .
```

### Development

### TEST

```bash
coverage run -m unittest discover -s tests
```

### Start Service

```bash
FLASK_APP=athena FLASK_ENV=development FLASK_RUN_PORT=5000 python -m flask run
```

OR

```bash
docker run -it --rm=true --name=athena -p 5000:5000 athena:latest
```

Access via: [locahost:5000/apidocs](http://localhost:5000/apidocs)

### CI/CD

Use Travis as our CI/CD, describe step at .travis.yml

[Travis](https://travis-ci.org/votiethuy/routing-service)

Step:

- Run Test
- Image build
- Push Image to Google Container Registry
- Helm chart build
- Push helm chart to helmchart repo
- Deploy into Kubernetes Cluster