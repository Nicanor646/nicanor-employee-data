# nicanor-employee-data
 An app to handle employee data

 # Requirements

 To be run locally, this app requires Docker to be installed in the instance.

# Setup

## Environment variables:

### Database

* EMPLOYEE_DB_NAME
* EMPLOYEE_DB_USER
* EMPLOYEE_DB_PASSWORD
* EMPLOYEE_DB_HOST: localhost

## Local setup

Run the following command to setup the app:

* `./setup_local.sh`

After that, run the following command to run the app:

* `./run_local.sh`

# Calling the app

## Calling the CSV endpoint

To call the CSV endpoint to load data from a file using curl:
`curl --location '{host}:{port}/csv/{type of file}' --form 'csv_file=@"/path/to/file"'`

The supported types of file are:
* employee: hired employee files
* job: job files
* department: department files

## Calling the reports endpoint

TO call the reports endpoint using curl:
`curl --location '127.0.0.1:5000/reports/{report_type}[?year={year}]'`

The supported report types are:
* employees_by_q: gives a list 
* departments_over_mean: job files

Notice the year param (`?year={year}`) is optional
