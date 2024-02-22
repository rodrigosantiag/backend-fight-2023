import unittest
from datetime import date
from uuid import uuid4


from models import Pessoa, init_session, db_session


class TestPessoa(unittest.TestCase):
    @init_session
    def test_create_pessoa(self):
        person_1 = Pessoa(
            id=uuid4(),
            apelido="person_1",
            nome="Person 1",
            nascimento=date(1986, 1, 23),
            stack="python,ruby",
        )

        db_session.get().add(person_1)
        db_session.get().commit()

        person_id = person_1.id

        person = db_session.get().get(Pessoa, person_id)

        self.assertEqual(person.id, person_id)
        self.assertEqual(person.apelido, "person_1")
        self.assertEqual(person.nome, "Person 1")
        self.assertEqual(str(person.nascimento), "1986-01-23")
        self.assertEqual(person.stack, "python,ruby")
