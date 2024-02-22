import unittest
from datetime import date
from http import HTTPStatus

from fastapi.testclient import TestClient

from main import app
from models import Pessoa, init_session, db_session

client = TestClient(app)


class TestMain(unittest.TestCase):
    @init_session
    def setUp(self):
        person = Pessoa(
            apelido="rodrigo",
            nome="Rodrigo",
            nascimento=date(1986, 1, 23),
            stack="python",
        )

        db_session.get().add(person)
        db_session.get().commit()

    @init_session
    def tearDown(self):
        db_session.get().query(Pessoa).delete()
        db_session.get().commit()

    def test_hello_world(self):
        response = client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "world"})

    def test_add_person_success(self):
        payload_1 = {
            "apelido": "josé",
            "nome": "José Roberto",
            "nascimento": "2000-10-01",
            "stack": ["C#", "Node", "Oracle"],
        }

        payload_2 = {
            "apelido": "ana",
            "nome": "Ana Barbosa",
            "nascimento": "1985-09-23",
            "stack": None,
        }
        subtest_params = (payload_1, payload_2)

        for params in subtest_params:
            payload = params

            with self.subTest(payload=payload):
                response = client.post("/pessoas", json=payload)

                self.assertEqual(response.status_code, HTTPStatus.CREATED)
                self.assertIn("/pessoas/", response.headers.get("Location"))
                self.assertIn("uid", response.json())

    def test_add_person_unprocessable_entity(self):
        payloads = [
            {
                "apelido": "rodrigo",
                "nome": "José Roberto",
                "nascimento": "2000-10-01",
                "stack": ["C#", "Node", "Oracle"],
            },
            {"apelido": "ana", "nome": None, "nascimento": "1985-09-23", "stack": None},
            {"apelido": None, "nome": "Ana Barbosa", "nascimento": "1985-01-23", "stack": None},
        ]

        for payload in payloads:
            with self.subTest(payload=payload):
                response = client.post("/pessoas", json=payload)

                self.assertEqual(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
                self.assertIn("errors", response.json())

    def test_add_person_bad_gateway(self):
        payloads = [
            {"apelido": "apelido", "nome": 1, "nascimento": "1985-01-01", "stack": None},
            {"apelido": "apelido", "nome": "nome", "nascimento": "1985-01-01", "stack": [1, "PHP"]},
        ]

        for payload in payloads:
            with self.subTest(payload=payload):
                response = client.post("/pessoas", json=payload)

                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
                self.assertIn("errors", response.json())
