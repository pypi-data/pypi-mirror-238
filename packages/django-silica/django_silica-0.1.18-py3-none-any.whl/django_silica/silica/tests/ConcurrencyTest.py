import time

from django_silica.SilicaComponent import SilicaComponent


class ConcurrencyTest(SilicaComponent):
    ui_value: str = None

    def slow_first(self):
        time.sleep(2)
        self.ui_value = "data_from_request_1"

    def slow_second(self):
        time.sleep(1)
        self.ui_value = "data_from_request_2"

    def inline_template(self):
        # language=HTML
        return """
            <div>
                <button id="slow_request_first" silica:click.prevent="slow_first">Slow</button>
                <button id="quick_request_second" silica:click.prevent="slow_second">Quick</button>
                <div id="updated_element">{{ ui_value }}</div>
            </div>
        """