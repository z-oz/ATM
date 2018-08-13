# STANDARD LIBRARY
import time


class Log(object):
    """Class: The Log class, handles recording all atm actions

    METHODS
        >> __init__(self)
            Constructs a Log object.

        >> write_log(self, action, last_four_account, amount)
            Writes a timestamped action to a datestamped log
    """

    def __init__(self):
        """METHOD: Constructs a Log Object.

            >> __init_(self)

            PARAMETERS
                None

            RETURN
                None
        """
        self._log_date = time.strftime("%x").replace("/", "-")

    def write_log(self, action, last_four_account, amount):
        """METHOD: Constructs a Log Object.

            >> write_log(self, action, last_four_account, amount)

            PARAMETERS
                @action: the action which was taken on the atm
                @last_four_account: last four digits of the associated account
                    number
                @amount: amount of money involved in transaction as applicable

            RETURN
                None
        """
        try:
            assert len(str(last_four_account)) == 4
            if type(amount) == int:
                assert amount < 5000
            filename = "log" + str(self._log_date) + ".txt"
            timestamp = time.asctime(time.gmtime(time.time()))
            with open(filename, 'a') as _log:
                _log.write(
                    action + " : " + str(last_four_account) + " : " + str(amount) + " : " + str(timestamp) + "\n")
        except AssertionError:
            return "assertion error found, log record not made"

    def print_log(self):
        import Report

    @property
    def log_date(self):
        """METHOD: returns the log date

        >> log_date(self)

        PARAMETERS
            None

        RETURN
            @_log_date: the current day
        """
        return self._log_date

    @log_date.setter
    def log_date(self):
        """METHOD: sets the log date to the current day

        >> log_date(self)

        PARAMETERS
            None

        RETURN
            @_log_date: the current day
        """
        return (time.strftime("%x"))

    def test(self):
        """METHOD: has the class test itself

        >> test(self)

        PARAMETERS
            None

        RETURN
            None
        """
        new_log = Log()
        assert new_log.log_date == time.strftime("%x").replace("/", "-")

        exceptions1 = new_log.write_log("testing log", 9999, "None")
        timestamp = time.asctime(time.gmtime(time.time()))
        exceptions2 = new_log.write_log("Testing accountNum", 88899, "None")
        exceptions3 = new_log.write_log("testing amount", 7777, 1000000)
        testb = "testing."
        for i in range(0, 3):
            time.sleep(1)
            print(testb + (i * '.'))
        filename = "log" + str(new_log.log_date) + ".txt"
        with open(filename) as test:
            text = test.read()
            test_string = "testing log : 9999 : None : %s" % (timestamp)
            if test_string in text:
                print("test succeeded")
            else:
                print('test failed')
            print("Log text:")
            print(text)
            print("Test string:")
            print(test_string)
            print("%s \n %s \n %s" % (exceptions1, exceptions2, exceptions3))


if __name__ == "__main__":
    """Runs the logging self test if __name__ == __main__"""
    new_log = Log()
    test = new_log.test()
    choice = input("would you like to print any logs?")
    if choice in ["yes", "Yes"]:
        new_log.print_log()
    else:
        pass