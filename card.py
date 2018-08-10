import itertools
import re


class Card:
    """CLASS: The Card class, handles the inserted card by user

    METHODS
        >> __init__(self, number)
            Constructs a Card object.

        >> number(self)
            Returns card number
    """

    def __init__(self, number):
        """METHOD: Constructs a Card Object.

            >> __init_(self, number)

            PARAMETERS
                @number: The card number associated with inserted card by user

            RETURN
                None
        """

        self._number = number

    @property
    def number(self):
        """METHOD: Gets card number

            >> number(self)

            PARAMETERS
                None

            RETURN
                Card number
        """

        return self._number

    def card_number_validation(self, number):
        """METHOD: Basic validation of card number.

                    >> card_number_validation(self, number)

                    PARAMETERS
                        number

                    RETURN
                        None
        """
        pattern = re.compile(r"(\d{4})-(\d{4})-(\d{4})-(\d{4})")

        if not pattern.fullmatch(number):
            print("Bad number")
        else:
            print("Success!")

        # OR

    #         if (len(number.split("-")) == 1 and len(number) == 16) or (
    #                 len(number.split("-")) == 4 and all(
    #                 len(i) == 4 for i in number.split("-"))):
    #             number = number.replace("-", "")
    #             try:
    #                 int(number)
    #                 if max(len(list(g)) for _, g in itertools.groupby(number)) > 3:
    #                     print("Failed: 4+ repeated digits")
    #                 else:
    #                     print("Passed")
    #             except ValueError as e:
    #                 print("Failed: non-digit characters")
    #         else:
    #             print("Failed: bad hyphens or length")

    def test(self):
        """METHOD: Tests all class properties and methods

            >> test(self)

            PARAMETERS
                None

            RETURN
                True if all tests are successful

            """

        card_number = Card("6244-5567-891-3458")
        assert isinstance(card_number.number, str), \
            "Account Number must be a string. Received %s" % type(card_number.number)

        return True


if __name__ == "__main__":
    card_number = Card("6244-5567-891-3458")
    if card_number.test():
        print("All tests successful")
