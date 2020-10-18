import random
import sqlite3


class CreditCardDb:

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = self.connect_db()

    def connect_db(self):
        conn = sqlite3.connect(self.db_name)
        return conn

    def create_card_table(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS card
                 (id integer primary key autoincrement, number text, pin text, balance integer default 0)''')

    def insert_card(self, card_number, pin, balance):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (card_number, pin, balance))
        self.conn.commit()

    def card_number_exists(self, card_number):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM card WHERE number=?", [card_number])
        return cursor.fetchone() is not None

    def check_card_login(self, card_number, pin):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM card WHERE number=? AND pin=?", [card_number, pin])
        return cursor.fetchone() is not None

    def get_balance(self, card_number, pin):
        cursor = self.conn.cursor()
        cursor.execute("SELECT balance FROM card WHERE number=? AND pin=?", [card_number, pin])
        balance = cursor.fetchone()[0]
        return balance

    def update_balance(self, card_number, amount):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE card SET balance=balance+? WHERE number=?", [amount, card_number])
        self.conn.commit()

    def delete_card(self, card_number, pin):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM card WHERE number=? AND pin=?", [card_number, pin])
        self.conn.commit()


class CreditCard:

    def __init__(self, credit_card_db):
        self.credit_card_db = credit_card_db
        credit_card_db.create_card_table()

    @staticmethod
    def print_menu():
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")

    def create_account(self):
        card_number, pin = self.generate_credit_card()
        print("Your card has been created")
        print("Your card number:", card_number, sep="\n")
        print("Your card PIN:", pin, sep="\n")

    def generate_credit_card(self):
        generated = False
        while not generated:
            card_number = "400000"
            pin = ""
            for _ in range(9):
                digit = random.randint(1, 9)
                card_number += str(digit)
            last_digit = self.apply_luhn_alg(card_number)
            card_number += str(last_digit)
            if not self.credit_card_db.card_number_exists(card_number):
                pin = self.generate_pin()
                self.credit_card_db.insert_card(card_number, pin, 0)
                generated = True
        return [card_number, pin]

    @staticmethod
    def generate_pin():
        pin = ""
        for _ in range(4):
            digit = random.randint(1, 9)
            pin += str(digit)
        return pin

    @staticmethod
    def apply_luhn_alg(card_number):
        length = len(card_number)
        sum_digits = 0
        for i in range(0, length):
            if i % 2 == 0:
                cur = int(card_number[i]) * 2
                if cur > 9:
                    cur -= 9
                sum_digits += cur
            else:
                sum_digits += int(card_number[i])
        rem = sum_digits % 10
        return rem if rem == 0 else 10 - rem

    def login(self):
        card_number = input("Enter your card number:")
        pin = input("Enter your PIN:")
        if self.credit_card_db.check_card_login(card_number, pin):
            print("You have successfully logged in!\n")
            self.account_operations(card_number, pin)
        else:
            print("Wrong card number or PIN!\n")

    def account_operations(self, card_number, pin):
        while True:
            self.print_card_menu()
            choice = int(input())
            if choice == 1:
                self.show_balance(card_number, pin)
            elif choice == 2:
                self.add_income(card_number)
            elif choice == 3:
                self.process_transfer(card_number, pin)
            elif choice == 4:
                self.close_account(card_number, pin)
            elif choice == 5:
                self.logout()
            elif choice == 0:
                self.exit_menu()
            else:
                print("Unknown option\n")

    @staticmethod
    def print_card_menu():
        print('''1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit''')

    def show_balance(self, card_number, pin):
        print(f"Balance: {self.credit_card_db.get_balance(card_number, pin)}\n")

    def add_income(self, card_number):
        income = int(input("Enter income:"))
        self.credit_card_db.update_balance(card_number, income)
        print("Income was added!\n")

    def process_transfer(self, card_number, pin):
        print("Transfer")
        transfer_card_number = input("Enter card number\n")
        if card_number == transfer_card_number:
            print("You can't transfer money to the same account!\n")
        else:
            last_digit = self.apply_luhn_alg(transfer_card_number[0:15])
            if str(last_digit) != transfer_card_number[-1]:
                print("Probably you made mistake in the card number. Please try again!\n")
            elif not self.credit_card_db.card_number_exists(transfer_card_number):
                print("Such a card does not exist.\n")
            else:
                self.transfer(card_number, pin, transfer_card_number)

    def transfer(self, card_number, pin, transfer_card_number):
        transfer_amount = int(input("Enter how much money you want to transfer:"))
        current_amount = self.credit_card_db.get_balance(card_number, pin)
        if transfer_amount > current_amount:
            print("Not enough money!\n")
        else:
            self.credit_card_db.update_balance(card_number, -1 * transfer_amount)
            self.credit_card_db.update_balance(transfer_card_number, transfer_amount)
            print("Success\n")

    def close_account(self, card_number, pin):
        self.credit_card_db.delete_card(card_number, pin)
        print("The account has been closed!\n")

    @staticmethod
    def logout():
        print("You have successfully logged out!\n")

    @staticmethod
    def exit_menu():
        print("Bye!")
        exit()

    def main(self):
        while True:
            self.print_menu()
            choice = int(input())
            if choice == 1:
                self.create_account()
            elif choice == 2:
                self.login()
            elif choice == 0:
                self.exit_menu()
            else:
                print("Unknown option\n")


if __name__ == '__main__':
    card_db = CreditCardDb("card.s3db")
    CreditCard(card_db).main()
