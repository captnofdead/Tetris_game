from sly import Lexer
from sly import Parser


class CCLangLexer(Lexer):
    tokens = {WHITESPACE, KEY_CONSTANTS, DIGIT, EQUAL, COMPARISON, PLUS, MINUS, DIVIDE, MULTIPLY, MOD, AND, OR, NOT,
              LEFT_PAR, RIGHT_PAR, LEFT_CPAR, RIGHT_CPAR, NEWLINE, COMMENTS, COMMA, COLON, PIECE_ID, ID,
              NUMBER, BOARD, PIECE, FUNCTION, CONTROLS, ACTION, ON, OFF, DEF, FOR, WHILE, IF, ELSE, BREAK, CONTINUE,
              RETURN, GAME_MODE, KEY_CONTROL, SPEED_CONTROL, ORIENTATION, HORIZON, SCORE, INIT_BOARD, STRING, LETTER}
    # Ignoring tab spaces
    ignore = ' \t'
    # literals = {'=', '+', '-', '*', '/', '(', ')'}
    literals = {'[', ']'}

    # Tokens
    # # KEYWORDS
    BOARD = r'BOARD'
    PIECE = r'PIECE'
    CONTROLS = r'CONTROLS'
    ACTION = r'ACTION'
    FUNCTION = r'FUNCTION'
    ON = r'ON'
    OFF = r'OFF'
    DEF = r'def'

    # #FLOW CONTROLS
    FOR = r'for'
    WHILE = r'while'
    IF = r'if'
    ELSE = r'else'
    BREAK = r'break'
    CONTINUE = r'continue'
    RETURN = r'return'

    # #GAME_CONTROL
    GAME_MODE = r'GAME_MODE'
    KEY_CONTROL = r'config_left|config_right|config_rotc|config_rotac'
    SPEED_CONTROL = r'set_speed'
    ORIENTATION = r'game_orientation'
    HORIZON = r'horizon'
    SCORE = r'score'
    INIT_BOARD = r'INIT_BOARD'

    # #IDENTIFIERS
    ID = r'[a-zA-Z][a-zA-Z|0-9]*'
    PIECE_ID = r'@[a-zA-Z][a-zA-Z|0-9]*'

    # #LITERALS
    STRING = r'"[a-zA-Z]*[0-9]*"'
    NUMBER = r'[0-9][0-9]*'
    ## SHOULD WE DO THIS YA NO PLEASE TELL CROW
    #NUMBER['0'] = DIGIT

    LETTER = r'[a-zA-Z]'
    # DIGIT = r'[0-9]'
    KEY_CONSTANTS = r'UP_ARROW|DOWN_ARROW|LEFT_ARROW|RIGHT_ARROW'

    # #OPERATORS
    COMPARISON = r'<=?|>=?|=='
    EQUAL = r'='
    PLUS = r'\+'
    MINUS = r'-'
    DIVIDE = r'/'
    MULTIPLY = r'\*'
    MOD = r'%'
    AND = r'&&'
    OR = r'\|\|'
    NOT = r'!'

    # #PARANTHESIS
    LEFT_PAR = r'\('
    RIGHT_PAR = r'\)'
    LEFT_CPAR = r'\{'
    RIGHT_CPAR = r'\}'

    # #WHITESPACE
    WHITESPACE = r'[\t |]'
    NEWLINE = r'\n'

    # #COMMENTS
    COMMENTS = r'#!.*'

    # #PUNCTUATIONS
    COMMA = r','
    COLON = r':'

    # Function to interpret digits
    @_(r'[0-9]')
    def DIGIT(self, t):
        t.value = int(t.value)
        return t

    # Function to interpret board
    @_(r'BOARD')
    def BOARD(self, t):
        return t

    # Function to interpret Piece _ID
    @_(r'@[a-zA-Z][a-zA-Z|0-9]*')
    def PIECE_ID(self, t):
        t.value = strToArr(str(t.value))
        return t

    # Function for interpreting numbers
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'"[a-zA-Z]*[0-9]*"')
    def STRING(self, t):
        t.value = str(t.value)
        return t

    # Function for interpreting a newline
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')
        return t

    @_(r'#!.*')
    def COMMENTS(self, t):
        pass

    # Illegal character Error
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    # #Special Cases for LEXER TO HANDLE
    # ID['if'] = IF
    # ID['else'] = ELSE


# Functions to set predefined pieces
def strToArr(yyval):
    s = yyval[1:]
    arr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    if s[0] == 's' and len(s) > 1:
        arr = [[1, 1, 0, 0],
               [1, 1, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    elif s[0] == 'z':
        arr = [[1, 1, 0, 0],
               [0, 1, 1, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    elif s[0] == 't':
        arr = [[1, 1, 1, 0],
               [0, 1, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    elif s[0] == 'li':
        arr = [[1, 1, 1, 1],
               [0, 0, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    elif s[0] == 'l':
        arr = [[1, 0, 0, 0],
               [1, 0, 0, 0],
               [1, 1, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    elif s[0] == 'j':
        arr = [[0, 1, 0, 0],
               [0, 1, 0, 0],
               [1, 1, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    elif s[0] == 's':
        arr = [[0, 1, 1, 0],
               [1, 1, 0, 0],
               [0, 0, 0, 0],
               [0, 0, 0, 0]]
        return s[0] + str(arr)
    return s[0] + str(arr)

