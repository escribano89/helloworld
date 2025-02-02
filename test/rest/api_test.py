import http.client
import urllib
import unittest
from urllib.request import urlopen

import pytest

BASE_URL = "http://localhost:5001"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(response.read().decode(), "3", "ERROR ADD")

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(response.read().decode(), "8", "ERROR SQRT")

    def test_api_multiply(self):
        url = f"{BASE_URL}/calc/multiply/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(response.read().decode(), "6", "ERROR MULTIPLY")

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/6/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(response.read().decode(), "2.0", "ERROR DIVIDE")

    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/6/0"
        try:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        except urllib.error.HTTPError as e:
            self.assertEqual(
                e.code,
                http.client.NOT_ACCEPTABLE,
                f"No se puede dividir por cero {url}",
            )
            return

        self.fail("Expected status 406")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
