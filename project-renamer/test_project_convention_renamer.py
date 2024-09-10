import unittest
from unittest.mock import patch, MagicMock
import os

# Importamos las funciones del script principal
from project_convention_renamer import (
    clean_name, camel_to_kebab, normalize_name, generate_new_name, rename_if_necessary
)


class TestFileRenamingFunctions(unittest.TestCase):

    def test_clean_name(self):
        # Probamos que remueva espacios al inicio/final y antes de la extensión
        self.assertEqual(clean_name('  exampleFile .txt '), 'exampleFile.txt')
        self.assertEqual(clean_name(' file_-.txt'), 'file.txt')
        self.assertEqual(clean_name('sample-name - .md'), 'sample-name.md')

    def test_camel_to_kebab(self):
        # Probamos que convierta camelCase a kebab-case
        self.assertEqual(camel_to_kebab('camelCaseName'), 'camel-case-name')
        self.assertEqual(camel_to_kebab('anotherExampleFile123'), 'another-example-file123')
        self.assertEqual(camel_to_kebab('fileWithoutChange'), 'file-without-change')

    def test_normalize_name(self):
        # Probamos que convierta el nombre a snake_case
        self.assertEqual(normalize_name('sample Name', snake_case=True), 'sample_name')
        self.assertEqual(normalize_name('complex-File--name', snake_case=True), 'complex_file_name')
        self.assertEqual(normalize_name('AnotherExampleFile', snake_case=True), 'anotherexamplefile')

        # Probamos que convierta el nombre a kebab-case
        self.assertEqual(normalize_name('sample Name'), 'sample-name')
        self.assertEqual(normalize_name('complex_file_name'), 'complex-file-name')
        self.assertEqual(normalize_name('AnotherExampleFile'), 'anotherexamplefile')

    def test_generate_new_name(self):
        # Probamos que genere nombres adecuados basados en las convenciones
        self.assertEqual(generate_new_name('CamelCaseFile.txt', snake_case_extensions=('.txt',)), 'camel_case_file.txt')
        self.assertEqual(generate_new_name('kebab-case-example.MD', snake_case_extensions=('.md',)), 'kebab_case_example.md')
        self.assertEqual(generate_new_name('sampleFile', snake_case_extensions=('.txt',)), 'sample-file')

    @patch('os.rename')
    def test_rename_if_necessary(self, mock_rename):
        # Probamos que se renombre si es necesario
        rename_if_necessary('old_name.txt', 'new_name.txt', 'archivo')
        mock_rename.assert_called_once_with('old_name.txt', 'new_name.txt')

        # Probamos que no se renombre si el nombre es el mismo
        mock_rename.reset_mock()
        rename_if_necessary('same_name.txt', 'same_name.txt', 'archivo')
        mock_rename.assert_not_called()

        # Probamos que maneje correctamente cuando el archivo ya existe
        with patch('os.path.exists', return_value=True):
            with patch('builtins.print') as mock_print:
                rename_if_necessary('old_name.txt', 'existing_name.txt', 'archivo')
                mock_print.assert_any_call('El archivo: existing_name.txt \033[41mya existe\033[0m. No se renombrará.')

if __name__ == '__main__':
    unittest.main()
