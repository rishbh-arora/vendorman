# Vendor managemenet System

# Setup

1.  Clone the repository:
    Get the repo locally to setup the server by simply running `git clone https://github.com/rishbh-arora/vendorman`
    <br>

2.  Configuring the environment variables:
    All environment variables to configure the settings must be stored in `path/to/base/directory/.env`. The `.env` file should be in the same directory as `manage.py`

    ```
    SECRET_KEY={YOUR_SECRET_KEY}
    DB_NAME={YOUR_DATABASE_NAME}
    DB_USER={YOUR_DATABASE_USERNAME}
    DB_PASSWORD={YOUR_DB_PASSWORD}
    DB_HOST={YOUR_DB_HOSTURL}
    DB_PORT={YOUR_DB_PORT}
    django_admin_username= {ADMIN_USERNAME}
    django_admin_password= {ADMIN_PASSWORD}
    django_admin_email = {ADMIN_EMAIL_ID}
    ```

    - To start a developement server, set `DJANGO_ENV=vendorman.settings.dev`.
    - For a production server, set `DJANGO_ENV=vendorman.settings.prod`
      <br>

3.  Depending on your enviroment, run the build command:
    Linux/Mac: `chmod +x setup.sh && ./setup.sh`
    Windows: `setup.bat`
    The Build command handles generating migrations, migrating and making the admin superuser using the environment variables set. **Make sure that your connected database does not contain any data/tables before running build command for a fresh migration**
    <br>
4.  Finally, start the server:
    For developement server: `python manage.py runserver`
    For Production server: `gunicorn newsapi.wsgi`

# Endpoints

## Authentication

The API uses Django's out of the box **Token Authentication** to autheticate users.

- **POST** /token: Client sends username and password for autheticataion. Returns a json containing authentication token if user authenticated.<br/>
  Request body template:

  ```
  body: {
      "username": "John_doe",
      "password": "Johnpa"
  }
  ```

  <br/>
  Response body template:

  ```
    body: {
        "token":  "XXXXXXXXXX"
    }
  ```

**All endpoints moving forward will be protected and will require an Authorization Header containing the recieved token.**

```
  header: {
    ....
      "Authorization":  "Token XXXXXXXXXX"
    ....
  }
```

## Create Manager accounts

- **POST** /users: Since vendor management is an internal API rather than for public use (customers), only the admin (superuser generated in setup) may create accounts for the organizations' managers.<br/>
  Request body template:

  ```
  body: {
      "username": "John_doe",
      "password": "Johnpa"
  }
  ```

  <br/>
  Response body template:

  ```
    body: {
        "username":  "John_doe",
        "password": "XXXXXXXXXXX" #Encrypted code
    }
  ```

- **DELETE** /users/[username]: The admin (superuser) may delete a manager account with [username].<br/>

## Vendor

This set of endpoints manages Vendor information.

### GET /api/vendors

Returns all vendors
Response body template: **/api/vendors**

```
body: [
    ...
        {
        "vendor_code": "XXXX",
        "name": "XXXX",
        "contact_details": "XXXX",
        "address": "XXXX",
        "on_time_delivery_rate": XX.XX,
        "quality_rating_avg": XX.XX,
        "average_response_time": XX.XX,
        "fullfillment_rate": XX.XX
    },
    {
        "vendor_code": "XXXX",
        "name": "XXXX",
        "contact_details": "XXXX",
        "address": "XXXX",
        "on_time_delivery_rate": XX.XX,
        "quality_rating_avg": XX.XX,
        "average_response_time": XX.XX,
        "fullfillment_rate": XX.XX
    }
    ...
]
```

### GET /api/vendors/[vendor_code]

Returns the vendor with [vendor_code]
Response body template: **/api/vendors/[vendor_code]**

```
body: {
    "vendor_code": "XXXX",
    "name": "XXXX",
    "contact_details": "XXXX",
    "address": "XXXX",
    "on_time_delivery_rate": XX.XX,
    "quality_rating_avg": XX.XX,
    "average_response_time": XX.XX,
    "fullfillment_rate": XX.XX
}
```

### POST /api/vendors

Creates new vendor
Request body template: **/api/vendors**

```
body: {
    "vendor_code" : "XXXX",
    "name" : "XXXX",
    "address" : "XXXX",
    "contact_details" : "XXXX"
}
```

Response body template:

```
body: {
    "vendor_code": "XXXX",
    "name": "XXXX",
    "contact_details": "XXXX",
    "address": "XXXX",
    "on_time_delivery_rate": XX.XX,
    "quality_rating_avg": XX.XX,
    "average_response_time": XX.XX,
    "fullfillment_rate": XX.XX
}
```

