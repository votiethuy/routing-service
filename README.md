# Routing Service

Project CodeName: Athena
You are provided data on the stations and lines of Singapore's urban rail system, including planned additions over the next few years. Your task is to use this data to build a routing service, to help users find routes from any station to any other station on this future network.

[![Build Status](https://travis-ci.org/votiethuy/routing-service.svg)](https://travis-ci.org/votiethuy/routing-service)
[![codecov](https://codecov.io/gh/votiethuy/routing-service/branch/main/graph/badge.svg?token=No8s3cbufI)](undefined)

Live deployment on GKE cluster: http://34.87.61.117/apidocs/

Local Development: Minikube + Skaffold
GKE Remote Deployment: Travis + Skaffold


## Local Development Instruction

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

Docker build image

```bash
docker build -t athena:latest .
```

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

### Kubernetes Local Development

Use Minikube + Helm + Skaffold

```
brew install minikube
brew install helm
brew install skaffold
```

Start Minikube

```
minikube start
```

* You can now run `skaffold build` to build the artifacts
* `skaffold run` to build and deploy
* `skaffold dev` to enter development mode, with auto-redeploy

To Auto port-forwad add flag `--port-forward`

```
skaffold dev --port-forward
```


Go to [localhost:5000/apidocs/](http://localhost:5000/apidocs/)



### CI/CD

- Use Travis as CI/CD
- Skaffold GKE profile

Detail describes at `.travis.yml` and `skaffold.yaml`

[Travis](https://travis-ci.org/votiethuy/routing-service)

Step:

- Run Test
- Trigger Google Cloud Build
- Push Image to Google Container Registry
- Deploy into Kubernetes Cluster