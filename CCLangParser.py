from sly import Lexer
from sly import Parser
import CCLangLexer
from CCLangLexer import CCLangLexer

Symbol_table_func = list()
Symbol_table_func_call = list()
Symbol_table_var = dict()


class CCLangParser(Parser):
    tokens = CCLangLexer.tokens
    # Precedence rules to handle math equations
    precedence = (
        ('left', PLUS, MINUS),
        ('left', MULTIPLY, DIVIDE),
    )

    def __init__(self):
        self.env = {}

    # GRAMMER for SECTION
    @_('BOARD COLON EXPR1',
       'CONTROLS COLON EXPR2',
       'PIECE COLON EXPR3',
       'ACTION COLON EXPR4',
       'FUNCTION COLON EXPR5')
    def Section(self, p):
        if str(p[0]) == "BOARD":
            return p.EXPR1
        elif str(p[0]) == "CONTROLS":
            return p.EXPR2
        elif str(p[0]) == "PIECE":
            return p.EXPR3
        elif str(p[0]) == "ACTION":
            return p.EXPR4
        elif str(p[0]) == "FUNCTION":
            return p.EXPR5

# //////////---EXPR 1 Grammer---//////////////
    @_('NUMBER NUMBER NEWLINE')
    def EXPR1(self, p):
        a = "vars.NUM_COLS = " + str(p[0])
        b = "vars.NUM_ROWS = " + str(p[1])
        c = "import tetris_game as tt"
        d = "from tetris_game import start_game"
        return a + "\n" + b + "\n" + c + "\n" + d

# //////////---EXPR2 Grammer---///////////////
    @_('GAME_CONTROLS EQUAL CONSTANT COMMA EXPR2')
    def EXPR2(self, p):
        if p[0] == "init_board":
            return p.GAME_CONTROLS + str(p[2]) +")) \n" + str(p[4])
        return p.GAME_CONTROLS + str(p[2]) +"\n" + str(p[4])

    @_('GAME_CONTROLS EQUAL CONSTANT NEWLINE')
    def EXPR2(self, p):
        if p[0] == "init_board":
            return p.GAME_CONTROLS + str(p[2]) +")) \n"
        return p.GAME_CONTROLS + str(p[2])

    @_('GAME_CONTROLS EQUAL CONSTANT')
    def EXPR2(self, p):
        if p[0] == "init_board":
            return p.GAME_CONTROLS + str(p[2]) +")) \n"
        return p.GAME_CONTROLS + str(p[2])

# //////////---EXPR 2 GAME_CONTROLS Grammer---//////////////
    @_('GAME_MODE')
    def GAME_CONTROLS(self, p):
        return "tt.GAME_MODE = "

    @_('KEY_CONTROL')
    def GAME_CONTROLS(self, p):
        if str(p[0]) == "config_left":
            a = "tt.MOVE_LEFT = pygame.K_"
            return a
        elif str([p[0]]) == "config_right":
            a = "tt.MOVE_RIGHT = pygame.K_"
            return a
        elif str([p[0]]) == "rot_c":
            a = "tt.ROT_C = pygame.K_"
            return a
        else:
            a = "tt.ROT_AC = pygame.K_"
            return a

    @_('SPEED_CONTROL')
    def GAME_CONTROLS(self, p):
        return "tt.FALL_SPEED ="

    @_('ORIENTATION')
    def GAME_CONTROLS(self, p):
        pass

    @_('HORIZON')
    def GAME_CONTROLS(self, p):
        return "tt.HORIZON = "

    @_('SCORE')
    def GAME_CONTROLS(self, p):
        return "tt.SCORE = "

    @_('INIT_BOARD')
    def GAME_CONTROLS(self, p):
        return "tt.init_board =" + p[0][10:]

