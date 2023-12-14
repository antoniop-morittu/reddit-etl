#!/bin/bash
echo '{ \
    "reddit": { \
    "USER_KEY": "", \
    "SECRET_KEY": "", \
    "PSW": "", \
    "USERNAME": "" \
    } \
    }' > ${AIRFLOW_HOME}/credentials/keys-template.json
    
airflow standalone