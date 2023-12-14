# Use Python image as the base image
FROM apache/airflow:latest-python3.10

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .

# Upgrade pip and install requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy DAGs to the Airflow DAGs directory
COPY ../dags/* /opt/airflow/dags/

# Copy the setup script to the Airflow home directory
COPY setup.sh ${AIRFLOW_HOME}

USER root

RUN mkdir -p /opt/airflow/credentials

RUN chmod +x setup.sh

# Set the entrypoint to run the setup script
USER airflow

# Set the entrypoint to run the setup script
ENTRYPOINT ["/bin/bash", "setup.sh"]