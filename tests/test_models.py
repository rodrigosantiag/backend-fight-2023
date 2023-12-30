import unittest
from datetime import date
from uuid import uuid4

from sqlalchemy.orm import Session

from database import engine
from models import Pessoa


class TestPessoa(unittest.TestCase):
    def test_create_pessoa(self):
        with Session(engine) as session:
            person_1 = Pessoa(
                id=uuid4(),
                apelido="person_1",
                nome="Person 1",
                nascimento=date(1986, 1, 23),
                stack="python,ruby",
            )

            session.add(person_1)
            session.commit()

            person_id = person_1.id

        with Session(engine) as session2:
            person = session2.get(Pessoa, person_id)

            self.assertEqual(person.id, person_id)
            self.assertEqual(person.apelido, "person_1")
            self.assertEqual(person.nome, "Person 1")
            self.assertEqual(str(person.nascimento), "1986-01-23")
            self.assertEqual(person.stack, "python,ruby")
