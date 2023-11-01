# Odooless

![Build Status](https://github.com/Barameg/odooless/actions/workflows/build.yml/badge.svg)

An Odoo-like serverless ORM for AWS DynamoDB 


## Installation

``` pip install odooless ```

## Getting Started

Define AWS credentials as environment variables 

```python
from odooless import Model, DB

DB._region_name = 'us-west-2' # AWS region
DB._endpoint_url = 'http://localhost:8000' # Omit for AWS cloud DynamoDB
DB._aws_access_key_id = 'test' # AWS access key id
DB._aws_secret_access_key = 'test' # AWS secret access key

```

## Model Definition

To create a new model

``` python
from odooless import models


class Users(models.Model):
    _name = 'Users' # dynamodb table name
    _limit = 80 # define default limit number of records to get from db
    _fields = [
            Field(
                name='id', 
                index=True, 
                hidden=False, 
                string='ID',
                type='S', # supported field types are Binary as B, Integer as N, String as S 
                index=True # create global secondary index for this attribute
            ),
    ]
```

## Methods
Currently available methods
### create
``` python
    from models import Users

    someUser = Users().create({
        'key': 'value',
    }) # create single record

    someUsers = Users().create([
        {
            'key': 'value',
        },
        {
            'key': 'value',
        }, ...
    ]) # or create multiple records
```

### read
``` python
    from models import Users

    someUsers = Users().read(id, fields) # returns recordset 
```

### search
``` python
    from models import Users

    domain = [
        ('field1', '=', 'value0'),
        ('field2', '>=', 'value1'),                                  
        ('field3', '<=', 'value2'),                                  
        ('field4', 'IN', ['value0', 'value1', 'value2',]),
        ('field5', 'between', ['value0', 'value1',]),
        ('field5', 'contains', 'value'),
        ('field5', 'begins_with', 'value'),
        ....
    ] 
    someUsers = users.search(field0=value, domain) # the search method takes index attribute name as a keyword parameter along with a domain that does not include this attribute and returns list of records

    for user in someUsers:
        print(user.name) 
```

### search_read
``` python
    from models import Users

    domain = [
        ('field1', '=', 'value0'),
        ('field2', '>=', 'value1'),
        ('field3', '<=', 'value2'),
        ('field4', 'IN', ['value0', 'value1', 'value2',]),
        ('field5', 'between', ['value0', 'value1']),
        ('field5', 'contains', 'value'),
        ('field5', 'begins_with', 'value'),
        ....
    ] # currently simple query operators soon will add full polish-notation support

    fields = [
        'field1',
        'field2',
        ....
    ]
    someUsers = Users().search_read(field0=value, domain, fields) # the search method takes index attribute name as a keyword parameter along with a domain that does not include this attribute and returns list of records

    for user in someUsers:
        print(user.name) 
```
### write
``` python
    from models import Users

    users.write({
        'id': 'UUIDv4'
        'key': 'value',
    }) # you can update single record by passing its id to model method

    users.write([
        {
            'id': 'UUIDv4'
            'key': 'value',
        },
        {
            'id': 'UUIDv4'
            'key': 'value',
        },...
    ]) # you can update multiple records by passing id of record

    someUser = Users().read(ids)

    for user in someUsers:
        user.write({
            'key': 'value',
        }) # no need to include id if you use update on the instance
```



### delete
``` python
    from models import Users

    someUser = Users().delete(ids) # you can delete single or multiple records
```


