# -*- coding: utf-8 -*-
import pandas as pd
import unittest
import unittest.mock as mock

from turon import Turon, Query


MOCK_GET_USER_BY_ID = {
    'id': '12345',
    'name': 'John Doe',
    'created': '2023-10-31',
}


class TestTuronClient(unittest.TestCase):
    def setUp(self):
        self.client = Turon('meowmeowmeow', 'woofwoofwoof')

    def test_session_headers(self):
        self.assertEqual(self.client.session.headers, {
            'TURON-APP-KEY': 'meowmeowmeow',
            'TURON-API-KEY': 'woofwoofwoof',
        })

    def test_session_base_url(self):
        self.assertEqual(self.client.session.base_url, 'https://pylon.turon.io')

    def test_get(self):
        query = self.client.get('GetUserById', id='12345')
        self.assertTrue(isinstance(query, Query))


class TestTuronQuery(unittest.TestCase):
    def setUp(self):
        self.client = Turon('meowmeowmeow', 'woofwoofwoof')
        self.query = self.client.get('GetUserById', id='12345')

    @mock.patch.object(Query, 'get_data')
    def test_to_dict(self, mock_get_data):
        mock_get_data.return_value = MOCK_GET_USER_BY_ID

        data = self.query.to_dict()

        self.assertEqual(data, {
            'id': '12345',
            'name': 'John Doe',
            'created': '2023-10-31',
        })

    @mock.patch.object(Query, 'get_data')
    def test_to_tuple(self, mock_get_data):
        mock_get_data.return_value = MOCK_GET_USER_BY_ID

        data = self.query.to_tuple()

        self.assertEqual(data, ('12345', 'John Doe', '2023-10-31'))

    @mock.patch.object(Query, 'get_data')
    def test_to_pandas(self, mock_get_data):
        mock_get_data.return_value = MOCK_GET_USER_BY_ID

        data = self.query.to_pandas()

        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertTrue(len(data) == 1)

    @mock.patch.object(Query, 'do_request')
    def test_get_data(self, mock_do_request):
        mock_do_request.side_effect = [
            {'data': [{'id': 1}, {'id': 2}], 'end_cursor': 'dummy', 'has_next_page': True},
            {'data': [{'id': 3}, {'id': 4}], 'end_cursor': 'dummy', 'has_next_page': True},
            {'data': [{'id': 5}, {'id': 6}], 'end_cursor': 'dummy', 'has_next_page': False},
        ]

        data = self.query.to_dict()

        self.assertEqual(data, [
            {'id': 1},
            {'id': 2},
            {'id': 3},
            {'id': 4},
            {'id': 5},
            {'id': 6},
        ])


if __name__ == '__main__':
    unittest.main()
