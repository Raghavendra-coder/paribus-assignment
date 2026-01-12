from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import requests
import os


class BulkHospitalCreateView(TemplateView):
    template_name = 'bulk_create.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Get data from request
        hospitals_data = request.POST.get('hospitals_data', '')

        if not hospitals_data:
            return JsonResponse({'error': 'No hospital data provided'}, status=400)

        # Parse the data (assuming JSON format)
        try:
            import json
            hospitals = json.loads(hospitals_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        # Get API endpoint from environment
        api_base_url = os.getenv('HOSPITAL_API_BASE_URL', 'https://hospital-directory.onrender.com')

        results = []
        for hospital in hospitals:
            try:
                response = requests.post(f"{api_base_url}/api/hospitals/", json=hospital)
                if response.status_code == 201:
                    results.append({'success': True, 'data': response.json()})
                else:
                    results.append({'success': False, 'error': response.text})
            except Exception as e:
                results.append({'success': False, 'error': str(e)})

        return JsonResponse({'results': results})
