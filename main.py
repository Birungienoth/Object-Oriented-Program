from abc import ABC, abstractmethod
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "mobile-money-demo-key"


# ============================================================
# ENCAPSULATION
# ============================================================

class User:
    def __init__(self, pin):
        self.__pin = pin

    def check_pin(self, pin):
        return self.__pin == pin


class Customer(User):
    def __init__(self, balance, pin):
        super().__init__(pin)
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            return "Invalid amount entered."

        elif amount > self.__balance:
            return False

        else:
            self.__balance -= amount
            return True


# ============================================================
# ABSTRACTION
# ============================================================

class Transaction(ABC):

    @abstractmethod
    def process(self, customer, amount):
        pass


# ============================================================
# POLYMORPHISM
# ============================================================

class Payment(Transaction):
    def process(self, customer, amount):

        result = customer.withdraw(amount)

        if result == "Invalid amount entered.":
            return result

        elif result:
            return f"Payment made successfully: UGX {amount:,.0f}"

        else:
            return "The amount on the account is too low to complete your transaction"


class Withdrawal(Transaction):
    def process(self, customer, amount):

        result = customer.withdraw(amount)

        if result == "Invalid amount entered.":
            return result

        elif result:
            return f"Money withdrawn successfully: UGX {amount:,.0f}"

        else:
            return "The amount on the account is too low to complete your transaction"


class Transfer(Transaction):
    def process(self, customer, amount):

        result = customer.withdraw(amount)

        if result == "Invalid amount entered.":
            return result

        elif result:
            return f"Money sent successfully: UGX {amount:,.0f}"

        else:
            return "The amount on the account is too low to complete your transaction"


# ============================================================
# FLASK APPLICATION
# ============================================================

@app.route("/", methods=["GET", "POST"])
def index():

    message = ""
    error = ""
    show_balance = False

    if request.method == "POST":

        action = request.form.get("action")

        # ----------------------------------------------------
        # DIAL USSD CODE
        # ----------------------------------------------------

        if action == "dial":

            code = request.form.get("code", "")

            if code == "*222#":

                session["dialed"] = True
                message = "USSD code accepted."

            else:

                error = (
                    "Dear customer the option you entered "
                    "doesn't exist. Please use *222#."
                )

        # ----------------------------------------------------
        # ENTER PIN
        # ----------------------------------------------------

        elif action == "login":

            pin = request.form.get("pin", "")

            # Starting balance for the demonstration
            balance = 20000

            customer = Customer(balance, pin)

            # The demonstration PIN is 222
            if pin == "222":

                session["pin"] = pin
                session["balance"] = balance
                session["authenticated"] = True

                message = (
                    f"Your account balance is: "
                    f"UGX {balance:,.0f}"
                )

                show_balance = True

            else:

                error = "Incorrect PIN. Please try again."

        # ----------------------------------------------------
        # CHECK BALANCE
        # ----------------------------------------------------

        elif action == "balance":

            if session.get("authenticated"):

                customer = Customer(
                    session["balance"],
                    session["pin"]
                )

                message = (
                    f"Your account balance is: "
                    f"UGX {customer.get_balance():,.0f}"
                )

                show_balance = True

            else:

                error = "Please enter your PIN first."

        # ----------------------------------------------------
        # PAYMENT, WITHDRAWAL AND TRANSFER
        # ----------------------------------------------------

        elif action in ("payment", "withdrawal", "transfer"):

            if not session.get("authenticated"):

                error = "Please enter your PIN first."

            else:

                try:

                    amount = float(
                        request.form.get("amount", "0")
                    )

                    pin = request.form.get("pin", "")

                except ValueError:

                    amount = 0
                    pin = ""

                customer = Customer(
                    session["balance"],
                    session["pin"]
                )

                # Check PIN
                if customer.check_pin(pin):

                    # Select transaction type
                    if action == "payment":

                        result = Payment().process(
                            customer,
                            amount
                        )

                    elif action == "withdrawal":

                        result = Withdrawal().process(
                            customer,
                            amount
                        )

                    else:

                        result = Transfer().process(
                            customer,
                            amount
                        )

                    # Display result
                    if result == "Invalid amount entered.":

                        error = result

                    elif "too low" in result:

                        error = result

                    else:

                        message = result

                    # Save updated balance
                    session["balance"] = (
                        customer.get_balance()
                    )

                    # Show balance after transaction
                    show_balance = True

                else:

                    error = "Incorrect PIN. Please try again."

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif action == "exit":

            session.clear()

            message = "Thank you for walking with us."

    # --------------------------------------------------------
    # DISPLAY PAGE
    # --------------------------------------------------------

    return render_template(
        "index.html",
        dialed=session.get("dialed", False),
        authenticated=session.get("authenticated", False),
        message=message,
        error=error,
        show_balance=show_balance,
        current_balance=session.get("balance")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
