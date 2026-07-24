"""A tiny calculator — the demo codebase for learning stacked PRs."""


def add(a, b):
    return a + b


def power(a, b):
    return a ** b


def mod(a, b):
    if b == 0:
        raise ValueError("cannot mod by zero")
    return a % b


def average(numbers):
    if not numbers:
        raise ValueError("cannot average an empty sequence")
    return sum(numbers) / len(numbers)
