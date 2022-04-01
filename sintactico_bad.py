import ply.lex as lex
import ply.yacc as yacc
from tkinter import Entry, Tk, Label, Button, font

IS_VALID = False

GROSERIAS = ['puto','chinga','chingada madre','puta','mierda','pendejo'
            ,'pendeja','puta madre','verga','maldito','chinga tu madre','chinga'
            ,'su puta','a la madre','alv','alm','ptm','sptm','idiota'
            ,'imbecil','imbécil','mames','mamando','mamón','mamador',
            'pedo','pedos','joder','jode','jodiendo','jodas','jodido','jodida',
            'chingar','chingando','chingada','chingón','chingon']

tokens = [
    'TLD',
    'PUNTO',
    'ARROBA',
    'ORGANIZACION',
    'PROTOCOLO',
    'NAMECURP',
    'PALABRA',
    'DATE',
    'SEXO',
    'CONSONANTES',
    'NUMAS',
    'SLASH',
    'ENTIDAD',
    'EMISOR',
    'NUMBANCO',
    'NUMCUENTA',
    'DIGSEG'
]

t_TLD = r'\.com'
t_PUNTO = r'\.'
t_ARROBA = r'@'
t_PROTOCOLO = r'https:|http:'
t_SLASH = r'/'
t_ORGANIZACION = r'gmail|outlook|hotmail'

t_NAMECURP = r'[A-Z]{4}(?=\d{4})'
t_DATE = r'\d{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])'
t_PALABRA = r'[a-zA-Z0-9]+'
t_SEXO = r'(?<=\d{4})H|M(?=[A-Z]{6})'
t_CONSONANTES = r'(?<=\d{4}(H|M)[A-Z]{2})[A-Z]{4}(?=\d)'
t_NUMAS = r'(?<=\d{4}(H|M)[A-Z]{2}[A-Z]{4})\d'
t_ENTIDAD = r'(?<=\d{4}(H|M))[A-Z]{2}(?=[A-Z]{4})'

t_EMISOR = r'\d(?=\d{5}\d{6}\d{4})'
t_NUMBANCO = r'(?<=\d)\d{5}(?=\d{6}\d{4})'
t_NUMCUENTA = r'(?<=\d\d{5})\d{6}(?=\d{4})'
t_DIGSEG = r'(?<=\d\d{5}\d{6})\d{4}'

t_ignore = ' '
def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

def t_error(t):
   print(f"Token inválido: {t.value[0]}")
   t.lexer.skip(1)

lexer = lex.lex()

def p_start(p):
    'comando : entrada'

def p(p):
    'entrada : PROTOCOLO SLASH SLASH dominioweb TLD SLASH'
    global IS_VALID
    IS_VALID = True

def p_dominio_web(p):
    'dominioweb : PALABRA PUNTO PALABRA'


def p_correo(p):
    'entrada : PALABRA ARROBA dominio'
    global IS_VALID
    IS_VALID = True


def p_dominio_correo(p):
    'dominio : ORGANIZACION TLD'

def p_curp(p):
    'entrada : NAMECURP DATE SEXO ENTIDAD CONSONANTES NUMAS'
    global IS_VALID
    IS_VALID = True


def p_tarjeta(p):
    'entrada : EMISOR NUMBANCO NUMCUENTA DIGSEG'
    global IS_VALID
    IS_VALID = True


def p_error(p):
    if p is not None:
        error = f"Error de sintáxis en el carácter número: {p.lexpos+1}."
    else:
        error = 'Token inválido'
        print('No se censura')
    global IS_VALID
    IS_VALID = False

    

parser = yacc.yacc()

words = []

def ejecutar_analizador(contenido):
    contenido = contenido.split(' ')
    for word in contenido:
        parser.parse(word)
        lexer.input(word)
        if IS_VALID:
            print('Se censura')
        words.append((word,IS_VALID))
        
    return words

        
        


    