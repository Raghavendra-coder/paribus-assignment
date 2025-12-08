from unittest.mock import Mock, patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


def _mock_response(status_code=201, ok=True, json_data=None, text=''):
    mock = Mock()
    mock.status_code = status_code
    mock.ok = ok
    mock.text = text
    mock.json = Mock(return_value=json_data or {'id': 1})
    return mock


class BulkHospitalTests(TestCase):

    def _csv_upload(self, rows):
        payload = 'name,address,phone\n' + '\n'.join(rows)
        return SimpleUploadedFile('hospitals.csv', payload.encode('utf-8'), content_type='text/csv')

    @patch('bulk.views.requests.patch')
    @patch('bulk.views.requests.post')
    def test_bulk_create_successfully_activates(self, mock_post, mock_patch):
        mock_post.side_effect = [_mock_response(json_data={'id': 101}), _mock_response(json_data={'id': 102})]
        mock_patch.return_value = _mock_response()

        response = self.client.post('/hospitals/bulk', {'file': self._csv_upload(['General Hospital,123 Main St,555-1234', 'Eastside Care,456 Elm St,'])})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['batch_activated'])
        self.assertEqual(data['failed_hospitals'], 0)
        self.assertEqual(len(data['hospitals']), 2)
        self.assertEqual(data['hospitals'][0]['status'], 'created_and_activated')
        self.assertEqual(data['hospitals'][1]['status'], 'created_and_activated')
        mock_patch.assert_called_once()

    @patch('bulk.views.requests.patch')
    @patch('bulk.views.requests.post')
    def test_bulk_create_skips_activation_on_failure(self, mock_post, mock_patch):
        mock_post.side_effect = [_mock_response(json_data={'id': 101}), _mock_response(ok=False, status_code=400, text='bad request')]

        response = self.client.post('/hospitals/bulk', {'file': self._csv_upload(['General Hospital,123 Main St,555-1234', 'Incomplete,,'])})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['batch_activated'])
        self.assertEqual(data['failed_hospitals'], 1)
        self.assertEqual(len(data['hospitals']), 2)
        self.assertEqual(data['hospitals'][1]['status'], 'failed')
        mock_patch.assert_not_called()
