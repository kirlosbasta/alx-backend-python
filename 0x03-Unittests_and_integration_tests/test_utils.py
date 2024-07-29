#!/usr/bin/env python3
'''
0. Parameterize a unit test
'''
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from utils import access_nested_map, get_json, memoize


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


class TestMemoize(unittest.TestCase):
    '''Test memoize decorator'''
    def test_memoize(self) -> None:
        '''should memoize each function call'''
        class TestClass:
            '''Test class'''
            def a_method(self) -> int:
                '''return 42'''
                return 42

            @memoize
            def a_property(self) -> int:
                '''call a_method and remember the result'''
                return self.a_method()

        with patch.object(TestClass, 'a_method') as a_method:
            a_method.return_value = 42
            test = TestClass()
            result1 = test.a_property
            result2 = test.a_property
            a_method.assert_called_once()
        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)
