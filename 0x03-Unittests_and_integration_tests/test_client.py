#!/usr/bin/env python3
'''
Unittest for client.py
'''
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from client import get_json, memoize, GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    '''Test github org client'''
    @parameterized.expand(['google, abc'])
    @patch('client.get_json')
    def test_org(self, org: str, mock_get_json) -> None:
        '''test that org return the expected result'''
        url = "https://api.github.com/orgs/{org}".format(org=org)
        org_client = GithubOrgClient(org)
        org_client.org()
        mock_get_json.assert_called_once_with(url)
