from django_silica.tests.SilicaTestCase import SilicaTestCase, SilicaTest
from django_silica.silica.tests.JsCalls import JsCalls


class TestJsCalls(SilicaTestCase):
    def test_js_is_called(self):
        (
            SilicaTest(component=JsCalls)
            .call("set_js_call")
            .assertJsCalled("alert", "hi")
        )
