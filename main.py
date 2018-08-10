# STANDARD LIBRARY
import tkinter

# USER-CREATED LIBRARY
import atm

# GLOBALS

root = tkinter.Tk()
root.geometry("500x500")
root.resizable(0, 0)

menu = None
prompt = None

SUBMISSIONS = ("Pin", "Withdrawal", "Deposit", "View")

machine = atm.ATM(atm.globals.accounts)

# arbitrary card; we can't insert a card into our computers
user = atm.card.Card("3906-4680-7735-0330")

# in reality, we'd need to respond to a failure in matching
match = machine.insert_card(user)
if match is None:
    root.destroy()
    raise SystemExit


# END OF GLOBALS

# base class for derivation
class Frame:
    def __init__(self, root, pad_x=0, pad_y=0):
        # fixed layout, so it's easier to style
        self._frame = tkinter.Frame(root, width=500, height=500, padx=pad_x, pady=pad_y)
        self._frame.pack(fill=tkinter.BOTH, expand=1)

    def hide(self):
        self._frame.pack_forget()
        return self

    def unhide(self):
        self._frame.pack(fill=tkinter.BOTH, expand=1)
        return self


# inherits from Frame
class Menu(Frame):
    def __init__(self, root):
        # initialize the Frame component
        super().__init__(root, 100, 50)
        self._buttons = []

    def add_button(self, button_text, button_function, options_dict):
        self._buttons.append(tkinter.Button(self._frame, options_dict, text=button_text,
                                            command=lambda frame=super(): button_function(frame)))

        self._buttons[len(self._buttons) - 1].pack(fill=tkinter.X, expand=1)


