# aws_org_client

![version number](https://img.shields.io/pypi/v/aws_org_client?color=blue&label=version)

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

