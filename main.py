from abc import ABC, abstractmethod

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

class Transaction(ABC):

    @abstractmethod
    def process(self, customer, amount):
        pass

class Payment(Transaction):
    def process(self, customer, amount):
        if customer.withdraw(amount):
            print("Payment made successfully: UGX", amount)
        else:
            print("The amount on the account is too low to complete your transaction")

class Withdrawal(Transaction):
    def process(self, customer, amount):
        if customer.withdraw(amount):
            print("Money withdrawn successfully: UGX", amount)
        else:
            print("The amount on the account is too low to complete your transaction")

class Transfer(Transaction):
    def process(self, customer, amount):
        if customer.withdraw(amount):
            print("Money sent successfully: UGX", amount)
        else:
            print("The amount on the account is too low to complete your transaction")

print("welcome to our services")

code = input("Access our services by dialing *222#: ")

if code == "*222#":

    balance = float(input("Enter starting balance (UGX): "))

    while True:
        pin = input("Create 3-digit PIN: ")

        if pin.isdigit() and len(pin) == 3:
            break
        else:
            print("PIN must be 3 digits")

    customer = Customer(balance, pin)

    while True:

        print("\nour available services")
        print("1. Check Balance")
        print("2. Make Payment")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Your account balance is: UGX", customer.get_balance())

        elif choice == "2":
            number = input("Enter payment number: ")
            amount = float(input("Enter payment amount (UGX): "))

            password = input("Enter PIN: ")

            if customer.check_pin(password):
                Payment().process(customer, amount)

        elif choice == "3":
            amount = float(input("Enter withdrawal amount (UGX): "))

            password = input("Enter PIN: ")

            if customer.check_pin(password):
                Withdrawal().process(customer, amount)

        elif choice == "4":
            number = input("Enter recipient phone number: ")
            amount = float(input("Enter transfer amount (UGX): "))

            password = input("Enter PIN: ")

            if customer.check_pin(password):
                Transfer().process(customer, amount)

        elif choice == "5":
            print("Thank you for walking with us")
            break
        else:
            print("The option you entered doesn't exist, try again")
else:
    print("Dear customer The option you entered doesn't existInvalid code")

