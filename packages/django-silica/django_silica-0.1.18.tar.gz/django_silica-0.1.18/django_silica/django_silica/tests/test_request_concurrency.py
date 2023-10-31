import logging
import os
import time

from django.test import override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import path

from selenium import webdriver
from selenium.webdriver.common.by import By

from django_silica.tests.SilicaTestCase import SilicaStaticLiveServerTestCase
from django_silica.silica.tests.ConcurrencyTest import ConcurrencyTest
from django_silica.urls import urlpatterns as silica_urlpatterns

urlpatterns = silica_urlpatterns + [
    path("silica/tests/concurrency", ConcurrencyTest.as_view()),
]

class ConcurrencyTestCase(SilicaStaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = webdriver.ChromeOptions()
        options.add_argument('--log-level=DEBUG')
        options.add_argument("--headless")
        options.add_argument("--remote-debugging-pipe")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = '/usr/bin/chromium'

        # service = webdriver.ChromeService(log_output=subprocess.STDOUT, service_args=['--verbose'])
        cls.selenium = webdriver.Chrome(options)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
        pass

    def test_a_slower_earlier_request_doesnt_overwrite_a_later_quicker_request(self):
        # Navigate to the page
        self.selenium.get(self.live_server_url + '/silica/tests/concurrency')

        # Trigger the first request
        self.selenium.find_element(By.ID, 'slow_request_first').click()

        # Without waiting, trigger the second request
        self.selenium.find_element(By.ID, 'quick_request_second').click()

        # Give time for the requests to complete
        time.sleep(3)

        # Wait for a UI element that gets updated by the responses
        updated_element = self.selenium.find_element(By.ID, 'updated_element')

        # NOTE: There is a "wait" method from Selenium too

        # Check that the updated_element contains data from the 2nd request ONLY.
        self.assertNotIn('data_from_request_1', updated_element.text)
        self.assertIn('data_from_request_2', updated_element.text)