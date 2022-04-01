import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import Button, simpledialog


from sintactico import ejecutar_analizador, GROSERIAS

HOST = '127.0.0.1'
PORT = 9090

class Client:

    def __init__(self,host, port) -> None:
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring('Nickname','Ingrese un apodo',parent=msg)
        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.recieve)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.win, text="Censura Chat",bg="lightgray")
        self.chat_label.config(font=("Arial",12))
        self.chat_label.pack(padx=20,pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20,pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Mensaje",bg="lightgray")
        self.msg_label.config(font=("Arial",12))
        self.msg_label.pack(padx=20,pady=5)

        self.input_area = tkinter.Text(self.win,height=3)
        self.input_area.pack(padx=20,pady=5)

        self.btn_send = Button(self.win,text='Enviar',command=self.write_msg)
        self.btn_send.config(font=("Arial",12))
        self.btn_send.pack(padx=20,pady=5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def recieve(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disable')
            except ConnectionAbortedError:
                break
            except :
                print('Error')
                self.sock.close()
                break

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def write_msg(self):
        message_before = self.input_area.get('1.0','end')
        words = ejecutar_analizador(message_before)
        for word, is_valid in words:
            temp_word = word.lower()
            if is_valid:
                message_before = message_before.replace(word,'*'*len(word))
            if temp_word[:-1] in GROSERIAS:
                message_before = message_before.replace(word,'*'*len(word))
        message = f"{self.nickname}: {message_before}\n"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')

if __name__ == '__main__':
    client = Client(HOST,PORT)