class Prompt(Frame):
    def __init__(self, root):
        super().__init__(root, 40, 40)

        # left side
        self._txtbox = tkinter.Text(self._frame, state="disabled", width=55, height=25, padx=15, pady=15)
        self._txtbox.pack(side="left")

        # right side
        self._rframe = tkinter.Frame(self._frame)
        self._rframe.pack(padx=(37, 0), pady=(80, 0))

        self._state = None
        self._action = None

        self._user_input = []
        self._buttons = []

        for i in range(1, 10):
            self._buttons.append(tkinter.Button(self._rframe, text=(str(i)), width=5, height=2,
                                                command=lambda i=i: self.button_press(i)))
            self._buttons[i - 1].grid(row=((i - 1) // 3), column=((i - 1) % 3))

        self._buttons.append(tkinter.Button(self._rframe, text="0", width=5, height=2,
                                            command=lambda i=i: self.button_press(0)))
        self._buttons[len(self._buttons) - 1].grid(row=(len(self._buttons) // 3), column=((len(self._buttons) - 1) % 3))

        self._buttons.append(tkinter.Button(self._rframe, text=".", width=5, height=2,
                                            command=lambda i=i: self.button_press(".")))

        self._buttons[len(self._buttons) - 1].grid(row=(len(self._buttons) // 3), column=((len(self._buttons) - 1) % 3))

        self._buttons.append(tkinter.Button(self._rframe, text="C", width=5, height=2,
                                            command=lambda i=i: self.button_press("C")))
        self._buttons[len(self._buttons) - 1].grid(row=((len(self._buttons) - 1) // 3),
                                                   column=((len(self._buttons) - 1) % 3))

        tkinter.Button(self._frame, text="Return", width=7, font=(None, 13), command=self.return_button).pack(
            side="left", padx=(35, 25))
        self._submit = tkinter.Button(self._frame, text="Submit", width=7, font=(None, 13), command=self.submit_button)
        self._submit.pack(side="left")

    def button_press(self, n):
        if str(n) != 'C':
            self._user_input.append(str(n))
            self._txtbox.config(state="normal")
            self._txtbox.delete("USER_ENTRY", tkinter.END)
            if self._state != "Pin":
                self._txtbox.insert(tkinter.END, ''.join(self._user_input))
            else:
                self._txtbox.insert(tkinter.END, ''.join(['*' for char in self._user_input]))
            self._txtbox.config(state="disabled")

            if self._state == "Pin" and len(self._user_input) == 4:
                self._submit.invoke()
        else:
            self._user_input.clear()
            self._txtbox.config(state="normal")
            self._txtbox.delete("USER_ENTRY", tkinter.END)
            self._txtbox.config(state="disabled")

    def hide(self):
        self._frame.pack_forget()
        return self

    def unhide(self):
        self._frame.pack(fill=tkinter.BOTH, expand=1)
        return self

    def return_button(self):
        global menu
        self.hide()
        root.geometry("500x500")
        self._user_input.clear()
        menu.unhide()

    def submit_button(self):
        # entry = self._txtbox.get("USER_ENTRY", tkinter.INSERT)
        entry = ''.join(self._user_input)
        ticket = None

        global match

        if self._state == "Pin":
            if entry.strip() == str(match.pin):
                self._user_input.clear()
                self.display("Enter the " + self._action.lower() + " amount: ")
                self._buttons[10]["state"] = "normal"
                self._state = SUBMISSIONS[1] if self._action == "Withdrawal" else SUBMISSIONS[2]
            else:
                self._user_input.clear()
                self.display("ERROR: Invalid pin.\nEnter your four-digit pin: ")
        elif self._state == "Withdrawal":
            try:
                withdrawal = atm.money.Money(amount=entry, currency="USD")

                if withdrawal < atm.money.Money(amount=0, currency="USD"):
                    raise ValueError

                match.withdraw(withdrawal)
                ticket = atm.receipt.Receipt(match, "Withdrawal", withdrawal)
            except ValueError as e:
                self._user_input.clear()

                if str(e) == "ERROR: Insufficient funds.\n":
                    self.display("ERROR: Insufficient funds.\nEnter the withdrawal amount: ")
                else:
                    self.display("ERROR: Invalid dollar amount.\nEnter the withdrawal amount: ")
            except:
                self._user_input.clear()
                self.display("ERROR: Invalid dollar amount.\nEnter the withdrawal amount: ")
        elif self._state == "Deposit":
            try:
                deposit = atm.money.Money(amount=entry, currency="USD")

                if deposit < atm.money.Money(amount=0, currency="USD"):
                    raise ValueError

                match.deposit(deposit)
                ticket = atm.receipt.Receipt(match, "Deposit", deposit)
            except:
                self._user_input.clear()
                self.display("ERROR: Invalid dollar amount.\nEnter the deposit amount: ")

        if ticket is not None:
            self._user_input.clear()
            self._rframe.pack_forget()
            self._txtbox["width"] = 80
            # very ugly line
            self.display('\n' * 5 + ('\n'.join(' ' * 17 + line for line in (str(ticket)).split('\n'))))

    def submit(self, submission_index, action):
        global SUBMISSIONS
        self._state = SUBMISSIONS[submission_index]
        self._action = action

        if self._state == "Pin":
            self._buttons[10]["state"] = "disabled"

    def display(self, text):
        self._txtbox.config(state="normal")
        self._txtbox.delete(1.0, tkinter.END)
        self._txtbox.insert(tkinter.END, text)
        self._txtbox.mark_set("USER_ENTRY", tkinter.INSERT)
        self._txtbox.mark_gravity("USER_ENTRY", tkinter.LEFT)
        self._txtbox.config(state="disabled")


def withdrawal_button(frame):
    frame.hide()  # hide frame
    root.geometry("750x500")
    global prompt

    if not prompt:
        prompt = Prompt(root)
    else:
        prompt.unhide()

    prompt.submit(0, "Withdrawal")
    prompt.display("Enter your four-digit pin: ")


def deposit_button(frame):
    frame.hide()  # hide frame
    root.geometry("750x500")
    global prompt

    if not prompt:
        prompt = Prompt(root)
    else:
        prompt.unhide()

    prompt.submit(0, "Deposit")
    prompt.display("Enter your four-digit pin: ")


def view_button(frame):
    frame.hide()  # hide frame
    root.geometry("750x500")
    global prompt

    if not prompt:
        prompt = Prompt(root)
    else:
        prompt.unhide()

    prompt._rframe.pack_forget()
    prompt._txtbox["width"] = 80
    # very ugly line
    global match

    ticket = atm.receipt.Receipt(match, "View", None)
    prompt.display('\n' * 5 + ('\n'.join(' ' * 17 + line for line in (str(ticket)).split('\n'))))


def quit_button(frame):
    root.destroy()


def create_menu():
    global menu

    menu = Menu(root)
    menu_buttons_options = {
        "bg": "#000000",
        "fg": "#FFFFFF",
        "relief": tkinter.SOLID,
        "font": (None, 16),
        "highlightbackground": "#FFFFFF",
        "pady": 15
    }

    menu.add_button("Withdrawal", withdrawal_button, menu_buttons_options)
    menu.add_button("Deposit", deposit_button, menu_buttons_options)
    menu.add_button("View", view_button, menu_buttons_options)
    menu.add_button("Quit", quit_button, menu_buttons_options)


create_menu()