# //////////---EXPR 2 CONSTANT Grammer---//////////////
    @_('DIGIT', 'NUMBER', 'STRING')
    def CONSTANT(self, p):
        return str(p[0])

    @_('ID')
    def CONSTANT(self, p):

        if (Symbol_table_var.has_key(p.ID)):
            return str(Symbol_table_var[p.ID])
        else:
            perror("Variable not declared")

    @_('KEY_CONSTANTS')
    def CONSTANT(self, p):
        return str(p[0])


# //////////---EXPR 3 Grammer---//////////////
    @_('PIECE_ID COMMA EXPR3')
    #       'CUSTOM_PIECE EQUAL ARRAY')
    def EXPR3(self, p):
        a = str(p[0])
        a = a[0:1]
        return "tt." + str(a).upper() + " = 1" + "\n" + str(p[2])

    @_('PIECE_ID COMMA')
    def EXPR3(self, p):
        a = str(p[0])
        a = a[0:1]
        return "tt." + str(a).upper() + " = 1" + "\n"

    @_('PIECE_ID NEWLINE')
    def EXPR3(self, p):
        a = str(p[0])
        a = a[0:1]
        return "tt." + str(a).upper() + " = 1" + "\n"

    @_('PIECE_ID')
    def EXPR3(self, p):
        a = str(p[0])
        a = a[0:1]
        return "tt." + str(a).upper() + " = 1" + "\n"

    @_('PIECE_ID EQUAL STRING COMMA EXPR3')
    def EXPR3(self, p):
        a = "[\""
        b = str(p[2])
        b = b[1:len(b) - 1]
        FLAG = 0
        for i in range(0, len(b) - 1):
            a = a + str(b[i])
            if i % 4 == 3 and i != len(b) - 1 and i != 0:
                a = a + "\", \""
            else:
                a = a + ""
        cus_arr = a + b[len(b) - 1] + "\"]"
        x = "cus_arr = " + cus_arr + "\n"
        y = "tt.shapes.append(cus_arr)" + "\n"
        z = "tt.shape.append([cus_arr, tt.rotate(cus_arr), tt.rotate(tt.rotate(cus_arr)), tt.rotate(tt.rotate(tt.rotate(cus_arr)))])"
        return x + y + z + str(p[4])

    @_('PIECE_ID EQUAL STRING NEWLINE')
    def EXPR3(self, p):
        a = "[\""
        b = str(p[2])
        b = b[1:len(b) - 1]
        FLAG = 0
        for i in range(0, len(b)-1):
            a = a + str(b[i])
            if i % 4 == 3 and i != len(b) - 1 and i != 0:
                a = a + "\", \""
            else:
                a = a + ""
        cus_arr = a+b[len(b)-1] + "\"]"
        x = "cus_arr = " + cus_arr + "\n"
        y = "tt.shapes.append(cus_arr)" + "\n"
        z = "tt.shape.append([cus_arr, tt.rotate(cus_arr), tt.rotate(tt.rotate(cus_arr)), tt.rotate(tt.rotate(tt.rotate(cus_arr)))])"
        return x+ y + z


    @_('PIECE_ID EQUAL STRING')
    def EXPR3(self, p):
        a = "[\""
        b = str(p[2])
        b = b[1:len(b) - 1]
        FLAG = 0
        for i in range(0, len(b) - 1):
            a = a + str(b[i])
            if i % 4 == 3 and i != len(b) - 1 and i != 0:
                a = a + "\", \""
            else:
                a = a + ""
        cus_arr = a + b[len(b) - 1] + "\"]"
        x = "cus_arr = " + cus_arr + "\n"
        y = "tt.shapes.append(cus_arr)" + "\n"
        z = "tt.shape.append([cus_arr, tt.rotate(cus_arr), tt.rotate(tt.rotate(cus_arr)), tt.rotate(tt.rotate(tt.rotate(cus_arr)))])"
        return x + y + z

