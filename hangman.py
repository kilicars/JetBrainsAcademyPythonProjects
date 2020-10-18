import random


class Hangman:
    def __init__(self):
        self.title = "H A N G M A N"
        self.play_exit_message = 'Type "play" to play the game, "exit" to quit: '
        self.words = ["python", "java", "kotlin", "javascript"]
        self.secret_word = None
        self.output_letters = None
        self.current_word = None
        self.num_lives = None
        self.guessed_letters = set()
        self.win_message = "You guessed the word!\nYou survived!"
        self.lose_message = "You lost!"

    def init_current_game(self):
        self.secret_word = random.choice(self.words)
        self.output_letters = list("-" * len(self.secret_word))
        self.num_lives = 8
        self.guessed_letters.clear()

    def set_current_word(self):
        self.current_word = "".join(self.output_letters)

    def show_current_word(self):
        print("\n" + self.current_word)

    @staticmethod
    def get_input():
        return input("Input a letter: ")

    def process_input(self, user_input):
        if user_input in self.guessed_letters:
            print("You already typed this letter")
        elif len(user_input) != 1:
            print("You should input a single letter")
        elif ord(user_input) < 97 or ord(user_input) > 122:
            print("It is not an ASCII lowercase letter")
        else:
            self.process_letter(user_input)

    def process_letter(self, letter):
        if letter not in self.secret_word:
            self.wrong_guess()
        else:
            self.right_guess(letter)
        self.guessed_letters.add(letter)

    def wrong_guess(self):
        print("No such letter in the word")
        self.num_lives -= 1

    def right_guess(self, letter):
        for j in range(0, len(self.secret_word)):
            if letter == self.secret_word[j]:
                self.output_letters[j] = letter

    def start_game(self):
        print(self.title)
        self.show_menu()

    def show_menu(self):
        answer = input(self.play_exit_message)
        if answer == "play":
            self.play_game()
        else:
            exit()

    def check_current_word(self):
        return self.current_word == self.secret_word

    def win_lose(self):
        if self.check_current_word():
            print(self.win_message)
            self.show_menu()
        elif self.num_lives == 0:
            print(self.lose_message)
            self.show_menu()

    def play_game(self):
        self.init_current_game()
        while self.num_lives >= 0:
            self.win_lose()
            self.set_current_word()
            self.show_current_word()
            self.process_input(self.get_input())


if __name__ == '__main__':
    Hangman().start_game()

