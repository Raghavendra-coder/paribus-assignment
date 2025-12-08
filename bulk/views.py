import csv
import io
import uuid
from time import monotonic

import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

MAX_HOSPITALS = 20
REQUIRED_COLUMNS = {'name', 'address'}


@method_decorator(csrf_exempt, name='dispatch')
class BulkHospitalCreateView(View):
    """Handle CSV uploads that create multiple hospitals via the external API."""

    def post(self, request):
        csv_file = request.FILES.get('file') or request.FILES.get('csv')
        if not csv_file:
            return JsonResponse({'error': 'CSV file is required under the "file" field.'}, status=400)

        try:
            payload = csv_file.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            return JsonResponse({'error': 'Unable to decode the uploaded file; ensure it is UTF-8.'}, status=400)

        reader = csv.DictReader(io.StringIO(payload))
        if not reader.fieldnames:
            return JsonResponse({'error': 'CSV file must include headers.'}, status=400)
        supplied_columns = {header.strip().lower() for header in reader.fieldnames}
        if not REQUIRED_COLUMNS.issubset(supplied_columns):
            return JsonResponse(
                {'error': f'CSV must contain headers: {", ".join(sorted(REQUIRED_COLUMNS))}.'},
                status=400,
            )

        rows = list(reader)
        total_hospitals = len(rows)
        if total_hospitals == 0:
            return JsonResponse({'error': 'CSV contained no hospital rows.'}, status=400)
        if total_hospitals > MAX_HOSPITALS:
            return JsonResponse({'error': f'CSV may contain at most {MAX_HOSPITALS} hospitals.'}, status=400)

        batch_id = str(uuid.uuid4())
        processed_hospitals = 0
        failed_hospitals = 0
        successful_hospitals = 0
        hospital_outcomes = []

        start_time = monotonic()

        for idx, raw_row in enumerate(rows, start=1):
            processed_hospitals += 1
            row = {k.strip().lower(): (v or '').strip() for k, v in raw_row.items()}
            name = row.get('name', '')
            address = row.get('address', '')
            phone = row.get('phone', '')

            if not name or not address:
                failed_hospitals += 1
                hospital_outcomes.append({
                    'row': idx,
                    'name': name or '<missing name>',
                    'status': 'failed',
                    'error': 'name and address are required fields',
                })
                continue

            payload = {'name': name, 'address': address, 'creation_batch_id': batch_id}
            if phone:
                payload['phone'] = phone

            try:
                response = requests.post(
                    f"{settings.HOSPITAL_API_BASE_URL}/hospitals/",
                    json=payload,
                    timeout=10,
                )
                if not response.ok:
                    raise RuntimeError(
                        f'API responded {response.status_code}: {response.text.strip()}'
                    )
                hospital_data = response.json()
                hospital_id = hospital_data.get('id')
                successful_hospitals += 1
                hospital_outcomes.append(
                    {
                        'row': idx,
                        'hospital_id': hospital_id,
                        'name': name,
                        'status': 'created',
                    }
                )
            except Exception as exc:
                failed_hospitals += 1
                hospital_outcomes.append(
                    {
                        'row': idx,
                        'name': name,
                        'status': 'failed',
                        'error': str(exc),
                    }
                )

        batch_activated = False
        activation_error = None
        if failed_hospitals == 0 and successful_hospitals > 0:
            try:
                activation_response = requests.patch(
                    f"{settings.HOSPITAL_API_BASE_URL}/hospitals/batch/{batch_id}/activate",
                    timeout=10,
                )
                if activation_response.ok:
                    batch_activated = True
                    for entry in hospital_outcomes:
                        if entry.get('status') == 'created':
                            entry['status'] = 'created_and_activated'
                else:
                    activation_error = (
                        f'Activation failed with {activation_response.status_code}: '
                        f'{activation_response.text.strip()}'
                    )
            except Exception as exc:
                activation_error = str(exc)

        serialized_outcomes = []
        for entry in hospital_outcomes:
            serialized = {
                'row': entry.get('row'),
                'name': entry.get('name'),
                'status': entry.get('status'),
            }
            if 'hospital_id' in entry:
                serialized['hospital_id'] = entry['hospital_id']
            if entry.get('status') == 'failed':
                serialized['error'] = entry.get('error')
            serialized_outcomes.append(serialized)

        processing_time_seconds = round(max(monotonic() - start_time, 0), 2)

        response_payload = {
            'batch_id': batch_id,
            'total_hospitals': total_hospitals,
            'processed_hospitals': processed_hospitals,
            'failed_hospitals': failed_hospitals,
            'processing_time_seconds': processing_time_seconds,
            'batch_activated': batch_activated,
            'hospitals': serialized_outcomes,
        }

        if activation_error:
            response_payload['activation_error'] = activation_error

        return JsonResponse(response_payload)
