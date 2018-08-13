# STANDARD LIBRARY
import datetime

# THIRD-PARTY LIBRARIES
import babel
import money

# ATM LIBRARY
import account
import globals


class Receipt:
    def __init__(self, acct, action, action_money):
        # refers to a global tuple of possible actions
        global ACTIONS

        assert isinstance(acct, account.Account)
        assert action in globals.ACTIONS
        assert isinstance(action_money, (money.Money, type(None)))

        # I have foregone the default construction
        self._account = acct
        self._action = action
        self._action_money = action_money

    def __str__(self):
        # DATE
        # TIME

        # CARD NUMBER (masked except last 4 digits)
        # CARDHOLDER

        # WITHDRAWAL/DEPOSIT AMOUNT
        # PREVIOUS BALANCE
        # CURRENT BALANCE

        # these identifiers are misnomers; they should be reversed!
        L_PADDING = 15
        R_PADDING = 30

        today = datetime.datetime.now()
        date = "\nDATE:".ljust(L_PADDING) + today.strftime("%x").rjust(R_PADDING + 1) + '\n'
        time = "TIME:".ljust(L_PADDING) + today.strftime("%X").rjust(R_PADDING) + '\n\n'

        card_number = "CARD NUMBER:".ljust(L_PADDING) + \
                      (''.join(('*' if char != '-' else ' ' for char in self._account.accountNumber[:-4])) + \
                       self._account.accountNumber[-4:]).rjust(R_PADDING) + '\n'
        card_holder = "CARD HOLDER:".ljust(L_PADDING) + self._account.name.rjust(R_PADDING) + '\n\n'

        if self._action != "View":
            action = (self._action.upper() + ":").ljust(L_PADDING) + \
                     (self._action_money.format("en_US")).rjust(R_PADDING) + '\n'

            if self._action == "Withdrawal":
                prev = self._account.balance + self._action_money
            else:
                prev = self._account.balance - self._action_money

            prev_balance = "PREV. BALANCE:".ljust(L_PADDING) + \
                           (prev.format("en_US")).rjust(R_PADDING) + '\n'

        cur_balance = "CUR. BALANCE:".ljust(L_PADDING) + \
                      (self._account.balance.format("en_US")).rjust(R_PADDING) + '\n\n'

        return date + time + card_number + card_holder + \
               ((action + prev_balance) if self._action != "View" else "") + cur_balance
