from calculator import add, subtract, multiply, divide, evaluate_expression


def run_tests():
    assert add(2, 3) == 5
    assert subtract(10, 4) == 6
    assert multiply(3, 7) == 21
    assert divide(10, 2) == 5
    assert evaluate_expression("2 + 3 * 4") == 14
    assert evaluate_expression("(1 + 2) ** 3") == 27
    assert evaluate_expression("-5 + 8") == 3
    print("All calculator tests passed.")


if __name__ == "__main__":
    run_tests()