- Metrics fields (on_time_delivery_rate, quality_rating_avg, average_response_time, fullfillment_rate) are not allowed to be manually set. These fields are updated as per Purchase Order edits.

### DELETE /api/vendors/[vendor_code]

- Deletes vendor with vendor_code passed in URL params.
- All related purchase orders and history snapshots are deleted.
  Request body template: **/api/vendors**

### PUT /api/vendors/[vendor_code]

Updates user with [vendor_code]. Metric fields are not allowed to be manually set. The method allowed partial updates, hence few or all of the fields in request template may be sent.

Request body template: **/api/vendors/[vendor_code]**

```
body: {
    "vendor_code": "XXXX",
    "name": "XXXX",
    "contact_details": "XXXX",
    "address": "XXXX",
}
```

Response body template:

```
body: {
    "vendor_code": "XXXX",
    "name": "XXXX",
    "contact_details": "XXXX",
    "address": "XXXX",
    "on_time_delivery_rate": XX.XX,
    "quality_rating_avg": XX.XX,
    "average_response_time": XX.XX,
    "fullfillment_rate": XX.XX
}

```

### GET /api/vendors/[vendor_code]/performance

Returns the vendor with [vendor_code] and it's performance metrics (on_time_delivery_date, quality_rating_avg, average_response_time, fullfillment_rate)
Response body template: **/api/vendors/[vendor_code]/performance**

```
body: {
    "vendor_code": "XXX",
    "on_time_delivery_rate": XX.XX,
    "quality_rating_avg": XX.XX,
    "average_response_time": XX.XX,
    "fullfillment_rate": XX.XX
}
```

## Purchase Orders:

- All users can create, update and delete purchase orders.
- On each update, each metric of the respective vendor is updated in line with the business logic described in the requirements document.

### GET /api/purchase_orders:

Fetches all purchase orders

Response body template: **/api/purchase_orders**

```
body: [
    ...
    {
        "po_number": "XXXX",
        "order_date": "XXXX-XX-XX XX:XX",
        "delivery_date": "XXXX-XX-XX XX:XX",
        "acknowledgement_date": "XXXX-XX-XX XX:XX",
        "issue_date": "XXXX-XX-XX XX:XX",
        "items": {
            "XXXX": "XXXX",
            "XXXX": "XXXX"
        },
        "quantity": XX,
        "status": "XXXX",
        "quality_rating": XXXX,
        "on_time": XXXX,
        "vendor": "XXXX"
    },
    {
        "po_number": "XXXX",
        "order_date": "XXXX-XX-XX XX:XX",
        "delivery_date": "XXXX-XX-XX XX:XX",
        "acknowledgement_date": "XXXX-XX-XX XX:XX",
        "issue_date": "XXXX-XX-XX XX:XX",
        "items": {
            "XXXX": "XXXX",
            "XXXX": "XXXX"
        },
        "quantity": XX,
        "status": "XXXX",
        "quality_rating": XXXX,
        "on_time": XXXX,
        "vendor": "XXXX"
    }
    ...
]
```

- **Query Filter: The API provides a filter to fetch all purchase orders related to a particular vendor through query parameters**

Response body template: **/api/purchase_orders?vendor=2**

```
body: [
    ...
    {
        "po_number": "XXXX",
        "order_date": "XXXX-XX-XX XX:XX",
        "delivery_date": "XXXX-XX-XX XX:XX",
        "acknowledgement_date": "XXXX-XX-XX XX:XX",
        "issue_date": "XXXX-XX-XX XX:XX",
        "items": {
            "XXXX": "XXXX",
            "XXXX": "XXXX"
        },
        "quantity": XX,
        "status": "XXXX",
        "quality_rating": XXXX,
        "on_time": XXXX,
        "vendor": "2"
    },
    {
        "po_number": "XXXX",
        "order_date": "XXXX-XX-XX XX:XX",
        "delivery_date": "XXXX-XX-XX XX:XX",
        "acknowledgement_date": "XXXX-XX-XX XX:XX",
        "issue_date": "XXXX-XX-XX XX:XX",
        "items": {
            "XXXX": "XXXX",
            "XXXX": "XXXX"
        },
        "quantity": XX,
        "status": "XXXX",
        "quality_rating": XXXX,
        "on_time": XXXX,
        "vendor": "2"
    }
    ...
]
```

### GET /api/purchase_orders/[po_number]:

Fetches the Purchase order with [po_number]

Response body template: **/api/purchase_orders/[po_number]**

