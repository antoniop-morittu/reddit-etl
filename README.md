
# Introduction

This app use the Reddit API in order to get list of posts.

Trough Airflow is possible to use the relate script's Reddit API with the relate DAG

# Structure 

```bash
.
|____.dockerignore
|____credentials
| |____keys.json
|____dags
|____Dockerfile
|____main.py
|____output
|____README.md
|____requirements.txt
|____setup.sh
|____src
| |____reddit_dag.py
| |____reddit_etl.py
| |______init__.py
```

- main.py : Script that help try the Reddit API
- src/
    - reddit_etl.py : Script that contain method and function to get Posts from reddit
    - reddit_dag.py : Airflow's DAG script

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

# Docker

- WORKDIR : `/app`
- Build Docker Image: `docker build . -t airflow-reddit`

## Structure 

### Before run the docker instance

*by default the reddit_dag.py is moved into the airflow dags folder, if it is needs create the volume to `:/opt/airflow/dags`*

```bash

docker run -p 8080:8080 -v /path/to/local/dags:/opt/airflow/dags -v /path/to/local/output:/app/output -v /path/to/local/credentials:/app/credentials -d airflow-reddit

# /app - Directory Tree Example

./app
|____output         # Volume to desidered directory where store csv                         -v /path/to/local/output:/app/output
|____dags           # Volume where put and modify dags                          [optional]    -v /path/to/local/dags:/opt/airflow/dags
|____credentials    # Volume to folder where are stored credentials in keys.json       -v /path/to/local/credentials:/app/credentials
| |____keys.json
|____setup.sh       # Script that activate airflow standalone when container start
|____src            # Package with Reddit API tools
| |____reddit_etl.py
| |______init__.py
|____main.py        # Script to try out without the use of Airflow
|____README.md
|____requirements.txt
```

### Docker run examples

docker run -p 8080:8080 -v /path/to/local/dags:/opt/airflow/dags -v -d airflow-reddit

## Standard

```bash
docker run \
-p 8080:8080 \
-v /path/to/local/credentials:/app/credentials \
-v /path/to/local//output:/app/output \
-d airflow-reddit
```

## Standard + Dags volume

```bash
docker run \
-p 8080:8080 \
-v /path/to/local/dags:/opt/airflow/dags \ 
-v /path/to/local/credentials:/app/credentials \ 
-v /path/to/local/output:/app/output \
-d airflow-reddit
```

