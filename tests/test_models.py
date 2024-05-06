import unittest
from datetime import date
from uuid import uuid4, UUID

from models import Pessoa, init_session, db_session


class TestPessoa(unittest.TestCase):
    @init_session
    def setUp(self):
        boxias = Pessoa(
            id=UUID("3c4044be-491c-4fde-be7f-394901d3ca75"),
            apelido="Boxias",
            nome="Isabelly Daniela Nogueira",
            nascimento=date(1986, 1, 23),
            stack="{Toceor,Elxies}",
        )

        xoxoyr = Pessoa(
            id=UUID("a4043fb9-e145-428b-adf6-75177d31b160"),
            apelido="Xoxoyr",
            nome="Andreia Kamilly Luzia Fogaça",
            nascimento=date(1986, 1, 23),
            stack="{Diewuo,Buakiu,Boirbi}",
        )

        tasais = Pessoa(
            id=UUID("a16d8738-6cf2-48a4-a720-b634230d941d"),
            apelido="Tasais",
            nome="Luan Nelson Ian Moreira",
            nascimento=date(1986, 1, 23),
            stack="{Weygel,Dyarou,Hozalu,Boirbi}",
        )

        db_session.get().add(boxias)
        db_session.get().add(xoxoyr)
        db_session.get().add(tasais)
        db_session.get().commit()

    @init_session
    def tearDown(self):
        db_session.get().query(Pessoa).delete()
        db_session.get().commit()

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
