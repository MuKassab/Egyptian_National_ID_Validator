# Egyptian National ID Validator

A Django REST API service for validating and extracting data from Egyptian National ID numbers. This project provides comprehensive validation and data extraction capabilities for Egyptian National IDs, including birth date, gender, governorate, and age calculation. The service also includes a complete API key management system for secure access control.

## Features

### National ID Validation

- **National ID Validation**: Validates Egyptian National ID numbers using checksum algorithm
- **Data Extraction**: Extracts personal information from valid National IDs including:
  - Birth date and age calculation
  - Gender identification
  - Birth governorate

### API Key Management

- **Secure API Key Generation**: Generate cryptographically secure 64-character API keys
- **API Key Verification**: Verify API keys with secure hashing (SHA-512)
- **Usage Tracking**: Track API key usage with detailed analytics
- **Usage Statistics**: Get comprehensive usage statistics including:
  - Total usage count
  - Recent usage (24-hour window)
  - Endpoint breakdown
  - Last usage timestamp

### Rate Limiting

- **API Key Based Rate Limiting**: Rate limiting applied only when API key is present
- **Configurable Limits**: Default 2 requests per minute per API key
- **Sliding Window**: 60-second sliding window for accurate rate limiting
- **Redis Backend**: Uses Redis for fast and scalable rate limiting
- **Automatic Cleanup**: Rate limit data automatically expires after 60 seconds

### Technical Features

- **RESTful API**: Clean REST API endpoints for easy integration
- **Error Handling**: Comprehensive error handling with detailed validation messages
- **Django Integration**: Built with Django and Django REST Framework
- **PostgreSQL Support**: Production-ready database configuration
- **Security**: Secure API key storage with hashing and tracking

## National ID Format

Egyptian National IDs are 14-digit numbers with the following structure:

- **Position 1**: Century indicator (2 for 1900s, 3 for 2000s)
- **Positions 2-3**: Year (last two digits)
- **Positions 4-5**: Month (01-12)
- **Positions 6-7**: Day (01-31)
- **Positions 8-9**: Governorate code
- **Positions 10-13**: Sequential number
- **Position 14**: Check digit

## API Endpoints

### 1. Validate National ID

**POST** `/api/national-id/validate`

Validates whether a National ID is valid.

**Request Body:**

```json
{
  "national_id": "29512301234567"
}
```

**Response:**

```json
{
  "is_valid_national_id": true
}
```

**Error Response:**

```json
{
  "is_valid_national_id": false,
  "reason": "Invalid check digit"
}
```

### 2. Extract Data from National ID

**POST** `/api/national-id/extract-data`

Extracts personal information from a valid National ID.

**Request Body:**

```json
{
  "national_id": "29512301234567"
}
```

**Response:**

```json
{
  "birth_governorate_name": "Cairo",
  "birth_date": "1995-12-30T00:00:00Z",
  "age": "28 years, 10 months, 15 days",
  "gender": "Male"
}
```

**Error Response:**

```json
{
  "is_valid_national_id": false,
  "reason": "Invalid governorate code"
}
```

**Rate Limit Exceeded Response:**

```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 2 requests per minute allowed",
  "retry_after": 45
}
```

## API Key Management Endpoints

### 1. Generate API Key

**POST** `/api/api-keys/generate`

Generates a new 64-character API key for accessing the service.

**Request Body:**

```json
{}
```

**Response:**

```json
{
  "success": true,
  "api_key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2",
  "message": "API key generated successfully"
}
```

### 2. Verify API Key

**POST** `/api/api-keys/verify`

Verifies an API key and returns its status.

**Request Body:**

```json
{
  "api_key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2"
}
```

**Response:**

```json
{
  "valid": true,
  "id": 1,
  "last_usage": "2024-01-15T10:30:00Z"
}
```

**Error Response:**

```json
{
  "valid": false,
  "error": "Invalid API key"
}
```

### 3. Get Usage Statistics

**POST** `/api/api-keys/usage-stats`

Retrieves detailed usage statistics for an API key.

**Request Body:**

```json
{
  "api_key": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2"
}
```

**Response:**

```json
{
  "success": true,
  "api_key_id": 1,
  "total_usage": 150,
  "recent_usage_24h": 25,
  "endpoint_breakdown": {
    "/api/national-id/validate": 80,
    "/api/national-id/extract-data": 70
  },
  "last_usage": "2024-01-15T10:30:00Z",
  "created_at": "2024-01-10T08:00:00Z"
}
```

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)
- Docker (for PostgreSQL database and Redis)
- PostgreSQL client (optional, for direct database access)

### Database Setup

1. **Start PostgreSQL using Docker:**

   ```bash
   docker run --name my_postgres \
     -e POSTGRES_USER=admin \
     -e POSTGRES_PASSWORD=secret123 \
     -e POSTGRES_DB=api_keys_db \
     -p 5432:5432 \
     -d postgres:16
   ```

2. **Start Redis using Docker:**

   ```bash
   docker run -d \
     --name redis \
     -p 6379:6379 \
     redis:latest
   ```

3. **Create environment file:**

   Create a `.env` file in the project root with the following content:

   ```env
   # Database Configuration
   DB_NAME=api_keys_db
   DB_USER=admin
   DB_PASSWORD=secret123
   DB_HOST=localhost
   DB_PORT=5432

   # Redis Configuration
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_DB=0
   REDIS_PASSWORD=
   ```

### Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd Egyptian_National_ID_Validator
   ```

2. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Project Structure

```
Egyptian_National_ID_Validator/
├── Egyptian_National_ID_Validator/          # Django project settings
│   ├── __init__.py
│   ├── settings.py                          # Django settings
│   ├── urls.py                              # Main URL configuration
│   ├── wsgi.py
│   ├── asgi.py
│   └── exceptions.py                        # Custom exception handler
├── core/                                    # Core utilities app
│   ├── helpers/
│   │   └── redis_client.py                  # Redis client configuration
│   ├── decorators/
│   │   └── rate_limiter.py                 # Rate limiting decorator
│   ├── models.py
│   ├── admin.py
│   └── apps.py
├── national_id/                             # National ID validation app
│   ├── constants/
│   │   └── constants.py                     # Governorate codes mapping
│   ├── helpers/
│   │   ├── check_sum.py                     # Checksum validation logic
│   │   └── dates.py                         # Age calculation utilities
│   ├── serializers/
│   │   └── national_id_serializer.py        # Input validation
│   ├── services/
│   │   └── national_id_service.py           # Core business logic
│   ├── views/
│   │   ├── national_id_validation_views.py  # Validation endpoint
│   │   └── national_id_data_extraction_views.py  # Data extraction endpoint
│   ├── models.py
│   ├── urls.py                              # App URL configuration
│   └── admin.py
├── api_keys/                                # API key management app
│   ├── constants/
│   │   └── constants.py                     # API key constants
│   ├── decorators/
│   │   └── api_key_tracker.py              # Usage tracking decorator
│   ├── helpers/
│   │   └── key_generator.py                # API key generation utilities
│   ├── serializers/
│   │   └── api_key_serializer.py           # API key validation
│   ├── services/
│   │   └── api_key_service.py              # API key business logic
│   ├── views/
│   │   ├── api_key_views.py                # API key endpoints
│   │   └── api_key_management_views.py     # Management endpoints
│   ├── tests/
│   │   └── api_creation_tests.py           # API key tests
│   ├── models.py                            # API key models
│   ├── urls.py                              # App URL configuration
│   └── admin.py
├── manage.py
├── requirements.txt                         # Python dependencies
└── .env                                     # Environment variables
```

## Rate Limiting

The API implements rate limiting to prevent abuse and ensure fair usage:

### Features

- **API Key Based**: Rate limiting only applies when an API key is present in the request
- **Per-Key Limits**: Each API key has its own rate limit counter
- **Sliding Window**: Uses a 60-second sliding window for accurate rate limiting
- **Redis Backend**: Uses Redis for fast and scalable rate limiting storage
- **Configurable**: Rate limits can be configured per endpoint (default: 2 requests/minute)

### Rate Limit Response

When rate limit is exceeded, the API returns:

```json
{
  "error": "Rate limit exceeded",
  "message": "Maximum 2 requests per minute allowed",
  "retry_after": 45
}
```

- **Status Code**: 429 (Too Many Requests)
- **retry_after**: Seconds until the rate limit resets

### Configuration

Rate limiting is configured using the `@rate_limit_by_api_key` decorator:

```python
from core.decorators.rate_limiter import rate_limit_by_api_key

@rate_limit_by_api_key(requests_per_minute=2)
def my_view(request):
    # Your view logic here
    pass
```

## API Key Security

The API key system implements several security measures:

- **Cryptographically Secure Generation**: API keys are generated using Python's `secrets` module
- **Secure Storage**: API keys are never stored in plain text; only SHA-512 hashes are stored
- **64-Character Length**: All API keys are exactly 64 alphanumeric characters
- **Usage Tracking**: All API key usage is logged with timestamps and endpoint information
- **Verification**: API keys are verified against stored hashes for authentication

### Using API Keys

To use an API key with the service, include it in the request headers:

```bash
curl -H "X-API-Key: your_api_key_here" \
     -H "Content-Type: application/json" \
     -X POST http://127.0.0.1:8000/api/national-id/validate \
     -d '{"national_id": "29512301234567"}'
```

## Validation Rules

The validator performs the following checks:

1. **Format Validation:**

   - Must be exactly 14 digits
   - Must contain only numeric characters
   - Must start with 2 or 3

2. **Date Validation:**

   - Birth date must be valid (not in the future)
   - Month must be between 01-12
   - Day must be valid for the given month/year

3. **Governorate Validation:**

   - Governorate code must exist in the predefined list

4. **Checksum Validation:**
   - Uses a weighted checksum algorithm to verify the last digit

## Database Models

### ApiKey Model

- `key_hash`: SHA-512 hash of the API key (unique)
- `last_usage`: Timestamp of last API key usage
- `is_active`: Boolean flag for API key status

### ApiKeyUsage Model

- `api_key`: Foreign key to ApiKey model
- `endpoint`: The endpoint that was accessed
- `time_of_usage`: Timestamp when the API key was used

## Error Handling

The API provides detailed error messages for various validation failures:

### National ID Validation Errors

- `"National ID must contain digits only."`
- `"National ID must be exactly 14 digits long."`
- `"National ID must start with 2 or 3."`
- `"Invalid governorate code"`
- `"Birth date is in the future"`
- `"Invalid birth date"`
- `"Invalid check digit"`
- `"Unexpected error"`

### API Key Errors

- `"API key is required"`
- `"API key must be exactly 64 characters long"`
- `"API key must contain only alphanumeric characters"`
- `"Invalid API key"`
- `"API key not found"`
- `"Failed to generate API key"`
- `"Failed to track usage"`

## Testing

The project includes comprehensive tests for API key management:

### Running Tests

```bash
# Run all tests
python manage.py test

python manage.py test api_keys

# Run with verbose output
python manage.py test --verbosity=2
```
