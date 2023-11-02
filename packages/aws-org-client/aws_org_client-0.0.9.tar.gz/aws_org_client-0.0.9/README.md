# aws_org_client

[![push](https://github.com/alphagov/aws_org_client/actions/workflows/push.yml/badge.svg?branch=main)](https://github.com/alphagov/aws_org_client/actions/workflows/push.yml) [![release](https://github.com/alphagov/aws_org_client/actions/workflows/release.yml/badge.svg)](https://github.com/alphagov/aws_org_client/actions/workflows/release.yml) [![documentation](https://github.com/alphagov/aws_org_client/actions/workflows/documentation.yml/badge.svg?branch=main)](https://github.com/alphagov/aws_org_client/actions/workflows/documentation.yml) 

[![pypi](https://img.shields.io/pypi/v/aws_org_client?color=blue&label=pypi)](https://pypi.org/project/aws-org-client) [![github pages](https://img.shields.io/badge/GitHub%20Pages-222222?style=flat&logo=GitHub%20Pages&logoColor=white)](https://ideal-broccoli-37v9kn4.pages.github.io/index.html)


## Contents
* [Overview](#overview)
* [Example Usage](#example-usage)
* [Development](#development)


## Overview
This project is a python package, aimed at providing a simple interface with AWS
organisation & identity services.

Using boto3 clients:
  * identitystore
  * organizations
  * sso-admin


## Example Usage
Setup boto session & initialise organisations client to list accounts.
```python
  import boto3
  from aws_org_client.organizations import Organizations
  session = boto3.Session(profile_name='my_profile', region_name='my_region')
  client = Organizations()
  client.list_accounts()
```

Example response:
```json
  [
    {
      "Id": "string", 
      "Arn": "string", 
      "Email": "string", 
      "Name": "string", 
      "Status": "ACTIVE", 
      "JoinedMethod": "CREATED", 
      "JoinedTimestamp": datetime.datetime(1970, 1, 1, 00, 00, 00, 000000, tzinfo=tzlocal()) 
    }
  ]
```


## Development
### Requirements
* Install [python poetry](https://python-poetry.org/docs/#installation).
* You will need a working aws profile configured in your filesystem. 

### Setup
Initialise a poetry environment:
```bash
  poetry shell
```

Install dependencies:
```bash
  poetry install
```

### Project processes
#### Coverage report
run coverage report:
```bash
  poetry run coverage run -m --source=aws_org_client pytest tests
  poetry run coverage report
```

#### Linting
run pylint with:
```bash
  poetry run pylint aws_org_client
  poetry run pylint tests
```

#### Formatting
run black formatter with:
```bash
  poetry run black .
```

#### SAST
run bandit scanner:
```bash
  poetry run bandit .
```

#### Documentation
this project uses sphinx to produce a static html site; published to 
github pages.

[github actions takes care of building the site & publishing it.](.github/workflows/documentation.yml)

to update the files used to build documentation use:

```bash
  poetry run sphinx-apidoc --ext-autodoc -f -o docs .
```

include any changes to the docs directory 

##### Build Documentation locally
you may wish to build documentation locally before publishing it.

form the project root run: 
```bash
  poetry run sphinx-build docs _build
```

this will create directory ```_build``` in the project root where you can load
html in your browser.