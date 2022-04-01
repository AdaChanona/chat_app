import ply.lex as lex
import ply.yacc as yacc
from tkinter import Entry, Tk, Label, Button, font


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
    label_resultado['text'] = 'Es válido'
    label_resultado['fg'] = '#46BE51'

def p_dominio_web(p):
    'dominioweb : PALABRA PUNTO PALABRA'
    label_resultado['text'] = 'Es válido'
    label_resultado['fg'] = '#46BE51'

def p_correo(p):
    'entrada : PALABRA ARROBA dominio'
    label_resultado['text'] = 'Es válido'
    label_resultado['fg'] = '#46BE51'

def p_dominio_correo(p):
    'dominio : ORGANIZACION TLD'

def p_curp(p):
    'entrada : NAMECURP DATE SEXO ENTIDAD CONSONANTES NUMAS'
    label_resultado['text'] = 'Es válido'
    label_resultado['fg'] = '#46BE51'

def p_tarjeta(p):
    'entrada : EMISOR NUMBANCO NUMCUENTA DIGSEG'
    label_resultado['text'] = 'Es válido'
    label_resultado['fg'] = '#46BE51'

def p_error(p):
    if p is not None:
        error = f"Error de sintáxis en el carácter número: {p.lexpos+1}."
    else:
        error = 'Token inválido'
    label_resultado['text'] = error
    label_resultado['fg'] = '#FF0000'
    

parser = yacc.yacc()

def ejecutar_analizador():
    contenido = my_text.get()
    parser.parse(contenido)
    lexer.input(contenido)
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)

if __name__ == '__main__':
    root = Tk()
    root.geometry('640x480')
    root.title('Analizadores')

    my_text = Entry(root,width=50,font=font.Font(size=13))
    my_text.place(x=0,y=50)

    btn_analizar = Button(root, text='Analizar', font=font.Font(size=13), width=10, command=ejecutar_analizador)
    btn_analizar.place(x=500,y=100)

    label_resultado = Label(root,text='',font=font.Font(size=15), width=40, fg='#46BE51')
    label_resultado.place(x=50,y=300)

    root.mainloop()

    