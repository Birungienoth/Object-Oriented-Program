from abc import ABC, abstractmethod
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "mobile-money-demo-key"


# Encapsulation
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
        if amount <= self.__balance:
            self.__balance -= amount
            return True
        return False


# Abstraction
class Transaction(ABC):

    @abstractmethod
    def process(self, customer, amount):
        pass


# Polymorphism
class Payment(Transaction):
    def process(self, customer, amount):
        if customer.withdraw(amount):
            return f"Payment made successfully: UGX {amount:,.0f}"
        return "The amount on the account is too low to complete your transaction"


class Withdrawal(Transaction):
    def process(self, customer, amount):
        if customer.withdraw(amount):
            return f"Money withdrawn successfully: UGX {amount:,.0f}"
        return "The amount on the account is too low to complete your transaction"


class Transfer(Transaction):
    def process(self, customer, amount):
        if customer.withdraw(amount):
            return f"Money sent successfully: UGX {amount:,.0f}"
        return "The amount on the account is too low to complete your transaction"


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    error = ""

    if request.method == "POST":
        action = request.form.get("action")

        # Create account
        if action == "setup":
            code = request.form.get("code", "")
            balance_text = request.form.get("balance", "")
            pin = request.form.get("pin", "")

            if code != "*222#":
                error = "The option you entered doesn't exist. Please use *222#."
            elif not balance_text:
                error = "Please enter a starting balance."
            elif not balance_text.replace(".", "", 1).isdigit():
                error = "Please enter a valid starting balance."
            elif not (pin.isdigit() and len(pin) == 3):
                error = "PIN must be 3 digits."
            else:
                session["balance"] = float(balance_text)
                session["pin"] = pin
                session["started"] = True
                message = "Account created successfully."

        # Check balance
        elif action == "balance":
            if session.get("started"):
                customer = Customer(session["balance"], session["pin"])
                message = f"Your account balance is: UGX {customer.get_balance():,.0f}"
            else:
                error = "Please create your account first."

        # Payment, withdrawal and transfer
        elif action in ("payment", "withdrawal", "transfer"):
            if not session.get("started"):
                error = "Please create your account first."
            else:
                try:
                    amount = float(request.form.get("amount", "0"))
                    pin = request.form.get("pin", "")
                except ValueError:
                    amount = 0
                    pin = ""

                customer = Customer(session["balance"], session["pin"])

                if customer.check_pin(pin):

                    if action == "payment":
                        result = Payment().process(customer, amount)

                    elif action == "withdrawal":
                        result = Withdrawal().process(customer, amount)

                    else:
                        result = Transfer().process(customer, amount)

                    if "too low" in result:
                        error = result
                    else:
                        message = result

                    # Save updated balance
                    session["balance"] = customer.get_balance()

                else:
                    error = "Incorrect PIN. Please try again."

        # Exit
        elif action == "exit":
            session.clear()
            message = "Thank you for walking with us."

    return render_template(
        "index.html",
        started=session.get("started", False),
        message=message,
        error=error,
        current_balance=session.get("balance")
    )


if __name__ == "__main__":
    app.run(debug=True)
