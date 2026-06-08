import unittest

from gen_fib import fib_coroutine, my_genn


class TestFibCoroutine(unittest.TestCase):
    """Набор тестов для проверки сопрограммы."""

    def test_0(self) -> None:
        """Проверяет возврат пустого списка при n = 0."""
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        result = gen.send(0)

        self.assertEqual(result, [])

    def test_1(self) -> None:
        """Проверяет возврат одного элемента ряда Фибоначчи."""
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        result = gen.send(1)

        self.assertEqual(result, [0])

    def test_3(self) -> None:
        """Проверяет возврат трех элементов ряда Фибоначчи."""
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        result = gen.send(3)

        self.assertEqual(result, [0, 1, 1])

    def test_5(self) -> None:
        """Проверяет возврат пяти элементов ряда Фибоначчи."""
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        result = gen.send(5)

        self.assertEqual(result, [0, 1, 1, 2, 3])

    def test_8(self) -> None:
        """Проверяет возврат восьми элементов ряда Фибоначчи."""
        my_gen = fib_coroutine(my_genn)
        gen = my_gen()
        result = gen.send(8)

        self.assertEqual(result, [0, 1, 1, 2, 3, 5, 8, 13])


if __name__ == "__main__":
    unittest.main()