```
body: {
    "po_number": [po_number],
    "order_date": "XXXX-XX-XX XX:XX",
    "delivery_date": "XXXX-XX-XX XX:XX",
    "acknowledgement_date": "XXXX-XX-XX XX:XX",
    "issue_date": "XXXX-XX-XX XX:XX",
    "items": {
        "XXXX": "XXXX",
        "XXXX": "XXXX"
    },
    "quantity": XX,
    "status": "XXXX",
    "quality_rating": XXXX,
    "on_time": XXXX,
    "vendor": "XX"
}
```

### POST /api/purchase_orders:

Creates new purchase order
Request body template: **/api/purchase_orders**

```
body: {
    "po_number": "XXXX",
    "order_date": "XXXX-XX-XX XX:XX",
    "delivery_date": "XXXX-XX-XX XX:XX",
    "items": {
        ...
        "XXXX": "XXXX",
        "XXXX": "XXXX"
        ...
    },
    "quantity": XX,
    "vendor": "XX"
}
```

**delivery_date must be dated after order_date**

Response body template:

```
body: {
    "po_number": "XXXX",
    "order_date": "XXXX-XX-XX XX:XX",
    "delivery_date": "XXXX-XX-XX XX:XX",
    "acknowledgement_date": null,
    "issue_date": "XXXX-XX-XX XX:XX",
    "items": {
        ...
        "XXXX": "XXXX",
        "XXXX": "XXXX"
        ...
    },
    "quantity": XX,
    "vendor": "XX",
    "status": "XXXX",
    "quality_rating": null,
    "on_time": null,
}
```

### DELETE /api/purchase_orders/[po_number]:

- Deleted purchase order with [po_number]
- Metrics update for related vendor triggered.

### PUT /api/purchase_orders/[po_number]:

Performs update of payload fields for purchase order with [po_number]
Endpoint allows partial update while being coherent will validations. Hence, the the request body may contain few or all of the attributes mentioned in template.
Request body template: **/api/purchase_orders/[po_number]**

```
body: {
    "po_number": "XXXX",
    "order_date": "XXXX-XX-XX XX:XX",
    "delivery_date": "XXXX-XX-XX XX:XX",
    "items": {
        ...
        "XXXX": "XXXX",
        "XXXX": "XXXX"
        ...
    },
    "quantity": XX,
    "vendor": "XX",
    "quality_rating": XX,
    "status": "XXXXX"
}
```

- Issue date is set as time of request as default. It is not editable by user.
- quality_rating can only be updated if `status = completed`.
- on_time is a stamp of if order was delivered on time. It is set by the API when client passes `status = completed`. Not editable by user.
- If currently `status = completed`, order_date and delivery_date are not editable. They may be updated along with status.
- acknowledgement_date is set by API at time of acknowledgement. Not editable by user.
- In case of `status = completed` request for an un-acknowledged order, order is acknowledged at request time and fullfillment_rate metric is updated.

### POST /api/purchase_orders/[po_number]/acknowledge:

Acknowledges the purchase order with [po_number]. Set's acknowledgement_date to time of request.
Each purchase order is can be acknowledged only once. In case of multiple acknowledgement requests:

Response body template:

```
body: {
    "message": "Purchase order acknowledged successfully."
}
```

For a valid acknowledgement:

```
body: {
    "message": "Purchase order acknowledged successfully."
}
```

- Acknowledgement request also updates fullfillment_rate metric.

## History:

### GET /api/history:

Fetches all purchase orders

Response body template: **/api/history**

```
body: [
    ...
    {
        "id": XXX,
        "date": "XXXXX",
        "on_time_delivery_rate": XXX,
        "quality_rating_rate": XXX,
        "average_response_time": XXXX,
        "fulfillment_rate": XXX,
        "vendor": "XX"
    },
    {
        "id": XXX,
        "date": "XXXXX",
        "on_time_delivery_rate": XXX,
        "quality_rating_rate": XXX,
        "average_response_time": XXXX,
        "fulfillment_rate": XXX,
        "vendor": "XX"
    }
    ...
]
```

- **Query Filter: The API provides a filter to fetch all purchase orders related to a particular vendor through query parameters**

Response body template: **/api/history?vendor=[vendor_code]**

```
body: [
    ...
    {
        "id": XXX,
        "date": "XXXXX",
        "on_time_delivery_rate": XXX,
        "quality_rating_rate": XXX,
        "average_response_time": XXXX,
        "fulfillment_rate": XXX,
        "vendor": [vendor_code]
    },
    {
        "id": XXX,
        "date": "XXXXX",
        "on_time_delivery_rate": XXX,
        "quality_rating_rate": XXX,
        "average_response_time": XXXX,
        "fulfillment_rate": XXX,
        "vendor": [vendor_code]
    }
    ...
]
```
