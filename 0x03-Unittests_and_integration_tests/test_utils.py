#!/usr/bin/env python3
'''
0. Parameterize a unit test
'''
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    '''Test accress_nested_map function'''

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: Mapping,
                               path: Sequence, expected: Any) -> None:
        '''should return the expected result'''
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence) -> None:
        '''should raise KeyError'''
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''Test case for get_json'''
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        '''should return the expected result'''
        response_mock = Mock()
        response_mock.json.return_value = test_payload
        with patch('utils.requests') as mock_requests:
            mock_requests.get.return_value = response_mock
            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_requests.get.assert_called_once_with(test_url)
