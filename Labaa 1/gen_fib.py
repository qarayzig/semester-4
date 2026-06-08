import functools
from collections.abc import Callable, Generator
from typing import Any


def fib_elem_gen() -> Generator[int, None, None]:
    """Генератор, возвращающий элементы ряда Фибоначчи по одному."""
    a = 0
    b = 1

    while True:
        yield a
        res = a + b
        a = b
        b = res


def my_genn() -> Generator[list[int] | None, int, None]:
    """Сопрограмма, возвращающая список первых n чисел ряда Фибоначчи."""
    while True:
        number_of_fib_elem = yield
        g = fib_elem_gen()
        result = [next(g) for _ in range(number_of_fib_elem)]
        yield result


def fib_coroutine(
    g: Callable[..., Generator[list[int] | None, int, None]],
) -> Callable[..., Generator[list[int] | None, int, None]]:
    """Декоратор для предварительного запуска сопрограммы."""

    @functools.wraps(g)
    def inner(*args: Any, **kwargs: Any) -> Generator[list[int] | None, int, None]:
        """Создает сопрограмму и подготавливает ее к приему данных через send()."""
        gen = g(*args, **kwargs)
        gen.send(None)
        return gen

    return inner


if __name__ == "__main__":
    my_gen = fib_coroutine(my_genn)
    gen = my_gen()
    print(gen.send(10))