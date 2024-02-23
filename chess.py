WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


class Piece:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Knight(Piece):
    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if abs(col - col1) * abs(row - row1) == 2 and row1 != row and \
                col1 != col and correct_coords(row1, col1):
            return True
        return False


class Bishop(Piece):
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row, col):
            return False
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
                return True
            if row + col == row1 + col1:
                step = 1 if (row1 >= row) else -1
                for r in range(row + step, row1, step):
                    c = row + col - r
                    if not (board.get_piece(r, c) is None):
                        return False
                return True
            return False
        return False


class Rook(Piece):
    def __init__(self, color):
        self.was_moved = False
        super().__init__(color)

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False
        self.was_moved = True
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Piece):
    def _init_(self, color):
        self.was_moved = False
        super().__init__(color)

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if ((abs(row - row1) == abs(col - col1) == 1)
            or (abs(row - row1) * abs(col - col1) == 0
                and (abs(row - row1) == 1 or abs(col - col1) == 1))) \
                and correct_coords(row1, col1):
            self.was_moved = True
            return True
        return False


class Queen(Piece):
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn(Piece):
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if col != col1:
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for _ in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  
        self.field[row1][col1] = piece  
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  
        piece = self.field[row][col]
        if not isinstance(piece, Pawn):
            return False
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == self.color:
            return False
        if row not in [1, 6] and row1 not in [0, 7]:
            return False
        self.field[row][col] = None
        if char == 'Q':
            self.field[row1][col1] = Queen(self.color)
        elif char == 'R':
            self.field[row1][col1] = Rook(self.color)
        elif char == 'B':
            self.field[row1][col1] = Bishop(self.color)
        elif char == 'N':
            self.field[row1][col1] = Knight(self.color)
        else:
            return False
        self.color = opponent(self.color)
        return True

    def castling0(self):
        if self.color == WHITE:
            if not isinstance(self.field[0][0], Rook):
                return False
            if not isinstance(self.field[0][4], King):
                return False
            if self.field[0][0].was_moved or self.field[0][4].was_moved:
                return False
            for i in self.field[0][1:4]:
                if i is not None:
                    return False
            self.field[0][4] = None
            self.field[0][0] = None
            self.field[0][2] = King(self.color)
            self.field[0][3] = Rook(self.color)
        elif self.color == BLACK:
            if not isinstance(self.field[7][0], Rook):
                return False
            if not isinstance(self.field[7][4], King):
                return False
            if self.field[7][0].was_moved or self.field[7][4].was_moved:
                return False
            for i in self.field[7][1:4]:
                if i is not None:
                    return False
            self.field[7][4] = None
            self.field[7][0] = None
            self.field[7][2] = King(self.color)
            self.field[7][3] = Rook(self.color)
        self.color = opponent(self.color)
        return True

    def castling7(self):
        if self.color == WHITE:
            if not isinstance(self.field[0][7], Rook):
                return False
            if not isinstance(self.field[0][4], King):
                return False
            if self.field[0][7].was_moved or self.field[0][4].was_moved:
                return False
            for i in self.field[0][5:7]:
                if i is not None:
                    return False
            self.field[0][4] = None
            self.field[0][7] = None
            self.field[0][6] = King(self.color)
            self.field[0][5] = Rook(self.color)
        elif self.color == BLACK:
            if not isinstance(self.field[7][7], Rook):
                return False
            if not isinstance(self.field[7][4], King):
                return False
            if self.field[7][7].was_moved or self.field[7][4].was_moved:
                return False
            for i in self.field[7][5:7]:
                if i is not None:
                    return False
            self.field[7][4] = None
            self.field[7][7] = None
            self.field[7][6] = King(self.color)
            self.field[7][5] = Rook(self.color)
        self.color = opponent(self.color)
        return True

    def is_under_attack(self, row, col, color):
        for i in range(8):
            for j in range(8):
                if self.field[i][j] is not None:
                    piece = self.field[i][j]
                    if piece.get_color() == color:
                        if piece.can_move(row, col):
                            return True
        return False

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None


def print_board(board):
    pos = 'abcdefgh'
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row + 1, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(pos[col], end='    ')
    print()


