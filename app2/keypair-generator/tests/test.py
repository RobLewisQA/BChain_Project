from flask import url_for, redirect
from flask_testing import TestCase
from application import app
import json


class TestBase(TestCase):
    def create_app(self):
        return app

# unit tests
## testing length of keypair output is greater than 30
class TestResponse(TestBase):
    def test_keypair_engine(self):
        response = self.client.get(url_for('keys_generator'))
        assert len(response.data.decode('UTF-8')) > 30
        self.assertIn(b'_',response.data)

    def test_keypair_json(self):
        response = self.client.get(url_for('keys_generator'))
        json_output = json.dumps(response.data.decode('UTF-8'))
        self.assertTrue(json_output)
        #assert len(json.loads(json_output)['private_key']) == 64

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
