# DPB1 Prediction
This tool takes in HLA typing and population information in the form of population codes and either (1) locus typing (up to five loci: A, C, B, DRB1, DQB1) in a GLstring or (2) phased multi-locus unambiguous genotypes (PMUGs). These information are then used to extract possible *HLA-DPB1* alleles from haplotype frequencies that contain *HLA-DPB1*. These alleles are than used to create likelihoods of *HLA-DPB1* at an allele level (single-locus genotypes - SLG) and at a TCE (T-cell epitope) group level. If patient and donor information are both available, then match category likelihoods (permissive vs. non-permissive mismatching) can be calculated.

## Table of Contents
- [REST Server](#rest-server-)
    - [Server Setup](#server-setup-)
    - [Preparation of Haplotype Frequencies](#preparation-of-haplotype-frequencies-)
    - [Server Initialization](#server-initialization-)
- [Testing](#testing-)
    - [BDD Testing](#bdd-testing-)
    - [BDD Results Report](#bdd-results-report)
- [Web Application](#web-app-)
    - [App Setup](#app-setup-)
    - [App Initialization](#app-initialization-)
- [DPB1 Prediction Base Image](#dpb1-prediction-base-image-)
    - [Base image build](#base-image-build-)
- [DPB1 Prediction REST Endpoints Docker Container](#dpb1-prediction-rest-endpoints-docker-container-)
    - [Prerequisite](#prerequisite-)
    - [Docker image build](#docker-image-build-)
    - [Docker container launch](#docker-container-launch-)
    - [Stopping the running container](#stopping-the-running-container-)
- [TCE Prediction Tool Docker Container](#tce-prediction-tool-docker-container-)
    - [Webapp Docker Prerequisite](#webapp-docker-prerequisite-)
    - [Webapp Docker image build](#webapp-docker-image-build-)
    - [Webapp Docker container launch](#webapp-docker-container-launch-)
    - [Stopping the running webapp container](#stopping-the-running-webapp-container-)
- [DPB1 Prediction Production Deployment](#dpb1-prediction-production-deployment-)
    - [Docker Deployment](#docker-)
    - [Unified Container Deployment](#unified-container-deployment-)

### REST Server [⤴](#table-of-contents)

#### Server Setup [⤴](#table-of-contents)

To begin preparing your repository for usage, ensure that you have Python3 installed. To check, issue this command to verify your python version:
```
python --version
```

If Python3 is not installed, please download it from [here](https://www.python.org/downloads/).

If Python3 is readily available, set up your virtual environment by running these commands:
```
python3 -m venv venv
source venv/bin/activate
```

Pip is the package installer for Python. It comes pre-packaged with Python. This will be used to install our requirements as such:
```
pip install --upgrade pip
pip install -r requirements.txt
```

#### Preparation of Haplotype Frequencies [⤴](#table-of-contents)
Reference frequencies need to be within zipped comma-delimited '.freqs' files that are named based on their population (ex: JAPI.freqs.gz). They need to contain a header that shows which column contains the haplotype name ('Haplo') and frequency ('Freq'). For example, the first line of each of the provided haplotype frequency files is 'Haplo,Count,Freq,D'. These haplotype frequency files need to be extracted and stored within the `data/frequencies/` directory. It is also possible to use your own haplotype frequency files, given they are in the same format.

To set up the default haplotype frequencies, follow these steps:

1.) Place individual population frequency files in directory:

`mkdir data/frequencies/`

#### Server Initialization [⤴](#table-of-contents)

To select a specific configuration for the server, set `FLASK_ENV` as follows:

```
export FLASK_ENV=<config>
```
`FLASK_ENV` can be set as `testing`, `production`. Otherwise, the default config weill be used.


Initialize the web service via this command:
```
python server.py
```
**Note:** This step will take several minutes (3 - 5, depending on the available resources).

Once initialized, you may use the REST API endpoints.

> *REST → **Re**presentational **S**tate **T**ransfer*
 *API → **A**pplication **P**rogramming **I**nterface*

For example, you can retrieve data from an endpoint by using cURL as shown below.


### Testing [⤴](#table-of-contents)

##### BDD Testing [⤴](#table-of-contents)

This repository was developed through *Behavior-Driven Development (BDD)*.

There is one test feature ('generate_perm_freqs.feature') that can take a while to run. Additionally, it needs to have a local server [running](#initialization-) with full haplotype frequencies initialized (which can take a couple of minutes to load). To skip this, run the following command:
```
behave --tags=-full_service
```

Otherwise, you can include this test with:
```
behave
```

##### BDD Results Report [⤴](#table-of-contents)
The results of your BDD tests can sometimes be difficult to view in the terminal. To view the tests results in the browser, we can use *allure-behave*, which was installed by pip during the [bootstrapping process](#bootstrapping-).

You will first need to specify *behave* to generate formatted *allure* results

```
behave -f allure_behave.formatter:AllureFormatter -o tests/results/
```

Finally, to view these formatted results in the browser, enter this command:
```
allure serve tests/results
```

### Web application [⤴](#table-of-contents)

#### App Setup [⤴](#table-of-contents)

We will need to go into the web app project's root folder
```
cd webapp
```

Since our web application uses JavaScript (Angular 8), install Node.js (≥10.9) and npm (node package manager) [here](https://nodejs.org/en/download/) if ```npm``` is not a recognized command in your terminal.

Through npm, we can install our dependencies by running:
```
npm install
```

#### App Initialization [⤴](#table-of-contents)

Once finished, ensure that the back-end REST server has been initialized on http://0.0.0.0:5010/ as detailed [here](#web-service-initialization-).

And then run a local development server:
```
ng serve
```

The web application will now be available on https://0.0.0.0:4200/.

## DPB1 Prediction Base Image [⤴](#table-of-contents)

The base image is used by both service and web application Dockerfiles. It contains the frequency files, tce assignments, and environment dependencies.

### Base Image Build [⤴](#table-of-contents)
The base image for subsequent images is manually built with the following command:

```
docker build -t nmdpbioinformatics/dpb1-prediction-base-image:0.0.4 -f Dockerfile-base-image .
```

## DPB1 Prediction Rest End Points Docker Container [⤴](#table-of-contents)

### Prerequisite [⤴](#table-of-contents)
The containerization is facilitated by [Docker Container](https://www.docker.com/resources/what-container). 

To be able to run Docker container, a docker setup and configuration is necessary. The installation details can be found in the [official docker documentation](https://docs.docker.com/get-docker/).

### Docker image build [⤴](#table-of-contents)
To build the image, navigate to the directory where `Dockerfile-flask` is located
Execute the comand (keep an eye on required "." at the end of the command)
```
docker build -t nmdpbioinformatics/dpb1-pred-backend:latest -f Dockerfile-flask .
```
Now the image should be built and available in the local docker registry

### Docker container launch [⤴](#table-of-contents)
To start a container form docker image (built in the last step) we need to execute the following command:

```
docker run -d -e PYTHONUNBUFFERED=1 -v $PWD/data/frequencies:/home/dpb1/data/frequencies -p 5010:5010 nmdpbioinformatics/dpb1-pred-backend:latest
```
Upon successful execution a container id should comeout. We can see the container if it is up by executing
```
docker ps -a
```
That should show us if the container is up and running. If it is up then we should be able to navigate to http://localhost:5010/ to see the API landing page.

### Stopping the running container [⤴](#table-of-contents)
We have to obtain the container id by executing 
```
docker ps -a
```
Then we have to execute 
```
docker stop $CONTAINER_ID
```

## TCE Prediction Tool Docker Container [⤴](#table-of-contents)

### Webapp Docker Prerequisite [⤴](#table-of-contents)

[DPB1 Prediction Rest End Points Docker Container](#dpb1-prediction-rest-end-points-docker-container-) is up and running for the webapp container to be working properly (for build that is not necessary).

The containerization is facilitated by [Docker Container](https://www.docker.com/resources/what-container). 

To be able to run Docker container, a docker set up and configuration is necessary. The installation details can be found in the [official docker documentation](https://docs.docker.com/get-docker/).

### Webapp Docker image build [⤴](#table-of-contents)
To build the image, navigate to the `webapp` directory where `Dockerfile` is located.
We will need to go into the web app project's root folder using the following command
```
cd webapp
```
Execute the command below(keep an eye on required "." at the end of the command)
```
docker build --build-arg CONFIGURATION="" -t nmdpbioinformatics/dpb1-web-app .
```
Now the image should be built and available in the local docker registry.

### Webapp Docker container launch [⤴](#table-of-contents)
To start the webapp container form docker image (built in the last step) we need to execute the following command:

```
docker run -d -p 80:80 -t nmdpbioinformatics/dpb1-web-app:latest
```
Upon successful execution a container id should come out. We can see the container if it is up by executing:
```
docker ps -a
```
That should show us if the container is up and running. If it is up then we should be able to navigate to http://localhost:80/ to see the Web App landing page.

### Stopping the running webapp container [⤴](#table-of-contents)
We have to obtain the container id by executing 
```
docker ps -a
```
Then we have to execute 
```
docker stop $CONTAINER_ID
```
## DPB1 Prediction Production Deployment [⤴](#table-of-contents)
The production deployment has two model, a) unified container model and b) segregated contaienrs model. 

a) The unified container packes both the backend (python-flask-gunicorn) and front end (angular and nginx) into one docker docker images while during the runtime Nginx acts as an webserver for front end and reverse proxy for backend. 

b) The segregated container deployment would provide independent scaling of backend and front end cluster should there be any need for it. Although the decoupling might be desirable under certain circumstances but this feature would require setting up an appropriate network using docker compose or Kubernetes and are currently not available.

### Unified Container Deployment [⤴](#table-of-contents)

The production `apiUrl` should be adjusted with the correct server in the file `webapp/src/environments/environment.prod.ts`

To build the docker image the following command may be executed in the project root directory:
```
docker build --build-arg CONFIGURATION="production" -t nmdpbioinformatics/dpb1-prediction .
```
After successful build we should have the docker image available in our local docker registry.

To deploy the app now we can use the following command. The application should be available in your domain, i.e. `http://host:80/`
```
docker run -d -v $PWD/tests/data/frequencies:/home/dpb1/data/frequencies -p 80:80 -t nmdpbioinformatics/dpb1-prediction:latest
```
To stop the app container, We have to obtain the container id by executing 
```
docker ps -a
```
Then we have to execute 
```
docker stop $CONTAINER_ID
```

### Docker Deployment [⤴](#table-of-contents)

Build the Docker image
```
docker build -t nmdpbioinformatics/dpb1-prediction:0.0.4 .
```

Start the Docker app
```
docker run -p 5000:5000 nmdpbioinformatics/dpb1-prediction:0.0.4
```

For testing purposes, you may use this command:
```
docker run -e PYTHONUNBUFFERED=1 -v $PWD/tests/data/frequencies:/home/dpb1/data/frequencies -p 5000:5000 nmdpbioinformatics/dpb1-prediction:0.0.4
```
