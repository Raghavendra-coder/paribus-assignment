# Hospital Bulk Processing Service

This Django service wraps the external Hospital Directory API and exposes a single CSV upload endpoint that:

- Validates and limits uploads to 20 hospitals.
- Assigns a unique batch ID to each upload.
- Creates hospitals one-by-one via `POST /hospitals/` on the upstream service.
- Activates the entire batch once every hospital has been created successfully.
- Returns a detailed report with row-level success/failure information.

## Running locally

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Export or copy `env.example` to `.env` and adjust the values as needed. The key environment variables are:

   - `HOSPITAL_API_BASE_URL`: Base URL of the deployed Hospital Directory API (defaults to `https://hospital-directory.onrender.com`).
   - `DJANGO_DEBUG`: `1` to enable debug mode.
   - `DJANGO_SECRET_KEY`: Any secret key for Django.

3. Run Django’s migrations (no models yet, but it is good practice):

   ```bash
   python manage.py migrate
   ```

4. Start the development server:

   ```bash
   python manage.py runserver
   ```

5. POST a multipart file to `/hospitals/bulk` under the field `file`. The CSV must have the headers `name,address,phone` (phone is optional).

## Testing

```bash
python manage.py test
```

## Docker

Build and run the container with:

```bash
docker build -t hospital-bulk .
docker run -p 8000:8000 --env HOSPITAL_API_BASE_URL=https://hospital-directory.onrender.com hospital-bulk
```

Or use `docker-compose up --build`.

## Endpoint behavior

- The response mirrors the Hospital Directory API’s `batch_id` and provides `total_hospitals`, `processed_hospitals`, `failed_hospitals`, and `processing_time_seconds`.
- Each CSV row returns a status of `created_and_activated`, `created`, or `failed` along with row-specific errors.
- If activation fails after creation, the response includes `activation_error` and leaves records in `created` status.

## Notes

- The CSV reader is forgiving about whitespace and will treat `phone` as optional.
- Activation only proceeds when every row has been persisted without upstream errors.
