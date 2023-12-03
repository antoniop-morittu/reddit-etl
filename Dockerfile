# Use Python image as the base image
FROM apache/airflow:latest-python3.10

WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip \
pip install --no-cache-dir -r requirements.txt

RUN mv /app/src/reddit_dag.py /opt/airflow/dags

# Switch to root user to install additional packages
USER root

# Copy your package directory into the site-packages directory in the container
COPY src/reddit_etl.py /usr/local/lib/python3.10/

# Install wget package
RUN apt-get update && apt-get install -y \
    wget

RUN chmod +x setup.sh

# Create a directory for credentials and create a keys template
RUN mkdir ./credentials && \
    echo '{ \
    "reddit": { \
    "USER_KEY": "", \
    "SECRET_KEY": "", \
    "PSW": "", \
    "USERNAME": "" \
    } \
    }' > ./credentials/keys-template.json

# Switch back to the airflow user
USER airflow

# Set the entrypoint to run the setup script
ENTRYPOINT ["/bin/bash", "setup.sh"]
