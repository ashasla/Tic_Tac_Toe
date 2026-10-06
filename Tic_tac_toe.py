import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class Player:

    def __init__(self):
        self.name = ''
        self.symbol = ''

    def choose_name(self):
        while True:
            name = input('Enter your name (letters only): ')
            if name.isalpha():
                self.name = name
                break
            print('Invalid name, please use letters only!')

    def choose_symbol(self, taken_symbols=()):
        while True:
            symbol = input(f'{self.name}, choose your symbol (a single letter): ')
            if not (symbol.isalpha() and len(symbol) == 1):
                print('Invalid symbol. Please try again with a single letter!')
            elif symbol.upper() in taken_symbols:
                print('This symbol is already taken, choose another one!')
            else:
                self.symbol = symbol.upper()
                break


class Menu:

    def validate_choice(self, choice):
        while choice not in ('1', '2'):
            print('Invalid number, please use the numbers (1 or 2)')
            choice = input('Enter your choice (1 or 2): ')
        return choice

    def display_main_menu(self):
        print('⊹₊˚‧︵‿₊Welcome to the XO GAME₊‿︵‧˚₊⊹')
        print('1. Start the GAME')
        print('2. Quit the GAME')
        choice = input('Enter your choice (1 or 2): ')
        clear_screen()
        return self.validate_choice(choice)

    def display_endgame_menu(self):
        menu_text = """
    Game Over!

    1. Restart the Game
    2. Quit the Game

    Enter your choice (1 or 2): """

        choice = input(menu_text)
        return self.validate_choice(choice)


class Board:

    def __init__(self):
        self.board = [str(i) for i in range(1, 10)]

    def display_board(self):
        for i in range(0, 9, 3):
            print('|'.join(self.board[i:i + 3]))
            if i < 6:
                print('-' * 5)

    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol
            return True
        return False

    def is_valid_move(self, choice):
        return self.board[choice - 1].isdigit()

    def restart_board(self):
        self.board = [str(i) for i in range(1, 10)]


class Game:

    def __init__(self):
        self.players = [Player(), Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()

        if choice == '1':
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()

    def setup_players(self):
        taken_symbols = []
        for number, player in enumerate(self.players, start=1):
            print(f'Player {number}, enter your details:')
            player.choose_name()
            player.choose_symbol(taken_symbols)
            taken_symbols.append(player.symbol)
            clear_screen()

    def play_game(self):
        while True:
            self.play_turn()
            if self.check_winner():
                self.board.display_board()
                print(f'{self.players[self.current_player_index].name} wins!')
            elif self.check_draw():
                self.board.display_board()
                print("It's a draw!")
            else:
                self.switch_player()
                continue

            choice = self.menu.display_endgame_menu()
            if choice == '1':
                self.restart_game()
            else:
                self.quit_game()
                break

    def play_turn(self):
        clear_screen()
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name}, it's your turn! Your symbol is '{player.symbol}'")
        while True:
            try:
                cell_choice = int(input('Choose a cell (1-9): '))
                if 1 <= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                print('Invalid move! Please try again.')
            except ValueError:
                print('Invalid input! Please enter a number between 1 and 9.')

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6),             # Diagonals
        ]

        for a, b, c in winning_combinations:
            if self.board.board[a] == self.board.board[b] == self.board.board[c]:
                return True
        return False

    def check_draw(self):
        return all(not cell.isdigit() for cell in self.board.board)

    def restart_game(self):
        self.board.restart_board()
        self.current_player_index = 0

    def quit_game(self):
        print('Thank you for playing! Goodbye >⩊<.')


if __name__ == '__main__':
    game = Game()
    game.start_game()