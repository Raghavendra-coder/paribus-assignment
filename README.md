# Hospital Bulk Creation API

A Django-based web application that provides a bulk hospital creation interface. This service allows users to create multiple hospitals at once by sending JSON data to an external hospital directory API.

## 🚀 Features

- **Web Interface**: User-friendly web form for bulk hospital creation
- **REST API**: JSON-based bulk creation endpoint
- **External API Integration**: Integrates with hospital-directory.onrender.com API
- **Docker Support**: Containerized deployment with Docker Compose
- **Development Ready**: Django development server setup

## 📋 Prerequisites

- Python 3.9+
- pip (Python package manager)
- Docker & Docker Compose (for containerized deployment)

## 🛠️ Installation & Setup

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd paribus
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env file with your configuration
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Web interface: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin/`

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Secret Key (change this in production!)
DJANGO_SECRET_KEY=your-secret-key-here

# Debug mode (set to 0 in production)
DJANGO_DEBUG=1

# External Hospital API Base URL
HOSPITAL_API_BASE_URL=https://hospital-directory.onrender.com
```

### Default Configuration

- **Database**: SQLite (db.sqlite3)
- **Debug Mode**: Enabled by default
- **Allowed Hosts**: All hosts in debug mode
- **External API**: hospital-directory.onrender.com

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000 (development)
http://localhost:8000 (Docker)
```

---

## 🚀 API Endpoints

### 1. Bulk Hospital Creation Form

**Endpoint:** `GET /hospitals/bulk`

**Method:** `GET`

**Description:** Returns the HTML form for bulk hospital creation.

**Payload:** None

**Response:**
- **Status Code:** `200 OK`
- **Content-Type:** `text/html`
- **Body:** HTML form with textarea for hospital data input

---

### 2. Bulk Hospital Creation (API)

**Endpoint:** `POST /hospitals/bulk`

**Method:** `POST`

**Description:** Creates multiple hospitals in bulk by forwarding the data to an external hospital directory API.

**Payload:**
- **Content-Type:** `application/x-www-form-urlencoded`
- **Required Parameters:**
  - `hospitals_data` (string): JSON string containing an array of hospital objects

**Payload Example:**
```form-data
hospitals_data=[
  {
    "name": "General Hospital",
    "address": "123 Main St, City, State",
    "phone": "+1-555-0123",
    "email": "info@generalhospital.com"
  },
  {
    "name": "City Medical Center",
    "address": "456 Health Ave, City, State",
    "phone": "+1-555-0456",
    "email": "contact@citymedical.com"
  }
]
```

**Success Response (200 OK):**
```json
{
  "results": [
    {
      "success": true,
      "data": {
        "id": 1,
        "name": "General Hospital",
        "address": "123 Main St, City, State",
        "phone": "+1-555-0123",
        "email": "info@generalhospital.com",
        "created_at": "2024-01-12T10:30:00Z"
      }
    },
    {
      "success": true,
      "data": {
        "id": 2,
        "name": "City Medical Center",
        "address": "456 Health Ave, City, State",
        "phone": "+1-555-0456",
        "email": "contact@citymedical.com",
        "created_at": "2024-01-12T10:30:00Z"
      }
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "No hospital data provided"
}
```

**Error Response (400 Bad Request - Invalid JSON):**
```json
{
  "error": "Invalid JSON data"
}
```

**Partial Success Response (200 OK):**
```json
{
  "results": [
    {
      "success": true,
      "data": {
        "id": 1,
        "name": "General Hospital",
        "created_at": "2024-01-12T10:30:00Z"
      }
    },
    {
      "success": false,
      "error": "{\"name\":[\"This field may not be blank.\"]}"
    }
  ]
}
```

**Error Codes:**
- `200 OK`: Request processed (check results array for individual outcomes)
- `400 Bad Request`: Missing or invalid hospitals_data parameter
- `500 Internal Server Error`: External API communication error

---

### 3. Django Admin Interface

**Endpoint:** `GET /admin/`

**Method:** `GET`

**Description:** Django admin interface for database management.

**Payload:** None

**Authentication:** Requires superuser credentials

**Response:**
- **Status Code:** `200 OK` (if authenticated) or `302 Found` (redirect to login)
- **Content-Type:** `text/html`
- **Body:** Django admin HTML interface

---

### 4. Django Admin Login

**Endpoint:** `POST /admin/login/`

**Method:** `POST`

**Description:** Authenticates admin users for Django admin access.

**Payload:**
- **Content-Type:** `application/x-www-form-urlencoded`
- **Parameters:**
  - `username` (string, required)
  - `password` (string, required)
  - `csrfmiddlewaretoken` (string, required)

**Success Response (302 Found):**
- Redirects to `/admin/` with authentication cookie

**Error Response (200 OK):**
- Returns login form with error message

---

## 📋 Hospital Data Structure

Each hospital object in the `hospitals_data` array should contain:

```json
{
  "name": "string (required)",
  "address": "string (optional)",
  "phone": "string (optional)",
  "email": "string (optional)"
}
```

**Field Requirements:**
- `name`: Required field, must be unique
- `address`: Optional field for hospital location
- `phone`: Optional field for contact number
- `email`: Optional field for contact email

---

## 🧪 API Testing Examples

### Using cURL

```bash
# Get the bulk creation form
curl -X GET http://127.0.0.1:8000/hospitals/bulk

# Create hospitals in bulk
curl -X POST http://127.0.0.1:8000/hospitals/bulk \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'hospitals_data=[{"name":"Test Hospital","address":"123 Test St"}]'
```

### Using Python

```python
import requests

# Get form
response = requests.get("http://127.0.0.1:8000/hospitals/bulk")
print(response.text)

# Create hospitals
url = "http://127.0.0.1:8000/hospitals/bulk"
data = {
    "hospitals_data": '''[
        {"name": "Test Hospital", "address": "123 Test St"},
        {"name": "Another Hospital", "address": "456 Another St"}
    ]'''
}

response = requests.post(url, data=data)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
// Get form
fetch('/hospitals/bulk')
  .then(response => response.text())
  .then(html => console.log(html));

// Create hospitals
const formData = new FormData();
formData.append('hospitals_data', JSON.stringify([
  { name: "Test Hospital", address: "123 Test St" }
]));

fetch('/hospitals/bulk', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Hospital Data Structure

Each hospital object should contain the following fields (as expected by the external API):

```json
{
  "name": "string (required)",
  "address": "string (optional)",
  "phone": "string (optional)",
  "email": "string (optional)"
}
```

## 🧪 Testing the API

### Using cURL

```bash
# Test the bulk creation endpoint
curl -X POST http://127.0.0.1:8000/hospitals/bulk \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'hospitals_data=[{"name":"Test Hospital","address":"123 Test St"}]'
```

### Using Python

```python
import requests

url = "http://127.0.0.1:8000/hospitals/bulk"
data = {
    "hospitals_data": '''[
        {"name": "Test Hospital", "address": "123 Test St"}
    ]'''
}

response = requests.post(url, data=data)
print(response.json())
```

## 🏗️ Project Structure

```
paribus/
├── bulk/                    # Main Django app
│   ├── templates/
│   │   └── bulk_create.html # Web interface template
│   ├── urls.py             # App URL configuration
│   ├── views.py            # API view logic
│   ├── models.py           # Database models
│   └── apps.py             # App configuration
├── hospital_bulk/          # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL routing
│   └── wsgi.py             # WSGI configuration
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container config
├── docker-compose.yml     # Docker Compose setup
├── manage.py              # Django management script
├── .env                   # Environment variables
└── README.md              # This file
```

## 🚀 Deployment

### Production Deployment

1. **Set environment variables for production:**
   ```env
   DJANGO_DEBUG=0
   DJANGO_SECRET_KEY=your-production-secret-key
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn hospital_bulk.wsgi:application --bind 0.0.0.0:8000
   ```

3. **Using Docker Compose:**
   ```bash
   docker-compose up -d
   ```

### Environment-Specific Settings

- **Development**: Debug enabled, all hosts allowed
- **Production**: Debug disabled, secure settings recommended

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **"No module named 'hospital_bulk.settings'"**
   - Ensure you're in the project root directory
   - Check that `settings.py` exists in `hospital_bulk/`

2. **"Connection refused" to external API**
   - Verify `HOSPITAL_API_BASE_URL` in `.env`
   - Check network connectivity

3. **Database errors**
   - Run `python manage.py migrate`
   - Ensure database file permissions are correct

### Logs

Check Django logs for detailed error information:
```bash
python manage.py runserver --verbosity=2
```

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the API documentation
