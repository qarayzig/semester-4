from collections.abc import Iterable, Iterator
from math import sqrt


def is_fibonacci_number(number: int) -> bool:
    """Проверяет, принадлежит ли число ряду Фибоначчи."""
    if number < 0:
        return False

    first_check = 5 * number**2 + 4
    second_check = 5 * number**2 - 4

    first_root = int(sqrt(first_check))
    second_root = int(sqrt(second_check))

    return first_root**2 == first_check or second_root**2 == second_check


class FibonacchiLst:
    """Итератор по числам Фибоначчи через методы __iter__ и __next__."""

    def __init__(self, instance: Iterable[int]) -> None:
        """Инициализирует итератор переданным итерируемым объектом."""
        self.instance = list(instance)
        self.idx = 0

    def __iter__(self) -> Iterator[int]:
        """Возвращает объект итератора."""
        return self

    def __next__(self) -> int:
        """Возвращает следующее число Фибоначчи из переданного списка."""
        while True:
            try:
                result = self.instance[self.idx]
            except IndexError as exc:
                raise StopIteration from exc

            self.idx += 1

            if is_fibonacci_number(result):
                return result


class FibonacchiLstGetItem:
    """Упрощенный итератор по числам Фибоначчи через метод __getitem__."""

    def __init__(self, instance: Iterable[int]) -> None:
        """Инициализирует объект списком чисел Фибоначчи."""
        self.instance = [
            elem for elem in instance
            if is_fibonacci_number(elem)
        ]

    def __getitem__(self, index: int) -> int:
        """Возвращает число Фибоначчи по индексу."""
        return self.instance[index]


if __name__ == "__main__":
    lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]

    print(list(FibonacchiLst(lst)))
    print(list(FibonacchiLstGetItem(lst)))