def main():
    board = Board()
    language = input('''
                    Welcome to CHESS!

Select language:
1. english
2. arabic
''')
    while language not in ('1', 'english', '2', 'arabic'):
        language = input('Incorrect answer, retry: ')
    interpretation = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    if language == ('1' or 'english'):
        input('''
                    English language has been selected
            Press "enter" to view commands and start the game
''')
        print('''
Command:                                  What it does:
exit                                      -- exit
move <row> <col> <row1> <col1>            -- move from (row, col) to (row1, col1); (for example "move 2 e 4 e")
castling <row> <col>                      -- rook castling
pawn <row> <col> <row1> <col1> <char>     -- turning a pawn into a selected piece
help                                      -- print commands

''')
        while True:
            print_board(board)
            if board.current_player_color() == WHITE:
                print("White's move:")
            else:
                print("Black's move")
            command = input()
            while command not in ['exit', 'help'] and ('castling' or 'pawn' or 'move') in command:
                command = input('Unexpected answer, retry: ')
            if command == 'exit':
                break
            elif command == 'help':
                print('''
Command:                                  What it does:
exit                                      -- exit
move <row> <col> <row1> <col1>            -- move from (row, col) to (row1, col1); (for example "move 1 b 3 c")
castling <row> <col>                      -- rook castling
pawn <row> <col> <row1> <col1> <char>     -- turning a pawn into a selected piece
help                                      -- print commands''')
            arguments = command.lower().split()
            if arguments[0] == 'move':
                row, col, row1, col1 = arguments[1:]
                row, col = int(row) - 1, interpretation.get(col)
                row1, col1 = int(row1) - 1, interpretation.get(col1)
                if board.move_piece(row, col, row1, col1):
                    print('Move Successful')
                else:
                    print('Incorrect coordinates! Please retry: ')
            elif arguments[0] == 'pawn':
                row, col, row1, col1, char = arguments[1:]
                row, col = int(row) - 1, interpretation.get(col)
                row1, col1 = int(row1) - 1, interpretation.get(col1)
                if board.move_and_promote_pawn(row, col, row1, col1, char):
                    print('Move Successful')
                else:
                    print('Incorrect coordinates! Please retry: ')
            elif arguments[0] == 'castling':
                row, col = map(int, arguments[1:])
                if col == 7 and board.castling7() or col == 0 and board.castling0():
                    print('Castling Successful')
                else:
                    print('Impossible to castle')

    else:
        input('''
                تم اختيار اللغة العربية       
               اضغط على 'Enter' للمتابعة
الأمر                           : ماذا يفعل:
exit                                   -- خروج
move <row> <col> <row1> <col1>         -- الحركة من الخلية (row, col) إلى الخلية (row1, col1)
castling <row> <col>                   -- القلب بتلك الرخ
pawn <row> <col> <row1> <col1> <char>  -- تحويل البيدق إلى القطعة المختارة
help                                   -- عرض قائمة الأوامر

''')
        while True:
            print_board(board)
            if board.current_player_color() == WHITE:
                print('تحرك البيض:')
            else:
                print('تحرك السود:')
            command = input()
            while command not in ['خروج', 'مساعدة'] and \
                    ('القلب' or 'البيدق' or 'نقل') in command:
                command = input('أمر غير معروف, أعد إدخال الإجابة: ')
            if command == 'exit':
                break
            elif command == 'help':
                print('''
الأمر                           : ماذا يفعل:
exit                                   -- خروج
move <row> <col> <row1> <col1>         -- الحركة من الخلية (row, col) إلى الخلية (row1, col1)
castling <row> <col>                   -- القلب بتلك الرخ
pawn <row> <col> <row1> <col1> <char>  -- تحويل البيدق إلى القطعة المختارة
help                                   -- عرض قائمة الأوامر
''')
            arguments = command.lower().split()
            if arguments[0] == 'move':
                row, col, row1, col1 = arguments[1:]
                row, col = int(row) - 1, interpretation.get(col)
                row1, col1 = int(row1) - 1, interpretation.get(col1)
                if board.move_piece(row, col, row1, col1):
                    print('الحركة ناجحة')
                else:
                    print('الإحداثيات غير صحيحة! جرب حركة أخرى!')
            elif arguments[0] == 'pawn':
                row, col, row1, col1, char = arguments[1:]
                row, col = int(row) - 1, interpretation.get(col)
                row1, col1 = int(row1) - 1, interpretation.get(col1)
                if board.move_and_promote_pawn(row, col, row1, col1, char):
                    print('الحركة ناجحة')
                else:
                    print('الإحداثيات غير صحيحة! جرب حركة أخرى!')
            elif arguments[0] == 'castling':
                row, col = map(int, arguments[1:])
                if col == 7 and board.castling7() or col == 0 and board.castling0():
                    print('القلعة ناجحة')
                else:
                    print('لا يمكن القلع')


main()