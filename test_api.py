from unittest import TestCase
from finder import create_app
import json


class TestFinder(TestCase):
    client = None

    def setUp(self):
        app = create_app()
        self.client = app.test_client()

    def test_1register(self):
        """
        测试添加微服务地址
        :return:
        """
        resp = self.client.post("register")
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 103)

        data = {
            "field": "2_EMAIL_",
            "value": "http://192.168.1.123:80",
            "force": True
        }
        resp = self.client.post("register", data=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 100)

        data = {
            "field": "F_EMAIL_",
            "value": "http://192.168.1.123:80",
            "force": True
        }
        resp = self.client.post("register", data=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        data = {
            "field": "F_EMAIL_",
            "value": "http://192.168.1.123:80",
            "force": False
        }
        resp = self.client.post("register", data=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 101)
        data = {
            "field": "F_EMAIL_",
            "value": "http://192.168.1.123:80",
            "force": True
        }
        resp = self.client.post("register", data=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)

    def test_2ls(self):
        resp = self.client.get('ls')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        self.assertEqual(len(data['message']), 0)
        data = {
            "field": "F_EMAIL_",
            "value": "http://192.168.1.123:80",
            "force": True
        }
        resp = self.client.post("register", data=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        data = {
            "field": "F_PHONE_",
            "value": "http://192.168.1.123:80",
            "force": True
        }
        resp = self.client.post("register", data=data)
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        resp = self.client.get('ls')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        self.assertEqual(len(data['message']), 0)

        # 测试check
        resp = self.client.get('check')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)

        # 测试get
        resp = self.client.get('/get/{}'.format("F_PHONE_"))
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        self.assertNotEqual(len(data['message']), 0)

        # 测试remove
        resp = self.client.delete('/remove/{}'.format("F_PHONE_"))
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        self.assertEqual(data['message'], 1)

        resp = self.client.get('/get/{}'.format("F_PHONE_"))
        data = json.loads(resp.data.decode())
        self.assertEqual(data['error_code'], 0)
        self.assertEqual(len(data['message']), 0)
