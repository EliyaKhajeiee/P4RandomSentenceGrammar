import unittest
import file_organizer_py
from io import StringIO
from unittest.mock import patch
import project4
from pathlib import Path
class TestingGrammar(unittest.TestCase):
    def test_append_rule(self):
        grammar = file_organizer_py.Grammar()
        rule = file_organizer_py.Rule("LetStatement")
        grammar.append_rules(rule)
        self.assertEqual(grammar.rules["LetStatement"], rule)

    def test_append_option(self):
        rule = file_organizer_py.Rule("LetStatement")
        option = file_organizer_py.Option(1, ["LET", "[Variable]", "[Value]"])
        rule.append_option(option)
        self.assertEqual(rule.full_options[0], option)

    def test_one_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] today
        }
        {
        Adjective
        3 happy
        }
        """
        expected_output = "Boo is happy today\n"

        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertEqual(fake_output.getvalue(), expected_output)

        f_p.unlink()

    def test_two_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] today
        }
        {
        Adjective
        3 sad
        3 happy
        }
        """
        expected_output = "Boo is happy today\n"
        expected_output_2 = "Boo is sad today\n"

        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertTrue(fake_output.getvalue() == expected_output or fake_output.getvalue() == expected_output_2)

        f_p.unlink()

    def test_mult_var_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] [Var] today
        }
        {
        Adjective
        3 happy
        }
        {
        Var
        3 camper
        }
        """
        expected_output = "Boo is happy camper today\n"

        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertTrue(fake_output.getvalue() == expected_output)

        f_p.unlink()

    def test_index_else_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] today
        }
        {
        Adjective
        1 happy
        10000000000 sad
        1 crazy
        }
        """
        expected_output = "Boo is sad today\n"

        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertTrue(fake_output.getvalue() == expected_output)

        f_p.unlink()

    def test_mult_var_same_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] [Var] today
        }
        {
        Adjective
        3 happy
        }
        {
        Var
        3 happy
        }
        """
        expected_output = "Boo is happy happy today\n"
        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertTrue(fake_output.getvalue() == expected_output)

        f_p.unlink()


    def test_blank_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] [Var] today
        }
        {
        Adjective
        3
        }
        {
        Var
        3
        }
        """
        expected_output = "Boo is today\n"
        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertTrue(fake_output.getvalue() == expected_output)

    def test_one_other_statement(self):
        file_path = "test_file.txt"
        f_p = Path(file_path)
        num_lines = "1"
        item_name = "HowIsBoo"

        input_data = """
        { 
        HowIsBoo
        1 Boo is [Adjective] today
        }
        {
        Adjective
        3 tooki
        }
        """
        expected_output = "Boo is tooki today\n"

        with open("test_file.txt", "w") as file:
            file.write(input_data)

        with patch('sys.stdout', new = StringIO()) as fake_output:
            with patch('builtins.input', side_effect = [file_path, num_lines, item_name]):
                project4.main()

            self.assertEqual(fake_output.getvalue(), expected_output)

        f_p.unlink()


if __name__ == '__main__':
    unittest.main()
