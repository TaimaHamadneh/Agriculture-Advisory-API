# Agriculture Advisory API

A smart agricultural advisory API that compares real-time sensor data with optimal crop conditions stored in a PostgreSQL database.

## Features

- Import crop data from CSV into PostgreSQL.
- Compare input data (temperature, humidity, CO2, soil moisture) with optimal ranges.
- Generate tailored farming advice based on deviations.
- Auto-generated API docs via Swagger UI.
- Fully containerized with Docker Compose.

## Tech Stack

- FastAPI (Python)
- PostgreSQL
- Docker & Docker Compose


## Run Locally with Docker

1. Ensure Docker & Docker Compose are installed.
2. Clone the repository:
   ```bash
   git clone [https://github.com/TaimaHamadneh/agri-advisory-api.git](https://github.com/TaimaHamadneh/Agriculture-Advisory-API.git)
   cd agri-advisory-api

Run:

docker-compose up --build

Open your browser at:

http://localhost:8000/docs

