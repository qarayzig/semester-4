import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import yaml

from main import Component, CsvDecorator, JsonDecorator, YamlDecorator


class FakeCurrencyComponent(Component):
    """Тестовый компонент с заранее заданными курсами валют."""

    def operation(self) -> dict[str, Any]:
        """Возвращает тестовые данные о курсах валют."""
        return {
            "Date": "2026-06-09T11:30:00+03:00",
            "Valute": {
                "USD": {
                    "CharCode": "USD",
                    "Name": "Доллар США",
                    "Nominal": 1,
                    "Value": 78.5,
                    "Previous": 79.1,
                },
                "EUR": {
                    "CharCode": "EUR",
                    "Name": "Евро",
                    "Nominal": 1,
                    "Value": 90.2,
                    "Previous": 91.0,
                },
            },
        }


class TestJsonDecorator(unittest.TestCase):
    """Тесты JSON-декоратора."""

    def test_operation_returns_json(self) -> None:
        """Проверяет, что декоратор возвращает строку JSON."""
        component = JsonDecorator(FakeCurrencyComponent())
        result = component.operation()
        data = json.loads(result)

        self.assertEqual(data["Valute"]["USD"]["CharCode"], "USD")

    def test_save_to_file(self) -> None:
        """Проверяет сохранение JSON-данных в файл."""
        component = JsonDecorator(FakeCurrencyComponent())

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "rates.json"
            component.save_to_file(str(file_path))

            data = json.loads(file_path.read_text(encoding="utf-8"))
            self.assertEqual(data["Valute"]["EUR"]["Name"], "Евро")


class TestYamlDecorator(unittest.TestCase):
    """Тесты YAML-декоратора."""

    def test_operation_returns_yaml(self) -> None:
        """Проверяет, что декоратор возвращает строку YAML."""
        component = YamlDecorator(FakeCurrencyComponent())
        result = component.operation()
        data = yaml.safe_load(result)

        self.assertEqual(data["Valute"]["USD"]["Name"], "Доллар США")

    def test_save_to_file(self) -> None:
        """Проверяет сохранение YAML-данных в файл."""
        component = YamlDecorator(FakeCurrencyComponent())

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "rates.yaml"
            component.save_to_file(str(file_path))

            data = yaml.safe_load(file_path.read_text(encoding="utf-8"))
            self.assertEqual(data["Valute"]["EUR"]["CharCode"], "EUR")


class TestCsvDecorator(unittest.TestCase):
    """Тесты CSV-декоратора."""

    def test_operation_returns_csv(self) -> None:
        """Проверяет, что декоратор возвращает строку CSV."""
        component = CsvDecorator(FakeCurrencyComponent())
        result = component.operation()

        self.assertIn("CharCode,Name,Nominal,Value,Previous", result)
        self.assertIn("USD,Доллар США,1,78.5,79.1", result)

    def test_save_to_file(self) -> None:
        """Проверяет сохранение CSV-данных в файл."""
        component = CsvDecorator(FakeCurrencyComponent())

        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "rates.csv"
            component.save_to_file(str(file_path))

            content = file_path.read_text(encoding="utf-8")
            self.assertIn("EUR,Евро,1,90.2,91.0", content)


if __name__ == "__main__":
    unittest.main()