#!/usr/bin/env python3
'''
Unittest for client.py
'''
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from client import get_json, memoize, GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''Test github org client'''

    @parameterized.expand(['google', 'abc'])
    @patch('client.get_json')
    def test_org(self, org: str, mock_get_json) -> None:
        '''test that org return the expected result'''
        url = "https://api.github.com/orgs/{org}".format(org=org)
        org_client = GithubOrgClient(org)
        org_client.org()
        mock_get_json.assert_called_once_with(url)

    def test_public_repos_url(self):
        """ Test that the result of _public_repos_url is the expected one
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payload = {"repos_url": "World"}
            mock.return_value = payload
            test_class = GithubOrgClient('test')
            result = test_class._public_repos_url
            self.assertEqual(result, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        '''should return list of repos name as expected'''
        mock_get_json.return_value = [
            {
                'name': 'python',
                'license': {'key': 'hello'}
            },
            {
                'name': 'js',
                'license': {'key': 'world'}
            },
            {
                'name': 'php',
                'license': {'key': 'hello'}
            }
        ]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'something not important'
            test = GithubOrgClient('test')
            result = test.public_repos('hello')
            self.assertEqual(result, ['python', 'php'])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()
