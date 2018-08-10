import account
import os


class Accounts(list):

    def __init__(self):
        """Creates an Accounts(list) object."""

        self.Accounts = []

    def readAccounts(self, filename):
        """Reads in the accounts from a database and stores it into a list of individual
            account objects

        Args:
            filename (str): name of database

        Returns: Accounts(list):  List of each account item

        """

        with open(filename, 'r') as file:
            line = file.readline()
            for line in file:
                name, acctNumber, pin, balance = (str(line)).split(',')
                acct = account.account(str(name), str(acctNumber), str(pin), float(balance))
                assert isinstance(acct.name, str), \
                    "Name must be a string. Received %s" % type(acct.name)
                assert isinstance(acct.accountNumber, str), \
                    "Account Number must be a string. Received %s" % type(acct.accountNumber)
                assert isinstance(acct.pin, str), \
                    "Pin must be a 4 digit integer. Received %s" % type(acct.pin)
                assert isinstance(acct.balance, float), \
                    "Balance must be of type money. Received %s" % type(acct.balance)
                self.append(acct)
            return self

    def checkForAccount(self, number):
        """Searches through accounts in database to see if there is a matching Account Number

        Args:
            number (float): Account Number from card

        Returns: bool:  True if it finds a matching account number, false otherwise.

        """

        for i in range(len(self)):
            if number == self[i].accountNumber:
                return True
        return False

    def findAccount(self, number):
        """Searches through accounts in database to find matching Account Number

        Args:
            number (float): Account Number from card

        Returns: Account(account):  The account in database with matching Account Number

        """

        for i in range(len(self)):
            if number == self[i].name:
                return self[i]
        return None

    def writeChanges(self, filename):
        """Writes the new account information stored in the Accounts list back into the database

        Args:
            filename (str): name of database

        """

        with open(filename, "w") as file:
            file.write("Name,Account Number,Pin,Balance\n")
            for i in range(0, len(self)):
                file.write("%s,%s,%s,%s\n" % (
                str(self[i].name), str(self[i].accountNumber), str(self[i].pin), str(self[i].balance)))
        file.close()

    def test(self):
        """Tests all the Accounts class properties and methods.

        Returns:
            True (bool): If all tests successful.

        """

        filename = "accounts.txt"
        self.readAccounts(filename)
        p = str("Gregg Gearhart")
        Acct = self.findAccount(p)
        Acct.deposit(100.00)
        print(Acct.balance)
        self.writeChanges(filename)


if __name__ == "__main__":
    """Run tests if module is executed by name."""
    accts = Accounts()
    if accts.test():
        print("All tests successful!")