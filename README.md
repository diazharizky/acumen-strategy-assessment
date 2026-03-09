# Acumen Strategy Assessment - Backend Engineer

A microservices-based data pipeline application that demonstrates best practices for data ingestion, storage, and retrieval. This project was built as a response to Acumen Strategy's backend engineer assessment.

## Project Overview

This application consists of two main services:

1. **Mock Server** - A Flask-based API that serves mock customer data
2. **Pipeline Service** - A FastAPI-based service that ingests data from the mock server and stores it in PostgreSQL

### Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     Docker Compose Network                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ PostgreSQL   │    │ Mock Server  │    │   Pipeline   │   │
│  │ (Port: N/A)  │◄───│ (Port: 5000) │◄───│   Service    │   │
│  │              │    │              │    │ (Port: 8000) │   │
│  └──────────────┘    └──────────────┘    └──────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Features

### Mock Server

- RESTful API serving customer data from `mock-server/data/customers.json`
- Health check endpoint for orchestration
- Pagination support for customer data retrieval
- Flask-based lightweight HTTP server

### Pipeline Service

- **Data Ingestion**: Pulls customer data from the mock server using `dlt` (data load tool)
- **Data Transformation**: Merges new data with existing records based on `customer_id` primary key
- **Database Storage**: Stores customer data in PostgreSQL
- **Customer Retrieval APIs**:
  - `POST /api/ingest` - Trigger customer data ingestion
  - `GET /api/customers` - Retrieve paginated customer list
  - `GET /api/customers/{customer_id}` - Retrieve specific customer details

## Technology Stack

- **Backend Frameworks**: FastAPI, Flask
- **Database**: PostgreSQL 15
- **Data Pipeline**: dlt (data load tool) with REST API integration
- **ORM**: SQLAlchemy
- **Containerization**: Docker & Docker Compose
- **Python Version**: 3.10+

## Prerequisites

- Docker & Docker Compose
- Python 3.10+ (if running locally)
- `.env` file with database configuration

## Getting Started

### Using Docker Compose (Recommended)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd acumen-strategy-assessment
   ```

2. **Create a `.env` file**

   ```bash
   cp .env.example .env  # or create it manually
   ```

   Configure the following variables:

   ```bash
   DB_USER=postgres
   DB_PASSWORD=your_secure_password
   DB_NAME=acumen_db
   MOCK_SERVER_URL=http://mock_server:5000
   DATABASE_URL=postgresql://DB_USER:DB_PASSWORD@postgres:5432/DB_NAME
   ```

3. **Start the services**

   ```bash
   docker-compose up --build
   ```

   The services will be available at:
   - **Mock Server**: `http://localhost:5000`
   - **Pipeline Service**: `http://localhost:8000`

4. **Verify services are running**

   ```bash
   curl http://localhost:5000/api/health
   curl http://localhost:8000/api/customers
   ```

### Local Development (Optional)

1. **Set up virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install pipeline service dependencies**

   ```bash
   cd pipeline-service
   pip install -r requirements.txt
   cd ..
   ```

3. **Install mock server dependencies**

   ```bash
   cd mock-server
   pip install -r requirements.txt
   cd ..
   ```

4. **Start PostgreSQL** (via Docker or local installation)

5. **Run services individually**

   ```bash
   # Terminal 1: Mock Server
   cd mock-server
   python app.py

   # Terminal 2: Pipeline Service
   cd pipeline-service
   python main.py
   ```

## API Endpoints

### Mock Server (Port: 5000)

| Method | Endpoint | Description | Query Params |
| ------ | -------- | ----------- | ------------ |
| GET | `/api/health` | Health check | - |
| GET | `/api/customers` | Get paginated customer list | `page`, `limit` |
| GET | `/api/customers/{customer_id}` | Get specific customer by ID | - |

#### Detailed Endpoint Information

**GET `/api/health`**

- Health check endpoint for orchestration and monitoring
- No parameters required
- Returns status of the mock server

**GET `/api/customers`**

- Retrieves a paginated list of all customers
- Query Parameters:
  - `page`: Page number (default: 1, must be >= 1)
  - `limit`: Number of records per page (default: 10, no upper limit enforced)
- Returns paginated data with total count

