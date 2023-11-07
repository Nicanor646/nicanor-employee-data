#!/bin/sh
# Create a python virtual environment
echo "Creating virtual environment called apienv"
python3 -m venv apienv
# Activate the virtual environment
echo "Activating virtual environment"
source apienv/bin/activate
# Install the required libraries
pip install -r requirements_local.txt

mkdir -p docker_data/db

docker pull postgres
docker run -d --name employee_data_db \
           -p $EMPLOYEE_DB_PORT:5432 \
           -v $PWD/docker_data/db:/var/lib/postgresql/data \
           -e POSTGRES_DB=$EMPLOYEE_DB_NAME \
           -e POSTGRES_USER=$EMPLOYEE_DB_USER \
           -e POSTGRES_PASSWORD=$EMPLOYEE_DB_PASSWORD \
           postgres

echo "Waiting 5 seconds for the database to be available"
sleep 5
python3 db/models.py