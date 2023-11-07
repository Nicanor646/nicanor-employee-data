#!/bin/sh
echo "Building docker"

docker network create employee_app_net

docker run -d --name employee_data_db \
           -p $EMPLOYEE_DB_PORT:5432 \
           -v $PWD/docker_data/db:/var/lib/postgresql/data \
           -e POSTGRES_DB=$EMPLOYEE_DB_NAME \
           -e POSTGRES_USER=$EMPLOYEE_DB_USER \
           -e POSTGRES_PASSWORD=$EMPLOYEE_DB_PASSWORD \
           --net employee_app_net \
           postgres

docker build -t employee_api .

mkdir -p docker_data/db

docker run -d --name employee_app \
           -e EMPLOYEE_DB_NAME=$EMPLOYEE_DB_NAME \
           -e EMPLOYEE_DB_USER=$EMPLOYEE_DB_USER \
           -e EMPLOYEE_DB_PASSWORD=$EMPLOYEE_DB_PASSWORD \
           -e EMPLOYEE_DB_PORT=$EMPLOYEE_DB_PORT
           -e EMPLOYEE_DB_HOST=employee_data_db \
           -p 8022:8022 \
           --net employee_app_net \
           employee_api

docker exec -d employee_app python3 db/models.py