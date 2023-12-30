import unittest
from datetime import date

from schemas import PessoaSchema
from pydantic import ValidationError


class TestPessoaSchema(unittest.TestCase):
    def test_valid(self):
        pessoa = PessoaSchema(
            apelido="foobar", nome="Foo Bar", nascimento="1986-01-23", stack=["C", "Ruby", "Python"]
        )

        self.assertEqual(pessoa.apelido, "foobar")
        self.assertEqual(pessoa.nome, "Foo Bar")
        self.assertEqual(pessoa.nascimento, date(1986, 1, 23))
        self.assertListEqual(pessoa.stack, ["C", "Ruby", "Python"])

    def test_valid_without_stack(self):
        pessoa = PessoaSchema(apelido="foobar", nome="Foo Bar", nascimento="1986-01-23")

        self.assertEqual(pessoa.apelido, "foobar")
        self.assertEqual(pessoa.nome, "Foo Bar")
        self.assertEqual(pessoa.nascimento, date(1986, 1, 23))
        self.assertIsNone(pessoa.stack)

    def test_invalid_missing_apelido(self):
        with self.assertRaises(ValidationError):
            PessoaSchema(nome="Foo Bar", nascimento="1986-01-23", stack=["C", "Ruby", "Python"])

    def test_invalid_missing_nome(self):
        with self.assertRaises(ValidationError):
            PessoaSchema(apelido="FooBar", nascimento="1986-01-23", stack=["C", "Ruby", "Python"])

    def test_invalid_missing_nascimento(self):
        with self.assertRaises(ValidationError):
            PessoaSchema(apelido="FooBar", nome="Foo Bar", stack=["C", "Ruby", "Python"])

    def test_invalid_nascimento(self):
        with self.assertRaises(ValidationError):
            PessoaSchema(
                apelido="FooBar",
                nome="Foo Bar",
                nascimento="1976-02-31",
                stack=["C", "Ruby", "Python"],
            )

    def test_invalid_stack(self):
        with self.assertRaises(ValidationError):
            PessoaSchema(
                apelido="FooBar",
                nome="Foo Bar",
                nascimento="1976-02-20",
                stack=["C", "Ruby", "Python342534t3rgergegertgter455tfhnftrhh"],
            )

    def test_invalid_stack_integer(self):
        with self.assertRaises(ValidationError):
            PessoaSchema(
                apelido="FooBar", nome="Foo Bar", nascimento="1976-02-20", stack=[1, "Ruby"]
            )
