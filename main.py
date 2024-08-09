import mysql.connector
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None
        # Establish connection to the remote database
        self.db_connection = mysql.connector.connect(
            host="your-database-host",  # Replace with your database host
            user="your-username",       # Replace with your database username
            password="your-password",   # Replace with your database password
            database="your-database-name"  # Replace with your database name
        )
        self.db_cursor = self.db_connection.cursor()
        self.initialize_leaderboard_table()

    def initialize_leaderboard_table(self):
        # Create the leaderboard table if it doesn't exist
        self.db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                player VARCHAR(255) PRIMARY KEY,
                wins INT
            )
        """)
        self.db_connection.commit()

    def load_leaderboard(self):
        # Load leaderboard data from the database
        self.db_cursor.execute("SELECT * FROM leaderboard ORDER BY wins DESC")
        return self.db_cursor.fetchall()

    def update_leaderboard(self, winner):
        # Update leaderboard with the winner's information
        self.db_cursor.execute("""
            INSERT INTO leaderboard (player, wins) VALUES (%s, 1)
            ON DUPLICATE KEY UPDATE wins = wins + 1
        """, (winner,))
        self.db_connection.commit()

    def print_leaderboard(self):
        # Print the leaderboard
        leaderboard = self.load_leaderboard()
        print("\nLeaderboard:")
        for player, wins in leaderboard:
            print(f"{player}: {wins} wins")

    def print_board(self):
        # Print the game board
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board()

    letter = 'X'
    while game.empty_squares():
        if game.num_empty_squares() == 0:
            return 'It\'s a tie!'

        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(f'{letter} makes a move to square {square}')
                game.print_board()
                print('')

            if game.current_winner:
                print(f'{letter} wins!')
                game.update_leaderboard(letter)
                return f'{letter} wins!'

            letter = 'O' if letter == 'X' else 'X'

    return 'It\'s a tie!'

if __name__ == '__main__':
    game = TicTacToe()

    while True:
        x_player = random  # Replace with actual player logic
        o_player = random  # Replace with actual player logic
        result = play(game, x_player, o_player, print_game=True)
        print(result)
        game.print_leaderboard()

        play_again = input("Play again? (y/n): ")
        if play_again.lower() != 'y':
            break
