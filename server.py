import socket
import sys
from message_codes import *
from _thread import *
from struct import pack

DB = {1 : {'Trainer' : "Paulo Contreras Flores",
           'Password' : "paulo",
           'Active': False},
      2 : {'Trainer' : "Virgilio Castro Rendón",
           'Password' : "virgilio",
           'Active': False},
      3 : {'Trainer' : "José Daniel Campuzano Barajas",
           'Password' : "daniel",
           'Active': False},
      4 : {'Trainer' : "Andrés Flores Martínez",
           'Password' : "andres",
           'Active': False},
      5 : {'Trainer' : "Ángel Iván Gladín García",
           'Password' : "angel",
           'Active': False},
      6 : {'Trainer' : "Miguel Concha Vázquez",
           'Password' : "miguel",
           'Active': False}}

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_socket(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.settimeout(60)
        except socket.error:
            print("Error en el binding.")
            sys.exit()
        print("Binding completado.")

    def listen_socket(self):
        self.socket.listen(5)
        print("El socket está listo.")

    def serve(self):
        while True:
            conn, addr = self.socket.accept()
            print("Conexión con: " + addr[0] + ":" + str(addr[1]))
            start_new_thread(clientthread, (conn,))
    
def transmit(conn, message):
    conn.sendall(message)

def get_trainers():
    return "\n".join([str(k) + " : " + v["Trainer"] for k,v in DB.items()])

def send_welcome_message(conn):
    transmit(conn, pack('B', WELCOME))

def send_pregunta_juego(conn):
    transmit(conn, pack('B', PLAYING_QUESTION))

def get_answer_to_play(conn):
    return bytes_2_int(conn.recv(1))

def terminate_session(conn):
    transmit(conn, pack('B', TERMINATED_SESSION))

def send_trainers(conn):
    transmit(conn, pack('B', TRAINER_LIST) + get_trainers().encode())

def get_user_id(conn):
    user_id = conn.recv(1)
    return bytes_2_int(user_id)

def send_id_no_encontrado(conn):
    transmit(conn, pack('B', ID_NOT_FOUND))

def send_active_user(conn):
    transmit(conn, pack('B', ACTIVE_USER))

def send_id_found(conn):
    transmit(conn, pack('B', YES))

def clientthread(conn):
    """
    msg = "hola\n"
    transmit(conn, msg.encode())
    clientreply = conn.recv(1024).decode()
    print(clientreply)
    """
    send_welcome_message(conn)
    send_pregunta_juego(conn)
    to_play =  get_answer_to_play(conn)
    if to_play == YES:
        send_trainers(conn)
        user_id = get_user_id(conn)
        while user_id not in DB.keys() or DB[user_id]["Active"]:
            print(user_id)
            if user_id not in DB.keys():
                send_id_no_encontrado(conn)
            elif DB[user_id]["Active"]:
                send_active_user(conn)
            user_id = get_user_id(conn)
        DB[user_id]["Active"] = True
        send_id_found(conn)

    elif to_play == NO:
        print("no quiere jugar")
        terminate_session(conn)
        conn.close()
        print("se cerró la conexión")
        
    

if __name__ == '__main__':
    server = Server('', 9999)
    server.bind_socket()
    server.listen_socket()
    server.serve()
