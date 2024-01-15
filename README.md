# Introduction

This app use the Reddit API in order to get list of posts.

It uses the opensource software Airflow, that allows to create DAGs that have the objective to collect data during a period of time.

# Structure 

```bash
.
├── config                          
│   └── credentials                     <- To use the Reddit API,  
│       └── keys.json                       credentials needs to be store as keys.json
├── dags
│   ├── custom                          <- Custom tools, etc. used in the DAG
│   │   ├── api.py 
│   │   ├── cli.py
│   │   ├── debug.py
│   │   ├── decorator.py
│   │   ├── etl.py
│   │   ├── __init__.py
│   │   └── tools.py
│   └── reddit_dag.py
├── data
├── docker
│   ├── airflow-data                    <- Docker Base Image for Airflow
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── airflow-standalone
│       ├── Dockerfile
│       ├── requirements.txt
│       └── setup.sh
├── docker-compose.yaml                
├── LICENSE
├── logs                           
├── main.py                             <- Script for CLI test
├── Makefile                            <- Makefile to install, test, lint and format
├── package                             
│   └── reddit-api                      <- Code same as custom directory built as Python package
│       ├── setup.py
│       └── src
│           └── reddit_api
│               ├── api.py
│               ├── cli.py
│               ├── debug.py
│               ├── decorator.py
│               ├── etl.py
│               ├── __init__.py
│               └── tools.py
├── README.md                           <- This file
└── requirements-dev.txt                <- Requirements for developer purpose

```

- main.py : Script to try out package reddit-api by command line
- dags/
    - custom : Script that contain tools, method and function to get posts from reddit
    - reddit_dag.py : Airflow's DAG script
- data/, logs/, config/credentials/ -> this directory are used as shared volumes when docker-compose up

## Credentials

create `keys.json` and popular the fields 

Example:

```json

{ 
    "reddit": { 

        "USER_KEY": "", 
        "SECRET_KEY": "", 
        "PSW": "", 
        "USERNAME": "" 
    } 
}

```
Command to create keys.json
```bash
mkdir ./config/credentials && \
    echo '{ \
    "reddit": { \
    "USER_KEY": "", \
    "SECRET_KEY": "", \
    "PSW": "", \
    "USERNAME": "" \
    } \
    }' > ./config/credentials/keys-template.json
```

# Usage

To get started with the code examples, start Airflow in docker using the following command:

```
docker-compose up -d --build
```

Wait for a few seconds and you should be able to access the examples at http://localhost:8080/.

To stop running the examples, run the following command:

```
docker-compose down
```

## Docker Image airflow-standalone Structure 

### Before run the docker instance

*in order to modify dag meanwhile the container is up is suggested to create a shared volume`:/opt/airflow/dags`*

```bash

docker run -p 8080:8080 -v /path/to/local/dags:/opt/airflow/dags -v /path/to/local/output:/app/output -v /path/to/local/credentials:/app/credentials -d airflow-reddit

# /opt/airflow - Directory Tree Example

./
├── data                # Volume to desidered directory where store csv                   -v /path/to/local/output:/app/output
├── logs                # Volume where put and modify dags                                -v /path/to/local/dags:/opt/airflow/dags
├── credentials         # Volume to folder where are stored credentials in keys.json      -v /path/to/local/credentials:/credentials/
│   └── keys.json
├── dags
│   └── reddit_dag.py   # ETL Dag to collect posts 
│   └── custom          # Package with Reddit API tools
│       └── api.py
|            ... 
├── requirements.txt
└── setup.sh            # Script that activate airflow standalone when container start
```
