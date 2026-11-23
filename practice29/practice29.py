import unittest


class BankAccount:
    def __init__(self, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним")
        self.balance = balance

    def deposit(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сума поповнення має бути додатною")
        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        if amount <= 0:
            raise ValueError("Сума зняття має бути додатною")
        if amount > self.balance:
            raise ValueError("Недостатньо коштів на рахунку")
        self.balance -= amount
        return self.balance


class TestBankAccount(unittest.TestCase):
    def test_1_deposit_positive_amount(self) -> None:
        account = BankAccount(100)
        actual = account.deposit(50)
        self.assertEqual(actual, 150)
        self.assertEqual(account.balance, 150)

    def test_2_withdraw_valid_amount(self) -> None:
        account = BankAccount(100)
        actual = account.withdraw(40)
        self.assertEqual(actual, 60)
        self.assertEqual(account.balance, 60)

    def test_3_withdraw_more_than_balance_rejected(self) -> None:
        account = BankAccount(100)
        with self.assertRaises(ValueError):
            account.withdraw(150)
        self.assertEqual(account.balance, 100)

    def test_4_deposit_negative_amount_raises_error(self) -> None:
        account = BankAccount(100)
        with self.assertRaises(ValueError):
            account.deposit(-5)
        self.assertEqual(account.balance, 100)

    def test_5_zero_and_boundary_operations(self) -> None:
        account = BankAccount(100)
        with self.assertRaises(ValueError):
            account.deposit(0)
        with self.assertRaises(ValueError):
            account.withdraw(0)
        self.assertEqual(account.balance, 100)

        # Граничний випадок: зняття всієї суми балансу
        self.assertEqual(account.withdraw(100), 0)
        self.assertEqual(account.balance, 0)


class SummaryTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.custom_passed = 0

    def addSuccess(self, test):
        super().addSuccess(test)
        self.custom_passed += 1
        doc = test.shortDescription() or test._testMethodName
        self.stream.writeln(f"{doc} — PASS")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        doc = test.shortDescription() or test._testMethodName
        self.stream.writeln(f"{doc} — FAIL")

    def addError(self, test, err):
        super().addError(test, err)
        doc = test.shortDescription() or test._testMethodName
        self.stream.writeln(f"{doc} — FAIL")


def run_suite() -> int:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBankAccount)
    runner = unittest.TextTestRunner(resultclass=SummaryTestResult, verbosity=0)
    result = runner.run(suite)
    errors_count = len(result.failures) + len(result.errors)
    print(f"Підсумок: {result.custom_passed} тестів пройдено, {errors_count} помилок.")
    return 0 if errors_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(run_suite())