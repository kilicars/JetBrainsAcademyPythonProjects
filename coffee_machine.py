class CoffeeMachine:

    def __init__(self, water, milk, beans, cups, money):
        self.cur_water = water
        self.cur_milk = milk
        self.cur_beans = beans
        self.cur_disposable_cups = cups
        self.cur_money = money

    def print_cur_state(self):
        print("The coffee machine has:")
        print(f"{self.cur_water} of water")
        print(f"{self.cur_milk} of milk")
        print(f"{self.cur_beans} of coffee beans")
        print(f"{self.cur_disposable_cups} of disposable cups")
        print(f"{self.cur_money} of money")

    def process_buy(self):

        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu::")
        answer = input()
        if answer == "back":
            return
        choice = int(answer)
        water_needed = 0
        milk_needed = 0
        beans_needed = 0
        cups_needed = 1
        money_needed = 0
        if choice == 1:
            water_needed = 250
            beans_needed = 16
            money_needed = 4
        elif choice == 2:
            water_needed = 350
            milk_needed = 75
            beans_needed = 20
            money_needed = 7
        elif choice == 3:
            water_needed = 200
            milk_needed = 100
            beans_needed = 12
            money_needed = 6

        if water_needed > self.cur_water:
            print("Sorry, not enough water!")
        elif milk_needed > self.cur_milk:
            print("Sorry, not enough milk!")
        elif beans_needed > self.cur_beans:
            print("Sorry, not enough coffee beans!")
        elif self.cur_disposable_cups == 0:
            print("Sorry, not enough disposable cups")
        else:
            print("I have enough resources, making you a coffee!")
            self.cur_water -= water_needed
            self.cur_milk -= milk_needed
            self.cur_beans -= beans_needed
            self.cur_disposable_cups -= cups_needed
            self.cur_money += money_needed

    def process_fill(self):

        print("Write how many ml of water do you want to add:")
        add_water = int(input())
        print("Write how many ml of milk do you want to add:")
        add_milk = int(input())
        print("Write how many grams of coffee beans do you want to add:")
        add_beans = int(input())
        print("Write how many disposable cups of coffee do you want to add:")
        add_disposable_cups = int(input())

        self.cur_water += add_water
        self.cur_milk += add_milk
        self.cur_beans += add_beans
        self.cur_disposable_cups += add_disposable_cups

    def process_take(self):
        print(f"I gave you ${self.cur_money}")
        self.cur_money = 0

    def menu(self):
        print("Write action (buy, fill, take, remaining, exit):")
        choice = input()
        while choice != "exit":
            if choice == "buy":
                self.process_buy()
            elif choice == "fill":
                self.process_fill()
            elif choice == "take":
                self.process_take()
            elif choice == "remaining":
                self.print_cur_state()

            print("Write action (buy, fill, take, remaining, exit):")
            choice = input()


if __name__ == "__main__":
    coffee_machine = CoffeeMachine(400, 540, 120, 9, 550)
    coffee_machine.menu()
