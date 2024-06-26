# Airport Service API

API Service for airport management, written on DRF and deployed using Docker.

## Installing using GitHub
    
```bash
git clone https://github.com/RomanHlodann/airport-api
cd py-airport-api
python -m venv venv
On mac: source venv/bin/activate Windows: venv/Scripts/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db user>
set PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```

If you want to get some data:
```bash
python manage.py loaddata airport_service_db_data.json
```

## Run with Docker
To run the project with Docker, follow these steps:

```bash
docker-compose up
```

## Features
* JWT authenticated
* Documentation is located at `/api/doc/swagger-ui/`
* Docker
* Postgresql
* Managing orders and tickets
* Managing airplane images
* Filtering flights
* Email as a username

## Access the API endpoints via 
`http://localhost:8000/`
* **Airport** `api/airport/all/`
* **Route** `api/airport/routes/`
* **Crew** `api/airport/crews/`
* **Airplane Type** `api/airport/airplanetypes/`
* **Airplane** `api/airport/airplanes/`
* **Flight** `api/airport/flights/`
* **Order** `api/airport/orders/`

To operate with tokens:
* **Get tokens** `api/users/token/`
* **Refresh token** `api/users/token/refresh/`
* **Verify token** `api/users/token/verify/`
* **Register** `api/users/register/`
* **Get profile** `api/users/me/`
