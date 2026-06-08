from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from urllib.request import urlopen

import yaml


class Component(ABC):
    """Базовый интерфейс компонента."""

    @abstractmethod
    def operation(self) -> dict[str, Any] | str:
        """Возвращает данные о курсах валют."""
        raise NotImplementedError


class FileSaver(ABC):
    """Интерфейс для сохранения данных в файл."""

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные в файл."""
        raise NotImplementedError


class CurrencyRatesComponent(Component):
    """Компонент, получающий курсы валют в формате словаря."""

    API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

    def operation(self) -> dict[str, Any]:
        """Получает курсы валют через API и возвращает словарь."""
        with urlopen(self.API_URL) as response:
            data = response.read().decode("utf-8")

        return json.loads(data)


class Decorator(Component, FileSaver):
    """Базовый класс декоратора."""

    def __init__(self, component: Component) -> None:
        """Инициализирует декоратор компонентом."""
        self._component = component

    @property
    def component(self) -> Component:
        """Возвращает обернутый компонент."""
        return self._component

    def operation(self) -> dict[str, Any] | str:
        """Возвращает результат работы обернутого компонента."""
        return self._component.operation()

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные в файл."""
        raise NotImplementedError


class JsonDecorator(Decorator):
    """Декоратор, преобразующий данные в JSON-формат."""

    def operation(self) -> str:
        """Возвращает данные в формате JSON."""
        data = self.component.operation()
        return json.dumps(data, ensure_ascii=False, indent=4)

    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные в JSON-файл."""
        Path(filename).write_text(self.operation(), encoding="utf-8")


class YamlDecorator(Decorator):
    """Декоратор, преобразующий данные в YAML-формат."""

    def operation(self) -> str:
        """Возвращает данные в формате YAML."""
        data = self.component.operation()
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False)

    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные в YAML-файл."""
        Path(filename).write_text(self.operation(), encoding="utf-8")


class CsvDecorator(Decorator):
    """Декоратор, преобразующий данные о валютах в CSV-формат."""

    def operation(self) -> str:
        """Возвращает данные о валютах в формате CSV."""
        data = self.component.operation()

        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем.")

        valutes = data.get("Valute", {})

        rows = [
            ["CharCode", "Name", "Nominal", "Value", "Previous"],
        ]

        for valute in valutes.values():
            rows.append(
                [
                    valute.get("CharCode"),
                    valute.get("Name"),
                    valute.get("Nominal"),
                    valute.get("Value"),
                    valute.get("Previous"),
                ]
            )

        return "\n".join(",".join(map(str, row)) for row in rows)

    def save_to_file(self, filename: str) -> None:
        """Сохраняет данные о валютах в CSV-файл."""
        data = self.component.operation()

        if not isinstance(data, dict):
            raise TypeError("Данные должны быть словарем.")

        valutes = data.get("Valute", {})

        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["CharCode", "Name", "Nominal", "Value", "Previous"])

            for valute in valutes.values():
                writer.writerow(
                    [
                        valute.get("CharCode"),
                        valute.get("Name"),
                        valute.get("Nominal"),
                        valute.get("Value"),
                        valute.get("Previous"),
                    ]
                )


def client_code(component: Component) -> None:
    """Выводит результат работы компонента."""
    print(component.operation())


if __name__ == "__main__":
    currency_component = CurrencyRatesComponent()

    json_component = JsonDecorator(currency_component)
    yaml_component = YamlDecorator(currency_component)
    csv_component = CsvDecorator(currency_component)

    json_component.save_to_file("rates.json")
    yaml_component.save_to_file("rates.yaml")
    csv_component.save_to_file("rates.csv")

    client_code(json_component) 