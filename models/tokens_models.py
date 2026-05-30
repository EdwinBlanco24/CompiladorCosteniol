TOKENS = {

    'SEMICOLON': r';',

    'TYPE': r'\b(Entero|Real|Texto|Logico)\b',

    'BOOLEAN': r'\b(Verdadero|Falso)\b',

    'TEXT': r'"[^"]*"',

    'REAL': r'\d+\.\d+',

    'ENTERO': r'\d+',

    'METHOD_CALL': r'Captura\.(Texto|Entero|Real|Logico)\(\)',

    'PRINT_CALL': r'Mensaje\.Texto\(([^)]+)\)',

    'IDENTIFIER': r'[a-zA-Z_]\w*',

    'ASSIGNMENT': r'=',

    'PLUS': r'\+',

    'MINUS': r'-',

    'MULTIPLY': r'\*',

    'DIVIDE': r'/',

    'LPAREN': r'\(',

    'RPAREN': r'\)'
}