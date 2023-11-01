
import pytest
import unittest
import requests
from requests.exceptions import RequestException
from requests_mock import Mocker
from interface import DKANPortalClient  # Annahme: Du importierst deine DKANPortalClient-Klasse aus der entsprechenden Datei

city = "essen"

class TestDKANPortalClient(unittest.TestCase):

    def test_connectiontest(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a successful response
        with Mocker() as m:
            url = f"{client.base_url}/action/site_read"
            m.get(url, json={"result": True})

            # Test the connection
            result = client.connectiontest()
            assert result is True

    def test_connectiontest_failure(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a failed response
        with Mocker() as m:
            url = f"{client.base_url}/action/site_read"
            m.get(url, status_code=404)  # Simulate a 404 error

            # Test the connection failure
            with pytest.raises(RequestException):
                client.connectiontest()


    def test_get_total_packages_with_resources(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a successful response
        with Mocker() as m:
            url = f"{client.base_url}/action/current_package_list_with_resources"
            m.get(url, json={"success": True, "result": [{"package_key": "value"}]})

            # Test the function
            result = client.get_total_packages_with_resources()
            assert isinstance(result, list)
            assert len(result) == 1


    def test_get_total_packages_with_resources_failure(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a failed response
        with Mocker() as m:
            url = f"{client.base_url}/action/current_package_list_with_resources"
            m.get(url, status_code=404)

            # Test the function failure
            with pytest.raises(requests.exceptions.RequestException):
                client.get_total_packages_with_resources()


    def test_get_contributors(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a successful response
        with Mocker() as m:
            url = f"{client.base_url}/action/group_list"
            m.get(url, json={"result": ["contributor1", "contributor2"]})

            # Test the function
            result = client.get_contributors()
            assert isinstance(result, list)
            assert len(result) == 2
            assert result == ["contributor1", "contributor2"]


    def test_get_contributors_failure(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a failed response
        with Mocker() as m:
            url = f"{client.base_url}/action/group_list"
            m.get(url, status_code=404)

            # Test the function failure
            with pytest.raises(requests.exceptions.RequestException):
                client.get_contributors()


    def test_get_packages(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a successful response
        with Mocker() as m:
            url = f"{client.base_url}/action/package_list"
            m.get(url, json={"success": True, "result": [{"package_key": "value"}]})

            # Test the function
            result = client.get_packages()
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["package_key"] == "value"


    def test_get_packages_failure(self):
        client = DKANPortalClient(city)

        # Mocking the requests module to simulate a failed response
        with Mocker() as m:
            url = f"{client.base_url}/action/package_list"
            m.get(url, status_code=404)

            # Test the function failure
            with pytest.raises(requests.exceptions.RequestException):
                client.get_packages()


if __name__ == '__main__':
    unittest.main()