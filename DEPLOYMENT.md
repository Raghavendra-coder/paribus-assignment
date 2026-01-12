# Paribus Hospital Bulk Creation API

**Base URL:** https://paribus.pythonanywhere.com/

**Admin Credentials:**
- Username: `admin@paribus`
- Password: `password`
- Admin URL: https://paribus.pythonanywhere.com/admin

---

## 1. Run on Localhost

### 1.1 Clone Repository
```bash
git clone https://github.com/Raghavendra-coder/paribus-assignment.git
cd paribus-assignment
```

### 1.2 Install Requirements
```bash
pip install -r requirements.txt
```

### 1.3 Run
```bash
python manage.py runserver
```
**Access:** http://127.0.0.1:8000

---

## 2. Run on Deployed

**Deployed URL:** https://paribus.pythonanywhere.com/

**Admin Access:** https://paribus.pythonanywhere.com/admin

---

## 3. List of APIs

### Base URL: https://paribus.pythonanywhere.com/

### 1. GET /hospitals/bulk
- **Method:** GET
- **Payload:** None
- **Response:** HTML form (200 OK)

### 2. POST /hospitals/bulk
- **Method:** POST
- **Payload:** `hospitals_data` (JSON string with hospital array)
- **Response:** JSON results array (200 OK)
- **Example:**
  ```json
  {
    "hospitals_data": "[{\"name\":\"Hospital Name\",\"address\":\"Address\"}]"
  }
  ```

### 3. GET /admin/
- **Method:** GET
- **Payload:** None
- **Response:** Django admin interface (requires authentication)

### Hospital Data Structure:
```json
{
  "name": "string (required)",
  "address": "string (optional)",
  "phone": "string (optional)",
  "email": "string (optional)"
}
```
