""""MODULE: The ATM module, also imports other necessary classes.

    CLASSES
        ATM
            ATM that handles withdrawal, depositing, and viewing.
        Account
            Account that holds the user's information.
        Card
            Card that represents a credit card.
        Receipt
            Receipt that contains a response from the ATM.
"""

# STANDARD LIBRARY
import getpass
import sys

# THIRD-PARTY LIBRARIES
import babel
import money

# ATM LIBRARY
import account
import card
import globals
import receipt
import validation


class ATM:
    """"CLASS: The ATM class, handles the basic functions of an ATM.

    METHODS
        >> __init__(self, accounts)
            Constructs an ATM object.

        >> begin_session(self, user)
            The lifeblood of the ATM's functions.

        >> withdraw(self, acct):
            The withdrawal function.

        >> deposit(self, acct):
            The deposit function.

        >> get_money(self, action):
            Inputs the dollar amount requested by the user.

        >> action_prompt(self):
            The menu of selections.

        >> match_pin(self, acct):
            Attempts to match the pin of the account with user input.

        >> insert_card(self, user):
            Searches for the user's account in the list of Accounts.
    """

    global ACTIONS

    def __init__(self, accounts):
        """METHOD: Constructs an ATM object.

            >> __init__(self, accounts)

            PARAMETERS
                @accounts: The list of Account objects to load into the ATM.

            RETURN
                None.
        """

        # avoid creating a property, this data should remain internal
        self._accounts = accounts

    def begin_session(self, user):
        """METHOD: The lifeblood of the ATM's functions.

            >> begin_session(self, user)

            PARAMETERS
                @user: The card to begin the session.

            RETURN
                None.
        """

        assert isinstance(user, card.Card)

        try:
            match = self.insert_card(user)
            if not self.match_pin(match):
                raise SystemExit("ERROR: Contact the administrator for assistance.\n")
        except SystemExit:
            raise
        except:
            match = None

        if match is not None:
            while True:
                try:
                    choice = self.action_prompt()

                    print()

                    if choice == 1:
                        output = self.withdraw(match)
                        self._accounts.writeChanges("accounts.txt")
                    elif choice == 2:
                        output = self.deposit(match)
                        self._accounts.writeChanges("accounts.txt")
                    elif choice == 3:
                        output = receipt.Receipt(match, globals.ACTIONS[2], None)
                    elif choice == 4:
                        pass  # the user choose to quit
                    break
                except ValueError as e:
                    if str(e) == "ERROR: Insufficient funds.\n":
                        print(str(e))
                    else:
                        raise

            if choice != 4: print(output)
        else:
            sys.stderr.write("ERROR: Account not found.\n")

        print("Thank you for choosing this ATM!")

    def withdraw(self, acct):
        """METHOD: The withdrawal function.

            >> withdraw(self, acct)

            PARAMETERS
                @acct: The account that has been matched.

            RETURN
                A Receipt object containing the ATM response.
        """

        money = self.get_money(globals.ACTIONS[0])
        acct.withdraw(money)
        return receipt.Receipt(acct, globals.ACTIONS[0], money)

    def deposit(self, acct):
        """METHOD: The deposit function.

            >> deposit(self, acct)

            PARAMETERS
                @acct: The account that has been matched.

            RETURN
                A Receipt object containing the ATM response.
        """

        money = self.get_money(globals.ACTIONS[1])
        acct.deposit(money)
        return receipt.Receipt(acct, globals.ACTIONS[1], money)

    def get_money(self, action):
        """METHOD: Inputs the dollar amount requested by the user.

            >> get_money(self, action)

            PARAMETERS
                @action: The action taken (string).

            RETURN
                The cash amount.
        """

        cash = None

        while True:
            try:
                value = input("Enter {} amount: $".format(action.lower()))
                cash = money.Money(amount=value, currency="USD")

                if cash < money.Money(amount=0, currency="USD"):
                    raise ValueError

                break
            except:
                sys.stderr.write("ERROR: Invalid dollar amount.\n")

        return cash

    def action_prompt(self):
        """METHOD: The menu of selections.

            >> action_prompt(self)

            PARAMETERS
                None.

            RETURN
                The choice selected.
        """

        for i, action in enumerate(globals.ACTIONS):
            print("[{}] {}".format(i + 1, action))

        return validation.get_integer("\nMake your selection: ", 1,
                                      len(globals.ACTIONS))

    def match_pin(self, acct):
        """METHOD: Attempts to match the pin of the account with user input.

            >> match_pin(self, acct)

            PARAMETERS
                @acct: The account that has been matched.

            RETURN
                True if the pin authenticated, false otherwise.
        """

        authenticated = False
        # user only has three attempts before they get locked out
        ATTEMPTS = 3

        for i in range(ATTEMPTS):
            pin = getpass.getpass("Enter the 4-digit pin: ")
            if (len(str(pin)) == 4 and acct.validatePin(int(pin)) == True):
                authenticated = True
                self._log.write_log("Pin match, account unlocked", acct.accountNumber[-4:], "None")
                break

            print("{} more attempt{} remaining.".format(ATTEMPTS - (i + 1),
                                                        "" if ATTEMPTS - (i + 1) == 1 else "s"))

        if not authenticated:
            self._log.write_log("Pin match failed", acct.accountNumber[-4:], "None")

        print()

        return authenticated

    def insert_card(self, user):
        """METHOD: Searches for the user's account in the list of Accounts.

            >> insert_card(self, user)

            PARAMETERS
                @user: The card that began the session.

            RETURN
                The matching Account if such an object exists.
        """

        assert isinstance(user, card.Card)

        match = -1

        for i, acct in enumerate(self._accounts):
            if acct.accountNumber == user.number:
                match = i
                break

        return self._accounts[match] if match != -1 else None
