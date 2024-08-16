# Avito Parser with FastAPI and Selenium

## Description

This project implements a service based on FastAPI for parsing the number of listings on the Avito website by specified search queries and regions. The service uses Selenium for page parsing and SQLAlchemy for working with the database. The project also uses Docker and Docker Compose for containerization.

## Key Features

- **Adding a Search Query**: Through the `/add/` endpoint, you can add a new search query and region to monitor the number of listings.
- **Getting Statistics**: Through the `/stat/{id}` endpoint, you can get statistics on the number of listings over a certain period.
- **Task Scheduler**: The service automatically updates the number of listings for specified queries using the APScheduler.

## Project Structure

- `main.py`: The main FastAPI application file.
- `models.py`: Defines data models using SQLAlchemy.
- `database.py`: Database connection settings.
- `parsers.py`: Functions for parsing pages using Selenium.
- `scheduler.py`: Task scheduler configuration and startup.
- `Dockerfile`: File for building the Docker image of the application.
- `docker-compose.yml`: File for managing containers using Docker Compose.

## Installation and Launch

### Prerequisites

- Docker and Docker Compose must be installed on your machine.

### Launching the Project

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/TimurTsedik/avito_parsing_bot
   cd avito-parser
   ```
   
2. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```
   
3. After the containers are built, the application will be available at:
```bash
http://localhost:8000
```

## Using the API

Adding a New Query
```
POST /add/
```
Adds a new search query and region for monitoring.

Example Request:

```bash
curl -X POST "http://localhost:8000/add/" -d "query=iphone 13&region=kaliningrad"
```

Example Response:

```json
{
  "id": 1
}
```

Getting Statistics
```
GET /stat/{id}
```
Returns statistics on the number of listings for the specified query.

Example Request:
```bash
curl -X GET "http://localhost:8000/stat/1"
```

Example Response:

```json
{
  "query": "iphone 13",
  "region": "kaliningrad",
  "statistics": [
    {
      "timestamp": "2024-08-16T12:34:56Z",
      "count": 237
    },
    ...
  ]
}
```
## Technical Details

FastAPI: The main web framework for creating the API.
SQLAlchemy: Used for interacting with the database.
Selenium: Used for web page parsing.
Gunicorn: WSGI server for running FastAPI in production.
APScheduler: Task scheduler for periodically updating data.
Disclaimer

For successful page parsing, it is important to ensure that chromedriver is compatible with your processor architecture (e.g., ARM64 for Apple Silicon). Using Docker provides environment isolation and simplifies the deployment process


## Approach fot hidden API:
```
import requests

url = "https://m.avito.ru/api/11/items"
params = {
    "key": "af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir",
    "localPriority": 0,
    "locationId": 630090,
    "query": "playstation",
    "page": 1,
    "lastStamp": 1723824960,
    "display": "list",
    "limit": 25,
    "pageId": "H4sIAAAAAAAA_wTAAQpCIQwG4LvsBO3JA_13mDBEUTKJTTOiu78v4sBPwQyyYfF5z2O-EknF6UMQBYO-JArHoNWL-aLjnfT85FvtvNo-3GNGa8ttkv8VAAD__zicsBdPAAAA",
    "presentationType": "serp"
}

response = requests.get(url, params=params)
data = response.json()

# Print the JSON response
print(data)
```