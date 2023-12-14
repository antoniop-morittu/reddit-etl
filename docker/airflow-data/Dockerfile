ARG AIRFLOW_BASE_IMAGE="apache/airflow:latest-python3.10"
FROM ${AIRFLOW_BASE_IMAGE}

USER root
RUN mkdir -p /data && chown airflow /data \
    && mkdir -p /credentials && chown airflow /credentials 

COPY requirements.txt /requirements.txt

USER airflow

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt

