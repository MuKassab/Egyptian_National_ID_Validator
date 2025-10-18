# Egyptian National ID Validator

A Django REST API service for validating and extracting data from Egyptian National ID numbers. This project provides comprehensive validation and data extraction capabilities for Egyptian National IDs, including birth date, gender, governorate, and age calculation.

## Features

- **National ID Validation**: Validates Egyptian National ID numbers using checksum algorithm
- **Data Extraction**: Extracts personal information from valid National IDs including:
  - Birth date and age calculation
  - Gender identification
  - Birth governorate
- **RESTful API**: Clean REST API endpoints for easy integration
- **Error Handling**: Comprehensive error handling with detailed validation messages
- **Django Integration**: Built with Django and Django REST Framework

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

## Installation

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

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
├── national_id/                             # Main application
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
├── manage.py
└── db.sqlite3                               # SQLite database
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

## Error Handling

The API provides detailed error messages for various validation failures:

- `"National ID must contain digits only."`
- `"National ID must be exactly 14 digits long."`
- `"National ID must start with 2 or 3."`
- `"Invalid governorate code"`
- `"Birth date is in the future"`
- `"Invalid birth date"`
- `"Invalid check digit"`
- `"Unexpected error"`
