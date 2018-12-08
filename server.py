import socket
import sys
from message_codes import *
from _thread import *
from struct import pack
from random import randint

DB_users = {
      1 : {'Trainer' : "Paulo Contreras Flores",
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

DB_pokemon = {
        1 : ("pikachu", "Pokémons/1.jpg"),
        2 : ("charizard", "Pokémons/2.jpg"),
        3 : ("mewtwo", "Pokémons/3.jpg"),
        4 : ("bulbasaur", "Pokémons/4.jpg"),
        5 : ("charizard", "Pokémons/5.jpg"),
        6 : ("blastoise", "Pokémons/6.jpg"),
        7 : ("caterpie", "Pokémons/7.jpg"),
        8 : ("rattata", "Pokémons/8.jpg"),
        9 : ("pidgeot", "Pokémons/9.jpg"),
        10 : ("oddish", "Pokémons/10.jpg")
}


              

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
    return "\n".join([str(k) + " : " + v["Trainer"] for k,v in DB_users.items()])

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
    user_id = conn.recv(2)
    if user_id[0] == CHOSEN_ID:
        return user_id[1]
    raise Exception("Esperaba choosen id")

def get_user_pwd(conn):#return a string
    user_pwd = conn.recv(1024)
    if user_pwd[0] == PASSWORD:
        return user_pwd[1:].decode()
    raise Exception("Esperaba PASSWORD")

def send_id_no_encontrado(conn):
    transmit(conn, pack('B', ID_NOT_FOUND))

def send_active_user(conn):
    transmit(conn, pack('B', ACTIVE_USER))

def send_confirmation(conn):
    transmit(conn, pack('B', YES))

def send_pass_no_match(conn):
    transmit(conn, pack('B', PASS_NO_MATCH))

def get_solicitud(conn):
    solicitud = conn.recv(1)
    return bytes_2_int(solicitud)

def choose_random_pokemon():
    return randint(1, len(DB_pokemon))

def send_pokemon_info(conn, pokemon_row):
    info = pack('B', CAPTURING_VERIFICATION) + pack('B', pokemon_row) + DB_pokemon[pokemon_row][0].encode()
    transmit(conn, info)



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
    user_id = -1
    if to_play == YES:
        send_trainers(conn)
        ### GET USER FROM CLIENT
        user_id = get_user_id(conn)
        while user_id not in DB_users.keys() or DB_users[user_id]["Active"]:
            if user_id not in DB_users.keys():
                send_id_no_encontrado(conn)
            elif DB_users[user_id]["Active"]:
                send_active_user(conn)
            user_id = get_user_id(conn)
        DB_users[user_id]["Active"] = True
        send_confirmation(conn)

        ### GET PASSWD FROM CLIENT
        user_pwd  = get_user_pwd(conn)
        while not DB_users[user_id]["Password"] == user_pwd:
            send_pass_no_match(conn)
            user_pwd = get_user_pwd(conn)
        send_confirmation(conn)

        # INICIA CAPTURA DE POKEMON

        solicitud = get_solicitud(conn)
        print(solicitud)
        if solicitud == REQUEST_CAPTURING:
            pokemon_row = choose_random_pokemon()
            send_pokemon_info(conn, pokemon_row)





        #YA SE VA A ACABAR LA CONEXION
        DB_users[user_id]["Active"] = False
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
