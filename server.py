import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def recieve():
    while True:
        client, address = server.accept()
        print(f'Conectado con {str(address)}')
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f'El nickname del cliente es {nickname}')
        broadcast(f'{nickname} se ha conectado al servidor!\n'.encode('utf-8'))
        client.send("Conectado al servidor".encode('utf-8'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} dice: f{message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

if __name__ == '__main__':
    print('Servidor corriendo...')
    recieve()