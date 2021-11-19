from flask import url_for, redirect
from flask_testing import TestCase
from application import app



class TestBase(TestCase):
    def create_app(self):
        return app

class TestResponse(TestBase):
    def test_keypair_engine(self):
        response = self.client.get(url_for('keys_generator'))
        assert len(response.data) > 2

    # def test_keypair_gen(self):
    #     response = self.client.get('http://keypair-generator:5001/keys_generator')
    #     assert response.status_code == 200
# #         # output = response.data.decode('utf-8')
# #         # assert output in ['a','b','c','d','e']


# # class route_testing(TestBase):
# #     def test_home(self):
# #         response = self.client.get('/')
# #         assert response.status_code == 200
# #         assert response.data != ''
