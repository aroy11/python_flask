from jsonschema import validate

customer_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "minLength": 4,
            "maxLength": 100
        },
        "username": {
            "type": "string",
            "minLength": 4,
            "maxLength": 15
        },
        "password": {
            "type": "string",
            "minLength": 4,
            "maxLength": 15
        },
        "address": {
            "type": "string",
            "minLength": 4,
            "maxLength": 250
        },
        "state": {
            "type": "string",
            "minLength": 2,
            "maxLength": 80
        },
        "country": {
            "type": "string",
            "minLength": 3,
            "maxLength": 80
        },
        "emailAddress": {
            "type": "string",
            "minLength": 8,
            "maxLength": 80,
            "pattern": "^[a-zA-Z0-9+._-]+@[a-zA-Z0-9+._-]+$"
        },
        "pan": {
            "type": "string",
            "minLength": 4,
            "maxLength": 20
        },
        "contactNo": {
            "type": "string",
            "minLength": 10,
            "maxLength": 14
        },
        "dob": {
            "type": "string",
            "description": "Supported formats: [MM.DD.YYYY] or [MM-DD-YYYY]",
            "pattern": "(0[1-9]|1[012])[-.](0[1-9]|[12][0-9]|3[01])[-.](19|20)[0-9]{2}"
        },
        "accountType": {
            "type": "string",
            "minLength": 5,
            "maxLength": 20
        },
        "accountNumber": {
            "type": "integer"
        }
    },
    "required": [
        "username",
        "accountNumber"
    ]
}

loan_schema = {
    "type": "object",
    "properties": {
       "username": {
        "type": "string",
        "minLength": 4,
        "maxLength": 15
      },
      "loanType": {
        "type": "string",
        "maxLength": 10
      },
      "loanAmount": {
        "type": "number",
        "maxLength": 6
      },
      "Date": {
        "type": "string",
        "description": "Supported formats: [MM.DD.YYYY] or [MM-DD-YYYY]",
        "pattern": "(0[1-9]|1[012])[-.](0[1-9]|[12][0-9]|3[01])[-.](19|20)[0-9]{2}"
      },
      "interestRate": {
        "type": "number",
        "maxLength": 6
      },
      "duration": {
        "type": "integer",
        "maxLength": 2
      }
    },
    "required": [
      "username",
      "loanType",
      "loanAmount",
      "Date",
      "interestRate",
      "duration"
    ]
}

customer_add_schema = {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "minLength": 4,
        "maxLength": 100
      },
      "username": {
        "type": "string",
        "minLength": 4,
        "maxLength": 15
      },
      "password": {
        "type": "string",
        "minLength": 4,
        "maxLength": 15
      },
      "address": {
        "type": "string",
        "minLength": 4,
        "maxLength": 250
      },
      "state": {
        "type": "string",
        "minLength": 2,
        "maxLength": 80
      },
      "country": {
        "type": "string",
        "minLength": 3,
        "maxLength": 80
      },
      "emailAddress": {
        "type": "string",
        "minLength": 8,
        "maxLength": 80,
        "pattern": "^[a-zA-Z0-9+._-]+@[a-zA-Z0-9+._-]+$"
      },
      "pan": {
        "type": "string",
        "minLength": 4,
        "maxLength": 20
      },
      "contactNo": {
        "type": "string",
        "minLength": 10,
        "maxLength": 14
      },
      "dob": {
        "type": "string",
        "description": "Supported formats: [MM.DD.YYYY] or [MM-DD-YYYY]",
        "pattern": "(0[1-9]|1[012])[-.](0[1-9]|[12][0-9]|3[01])[-.](19|20)[0-9]{2}"
      },
      "accountType": {
        "type": "string",
        "minLength": 5,
        "maxLength": 20
      }
    },
    "required": [
      "name",
      "username",
      "password",
      "address",
      "state",
      "country",
      "emailAddress",
      "pan",
      "contactNo",
      "dob",
      "accountType"
    ]
  }


def validate_json(request, schema_type):
    if schema_type == 1:
        validate(instance=request, schema=customer_schema)
    elif schema_type == 2:
        validate(instance=request, schema=loan_schema)
    elif schema_type == 3:
        validate(instance=request, schema=customer_add_schema)
