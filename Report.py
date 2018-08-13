"""This program is designed to take a log file from the ATM and print it as an html page

Input:
    String: date of the log to be opened

Output:
    An html page displaying the logs contents

Example:
    Input date in format MM-DD-YY or x to quit:
    05-18-2018
    **opens webpage**
    BANK ATM LOG
    testing log : 9999 : None : Wed May 9 15:41:18 2018


References:
    https://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/webtemplates.html
    https://docs.python.org/3/library/re.html
"""

import re
import time
import os


def set_contents(date):
    """METHOD: Sets the content of the html page

    PARAMETERS
        None

    RETURN
        None

    RAISES
        Prints exception if file cannot be found
    """
    try:
        filename = "log" + str(date) + ".txt"
        with open(filename, 'r') as log:
            log_string = log.read()
            log_string = log_string.replace("\n", "<br></br>\n")
            if log_string != "":
                contents = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
                    <html>
                    <head>
                      <meta content="text/html; charset=ISO-8859-1"
                     http-equiv="content-type">
                      <title>%s</title>
                    </head>
                    <body>
                    <header>
                        <strong style="font-size:25px">BANK ATM LOG</strong>
                    </header>
                    %s
                    </body>
                    </html>
                    ''' % (filename, log_string)
            else:
                return None
        return contents
    except Exception as exception:
        print("file could not be found")
        return None


def strToFile(text, filename):
    """METHOD: Writes an html file with the given name and the given text.

    PARAMETERS
        @text: html formatted text to be written to file
        @filename: The filename to which the text will be written

    RETURNS
        None

    RAISES
        exception if file cannot write
    """
    try:
        output = open(filename, "w")
        output.write(text)
        output.close()
    except:
        print("file could not be written, try again")


def browseLocal(web_contents, filename='tempLogLocal.html'):
    """METHOD: Start your webbrowser on a local file containing the text
    with given filename.

    PARAMETERS
        @web_contents: the contents used to populate the page
        @filename: The name of the local html file created, always = "tempLogLocal.html"

    RETURNS
        None
    """
    import webbrowser, os.path
    strToFile(web_contents, filename)
    webbrowser.open("file:///" + os.path.abspath(filename))  # elaborated for Mac


def main():
    """Runs main program logic"""
    while True:
        try:
            date = input("Input date in format MM-DD-YY or x to quit:\n")
            reg = r"(\d{2}-\d{2}-\d{2})"
            if date == "x":
                break
            elif re.fullmatch(reg, date) != None:
                web_contents = set_contents(date)
                if web_contents == None:
                    print("An unexpected error has occured and file %s was not able" % ("log" + date + ".txt"))
                    print("to produce content")
                else:
                    browseLocal(set_contents(date))
            else:
                print("date was not in proper format, please try again")

        except Exception as exception:
            print("Unexpected error")
            print("Error:", sys.exc_info()[1])
            print("File: ", sys.exc_info()[2].tb_frame.f_code.co_filename)
            print("Line: ", sys.exc_info()[2].tb_lineno)
            print(exception)


main()