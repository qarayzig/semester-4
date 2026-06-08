import unittest

from fib_iterator import FibonacchiLst, FibonacchiLstGetItem


class TestFibIterator(unittest.TestCase):
    """Набор тестов для проверки итераторов."""

    def test_normal(self) -> None:
        """Проверяет обычный случай со списком range(10)."""
        result = list(FibonacchiLst(range(10)))

        self.assertEqual(result, [0, 1, 2, 3, 5, 8])

    def test_list_with_duplicate_one(self) -> None:
        """Проверяет список, в котором единица встречается повторно."""
        result = list(FibonacchiLst([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1]))

        self.assertEqual(result, [0, 1, 2, 3, 5, 8, 1])

    def test_corner_0(self) -> None:
        """Проверяет пустой список."""
        result = list(FibonacchiLst([]))

        self.assertEqual(result, [])

    def test_corner_1(self) -> None:
        """Проверяет список из одного элемента."""
        result = list(FibonacchiLst(range(1)))

        self.assertEqual(result, [0])

    def test_corner_2(self) -> None:
        """Проверяет список из двух элементов."""
        result = list(FibonacchiLst(range(2)))

        self.assertEqual(result, [0, 1])

    def test_corner_3(self) -> None:
        """Проверяет список, состоящий из двух единиц."""
        result = list(FibonacchiLst([1, 1]))

        self.assertEqual(result, [1, 1])

    def test_getitem_iterator(self) -> None:
        """Проверяет упрощенный итератор через метод __getitem__."""
        result = list(FibonacchiLstGetItem(range(10)))

        self.assertEqual(result, [0, 1, 2, 3, 5, 8])


if __name__ == "__main__":
    unittest.main()