# Mobile Money System

## Project Description

This project is a simple Mobile Money System developed using Python and Object-Oriented Programming (OOP) concepts.

The system simulates basic mobile money services through a USSD-style interface.

## Services Provided

- Check account balance
- Make payments
- Withdraw money
- Transfer money
- Exit the system

## Object-Oriented Programming Concepts

### Encapsulation
The customer's PIN and account balance are kept private inside the classes.

### Inheritance
The `Customer` class inherits from the `User` class. The `Payment`, `Withdrawal`, and `Transfer` classes inherit from the `Transaction` class.

### Abstraction
The `Transaction` class provides a common structure using the abstract `process()` method.

### Polymorphism
The `Payment`, `Withdrawal`, and `Transfer` classes each implement the `process()` method differently.

## Technologies Used

- Python
- Flask
- GitHub
- Render

## Author

**Birungi Enoth**
