import babel
import money


class Account:
    """Supports account information such as account number,
        name, pin, and balance

    """

    def __init__(self, name, accountNumber, pin, balance):
        assert isinstance(balance, money.Money)
        """Creates an account object.

        Args:
            name (string): Person the account belongs to.
            accountNumber (string): number assigned to the account.
            pin (float): 4 digit code to access account.
            balance (float): Current amount of money in account.

        AssertionError: If balance is not of the type "money".

        """

        self._name = name
        self._accountNumber = accountNumber
        self._pin = pin
        self._balance = balance

    @property
    def name(self):
        """Gets name of account holder.

        Returns:
            string: name

        """

        return self._name

    @property
    def accountNumber(self):
        """Gets the account number.

        Returns:
            string: account number

        """

        return self._accountNumber

    @property
    def balance(self):
        """Gets the current balance of the account.

        Returns:
            float: balance

        """

        return self._balance

    @property
    def pin(self):
        """Gets the accounts pin number.

        Returns:
            float: pin number

        """
        return self._pin

    def withdraw(self, amount):
        """Subtracts amount of money from the balance.

        Args:
            amount (float): amount to be taken out of balance

        Raises:
            AssertionError: If amount is not of the type "money"
            Error: if balance is less than amount

        """

        assert isinstance(amount, money.Money)

        if amount > self.balance:
            raise ValueError("ERROR: Insufficient funds.\n")
        else:
            self._balance -= amount

    def deposit(self, amount):
        """Adds amount of money to the balance.

        Args:
            amount (float): amount to be added to balance

        Raises:
            AssertionError: If amount is not of the type "money"

        """

        assert isinstance(amount, money.Money)
        self._balance += amount

    def test(self):
        """Tests all the account class properties and methods.

        Returns:
            True (bool): If all tests successful.

        Raises:
            AssertionError: If a test fails.

        """

        acct = account("John Jackson", "4899321004786381", 3465, 981.92)
        assert isinstance(acct.name, str), \
            "Name must be a string. Received %s" % type(acct.name)
        assert isinstance(acct.accountNumber, str), \
            "Account Number must be a string. Received %s" % type(acct.accountNumber)
        assert isinstance(acct.pin, int), \
            "Pin must be a 4 digit integer. Received %s" % type(acct.pin)
        assert isinstance(acct.balance, money.Money), \
            "Balance must be a float. Received %s" % type(acct.balance)

        acct.withdraw(200.00)
        assert acct.balance == 781.92

        acct.deposit(100.00)
        assert acct.balance == 881.92

        return True


if __name__ == "__main__":
    """Run tests if module is executed by name."""

    acct = account("John Jackson", "4899321004786381", 3465, 981.92)
    if acct.test():
        print("All tests successful!")