# //////////---EXPR 4 Grammer---//////////////
    @_('ID LEFT_PAR RIGHT_PAR COMMA EXPR4')
    def EXPR4(self, p):
        Symbol_table_func_call.append(str(p[0]) + "()")
        return ""

    @_('ID LEFT_PAR RIGHT_PAR NEWLINE')
    def EXPR4(self, p):
        Symbol_table_func_call.append(str(p[0]) + "()")
        return ""

    @_('ID LEFT_PAR RIGHT_PAR')
    def EXPR4(self, p):
        Symbol_table_func_call.append(str(p[0]) + "()")
        return ""

# //////////---EXPR 5 Grammer---//////////////
    @_('PROCEDURE NEWLINE EXPR5')
    def EXPR5(self, p):
        return str(p[0]) + "\n" + str(p[2])

    @_('empty')
    def EXPR5(self, p):
        return ""

    @_('DEF ID LEFT_PAR RIGHT_PAR LEFT_CPAR FBODY RIGHT_CPAR')
    def PROCEDURE(self, p):
        Symbol_table_func.append(str(p[1]) + "()")
        return str(p[5])

    @_('EXPR2 FBODY')
    def FBODY(self, p):
        return p.EXPR2 + "\n" + str(p[1])

    @_('IF LEFT_PAR BEXPR RIGHT_PAR LEFT_CPAR NEWLINE FBODY NEWLINE RIGHT_CPAR')
    def FBODY(self, p):
        return

    @_('ELSE LEFT_CPAR NEWLINE FBODY NEWLINE RIGHT_CPAR')
    def FBODY(self, p):
        return

    @_('FOR LEFT_PAR EXPR2 EXPR2 EXPR2 RIGHT_PAR LEFT_CPAR NEWLINE FBODY NEWLINE RIGHT_CPAR')
    def FBODY(self, p):
        return

    @_('WHILE LEFT_PAR BEXPR RIGHT_PAR LEFT_CPAR NEWLINE FBODY NEWLINE RIGHT_CPAR')
    def FBODY(self, p):
        return

    @_('CONTINUE', 'BREAK')
    def FBODY(self, p):
        pass

    @_('ID EQUAL AEXPR')
    def FBODY(self, p):
        Symbol_table_var[p.ID] = p.AEXPR
        return ""

    @_('ID EQUAL BEXPR')
    def FBODY(self, p):
        return

    @_('RETURN')
    def FBODY(self, p):
        return ""

    @_('AEXPR PLUS term')
    def AEXPR(self, p):
        return p.AEXPR + p.term

    @_('AEXPR MINUS term')
    def AEXPR(self, p):
        return p.AEXPR - p.term

    @_('term')
    def AEXPR(self, p):
        return p.term

    @_('term MULTIPLY factor')
    def term(self, p):
        return p.term * p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.term / p.factor

    @_('term MOD factor')
    def term(self, p):
        return p.term % p.factor

    @_('term COMPARISON factor')
    def term(self, p):
        return p.term < p.factor

    @_('factor')
    def term(self, p):
        return p.factor

    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('LEFT_PAR AEXPR RIGHT_PAR')
    def factor(self, p):
        return p.AEXPR

    @_('NOT ID', 'ID BOOL_OP ID', 'ON', 'OFF')
    def BEXPR(self, p):
        return

    @_('AND', 'OR')
    def BOOL_OP(self, p):
        return

    @_('')
    def empty(self, p):
        pass

    @_('COMMENTS', 'WHITESPACE', 'LETTER')
    def Section(self):
        pass

if __name__ == '__main__':
    lexer = CCLangLexer()
    parser = CCLangParser()

    with open('game.py', 'w') as f:
        print('import pygame', file=f)
        print('import vars', file=f)

    with open('cclang_script.txt.', 'r') as g:
        for line in g:
            print(line)
            try:
                result1 = lexer.tokenize((str(line)))
                #for res in result1:
                #    print(res)
                result = parser.parse(lexer.tokenize(str(line)))
                with open('game.py', 'a') as f:
                    f.write(f"{result}\n")
            except EOFError:
                break
    with open('game.py', 'a') as f:
        print('start_game()', file=f)