**GET `/api/customers/{customer_id}`**

- Retrieves details for a specific customer
- Path Parameters:
  - `customer_id`: Unique identifier for the customer (required)
- Returns customer object if found, 404 error otherwise

### Pipeline Service (Port: 8000)

| Method | Endpoint | Description | Query Params |
| ------ | -------- | ----------- | ------------ |
| POST | `/api/ingest` | Trigger data ingestion | - |
| GET | `/api/customers` | Get customers from DB | `page` (1+), `limit` (1-25) |
| GET | `/api/customers/{customer_id}` | Get customer by ID | - |

## Example Usage

### Trigger Data Ingestion

```bash
curl -X POST http://localhost:8000/api/ingest
```

Response:

```json
{
  "status": "success",
  "records_processed": 100
}
```

### Retrieve Customers

```bash
curl "http://localhost:8000/api/customers?page=1&limit=10"
```

Response:

```json
{
  "data": [
    {
      "customer_id": "C001",
      "name": "John Doe"
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 10
}
```

### Retrieve Specific Customer

```bash
curl http://localhost:8000/api/customers/C001
```

## Project Structure

```text
acumen-strategy-assessment/
├── docker-compose.yml          # Docker Compose configuration
├── .env                        # Environment variables (create manually)
├── README.md                   # This file
│
├── mock-server/                # Mock Server Service
│   ├── app.py                 # Flask application
│   ├── Dockerfile             # Container configuration
│   ├── requirements.txt        # Python dependencies
│   ├── requirements.in         # Pip-compile source file
│   └── data/
│       └── customers.json      # Mock customer data
│
└── pipeline-service/           # Pipeline Service
    ├── main.py                # FastAPI application
    ├── database.py            # Database configuration & session management
    ├── Dockerfile             # Container configuration
    ├── requirements.txt        # Python dependencies
    ├── requirements.in         # Pip-compile source file
    └── models/
        └── customer.py        # SQLAlchemy Customer model
    └── services/
        └── ingestion.py       # Data ingestion logic using dlt
```

## Database Schema

### Customers Table

The application automatically creates and manages the `customers` table in PostgreSQL with the following structure:

- `customer_id` (Primary Key)
- `name`
- `email`
- `phone`
- `created_at`
- `updated_at`
- (Additional fields as defined in the data model)

## Environment Variables

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `secure_password` |
| `DB_NAME` | Database name | `acumen_db` |
| `DATABASE_URL` | Full database connection string | `postgresql://user:pass@postgres:5432/db` |
| `MOCK_SERVER_URL` | Mock server base URL | `http://mock_server:5000` |

## Health Checks

The Docker Compose configuration includes health checks for all services:

- **PostgreSQL**: Verifies database connectivity via `pg_isready`
- **Mock Server**: Checks `/api/health` endpoint
- **Pipeline Service**: Depends on mock server and PostgreSQL health

Services only start when their dependencies are healthy.

## Error Handling

- **404 Not Found**: Returned when customer ID doesn't exist in the database
- **Validation Errors**: Returned for invalid query parameters (e.g., page < 1, limit > 25)
- **Database Connection Errors**: Service will retry based on Docker restart policy

## Development Notes

- Mock server data is loaded into memory on startup for performance
- Pipeline service uses SQLAlchemy ORM for type-safe database operations
- Data ingestion uses `dlt` library for robust ETL operations with automatic schema detection
- FastAPI automatically generates interactive API documentation at `/docs` (Swagger UI)

## Troubleshooting

### Services not starting

```bash
# Check logs for all services
docker-compose logs -f

# Check specific service
docker-compose logs -f pipeline_service
```

### Database connection issues

- Verify `.env` file exists and has correct credentials
- Ensure PostgreSQL container is healthy: `docker-compose ps`
- Check `DATABASE_URL` format matches PostgreSQL connection string

### Port conflicts

If ports 5000 or 8000 are already in use, modify `docker-compose.yml`:

```yaml
mock_server:
  ports:
    - "5001:5000"  # Changed from 5000:5000

pipeline_service:
  ports:
    - "8001:8000"  # Changed from 8000:8000
```

## License

This project was created as an assessment submission for Acumen Strategy.
