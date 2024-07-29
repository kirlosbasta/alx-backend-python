#!/usr/bin/env python3
'''
Unittest for client.py
'''
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Mapping, Sequence, Any, Dict
from client import get_json, memoize, GithubOrgClient
from fixtures import TEST_PAYLOAD


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict, license: str,
                         expected: bool) -> None:
        '''should return true if has license false otherwise'''
        test = GithubOrgClient('test')
        result = test.has_license(repo, license)
        self.assertEqual(result, expected)


@parameterized_class([{
    'org_payload': TEST_PAYLOAD[0][0],
    'repos_payload': TEST_PAYLOAD[0][1],
    'expected_repos': TEST_PAYLOAD[0][2],
    'apache2_repos': TEST_PAYLOAD[0][3]
}])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''Integration test for puplic_repos method'''
    @classmethod
    def setUpClass(cls) -> None:
        '''setup the patcher'''
        repos = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload
        }

        def payload(url: str) -> Mock:
            '''return a mock'''
            return Mock(**{'json.return_value': repos.get(url)})

        cls.get_patcher = patch('requests.get', side_effect=payload)
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls) -> None:
        '''TearDown class'''
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Tests the public_repos method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the public_repos method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )
