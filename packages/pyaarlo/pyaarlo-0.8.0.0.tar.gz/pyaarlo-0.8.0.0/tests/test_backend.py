from unittest import TestCase
import pyaarlo.backend
import tests.arlo


class TestArloBackEnd(TestCase):
    def test_user_agent(self):
        arlo = tests.arlo.PyArlo()
        be = pyaarlo.ArloBackEnd(arlo)
        print(be.user_agent("linux"))
        self.fail()
