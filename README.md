## The "Guide" entity contains the following attributes:

- guide identifier (global and independent of the version)
- name
- short name
- description
- version (type: string, cannot be empty, unique within one directory)
- the start date of the directory of this version

## The "Directory Element" entity

- id
- guide id
- element code (type: string, cannot be empty)
- element value (type: string, cannot be empty)

## The API provides the following methods

- getting a list of guides.
- getting a list of guides relevant on the specified date
- getting the elements of the specified guide of the current version
- validation of elements of a given guide of the current version
- getting the elements of the specified guide of the specified version
- validation of an element of a given guide according to the specified version
  
## Getting a list of guides

### Request

    GET https://<host>/terminology/guides/data HTTP/1.1

<details>
<summary>Example</summary>

#### Request

    GET /terminology/guides/data HTTP/1.1

#### Response

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 1,
            "name": "specialties",
            "short_name": "",
            "description": "",
            "version": "1",
            "start_date": "2021-01-01"
        },
        {
            "id": 1,
            "name": "specialties",
            "short_name": "",
            "description": "",
            "version": "2",
            "start_date": "2021-06-01"
        },
        {
            "id": 1,
            "name": "specialties",
            "short_name": "",
            "description": "",
            "version": "3",
            "start_date": "2052-06-01"
        },
        {
            "id": 2,
            "name": "facilities",
            "short_name": "",
            "description": "",
            "version": "3",
            "start_date": "2021-04-22"
        },
        {
            "id": 2,
            "name": "facilities",
            "short_name": "",
            "description": "",
            "version": "4",
            "start_date": "2023-08-23"
        }
    ]

</details>


## Getting a list of guides relevant on the specified date

### Request

    GET https://<host>/terminology/guides/data?start_date_lte=date HTTP/1.1

`date` is specified date.

<details>
<summary>Example</summary>

#### Request

    GET /terminology/guides/data?start_date_lte=2021-03-01 HTTP/1.1

#### Response

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 1,
            "name": "specialties",
            "short_name": "",
            "description": "",
            "version": "1",
            "start_date": "2021-01-01"
        }
    ]

</details>

## Getting the elements of the specified guide of the current version

### Request

    GET https://<host>/guides/<guide_id>/guide-items/data

`<guide_id>` is guide id.

<details>
<summary>Example</summary>

#### Request

    GET /terminology/guides/1/guide-items/data HTTP/1.1

#### Response

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 1,
            "guide_id": 1,
            "code": "1",
            "value": "surgeon"
        },
        {
            "id": 2,
            "guide_id": 1,
            "code": "2",
            "value": "therapist"
        },
        {
            "id": 3,
            "guide_id": 1,
            "code": "3",
            "value": "otolaryngologist"
        },
        {
            "id": 4,
            "guide_id": 1,
            "code": "4",
            "value": "dentist"
        }
    ]

</details>


## Getting the elements of the specified guide of the specified version

### Request

    GET https://<host>/guides/<guide_id>/guide-items/data?version=specific_version

`<guide_id>` is guide id.

`specific_version` is specific version.

<details>
<summary>Example</summary>

#### Request

    GET /terminology/guides/1/guide-items/data?version=1 HTTP/1.1

#### Response

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 1,
            "guide_id": 1,
            "code": "1",
            "value": "surgeon"
        },
        {
            "id": 2,
            "guide_id": 1,
            "code": "2",
            "value": "therapist"
        },
        {
            "id": 3,
            "guide_id": 1,
            "code": "3",
            "value": "otolaryngologist"
        }
    ]

</details>


## Validation of elements of a given guide of the current version

    POST https://<host>/guides/<guide_id>/guide-items/validate HTTP/1.1
    Content-Type: application/json

    <body>

`<guide_id>` is guide id.

`<body>` is json data that needs to be validate, of the following structure:

    [
        {
            "id": <id>,
            "guide_id": <guide_id>,
            "code": <code>,
            "value": <value>
        },
        {
            "id": <id>,
            "guide_id": <guide_id>,
            "code": <code>,
            "value": <value>
        },
        ...
    ]

If data is valid then return json, of the following structure:

    {"all": true}

If data is invalid then return json, of the following structure:

    [
        {
            <id>: false
        },
        {
            <id>: false
        },
        ...
    ]

`<id>` is id of guide item.

<details>
<summary>Example</summary>

#### Request

    POST /terminology/guides/1/guide-items/validate HTTP/1.1

    [
        {
            "id": 1,
            "guide_id": 1,
            "code": "1",
            "value": "surgeon"
        },
        {
            "id": 2,
            "guide_id": 1,
            "code": "2",
            "value": "therapist"
        },
        {
            "id": 3,
            "guide_id": 1,
            "code": "3",
            "value": "otolaryngologist"
        }
    ]

#### Response

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "all": true
    }

</details>

## Validation of an element of a given guide according to the specified version

    POST https://<host>/guides/<guide_id>/guide-items/validate?version=specific_version HTTP/1.1
    Content-Type: application/json

    <body>

`<guide_id>` is guide id.

`specific_version` is specific version.

`<body>` is json data that needs to be validate, of the following structure:

    [
        {
            "id": <id>,
            "guide_id": <guide_id>,
            "code": <code>,
            "value": <value>
        },
        {
            "id": <id>,
            "guide_id": <guide_id>,
            "code": <code>,
            "value": <value>
        },
        ...
    ]

If data is valid then return json, of the following structure:

    {"all": true}

If data is invalid then return json, of the following structure:

    [
        {
            <id>: false
        },
        {
            <id>: false
        },
        ...
    ]

`<id>` is id of guide item.

<details>
<summary>Example</summary>

#### Request

    POST /terminology/guides/1/guide-items/validate?version=1 HTTP/1.1

    [
        {
            "id": 1,
            "guide_id": 1,
            "code": "1",
            "value": "surgeon"
        },
        {
            "id": 2,
            "guide_id": 1,
            "code": "2",
            "value": "therapist"
        },
        {
            "id": 3,
            "guide_id": 1,
            "code": "3",
            "value": "otolaryngologist"
        },
        {
            "id": 4,
            "guide_id": 1,
            "code": "4",
            "value": "dentist"
        }
    ]

#### Response

    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "4": false
        }
    ]

</details>
