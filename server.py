import socket
import os
import sys
from message_codes import *
from _thread import *
from struct import pack
from random import randint

DB_users = {
      1 : {'Trainer' : "Paulo Contreras Flores",
           'Password' : "paulo",
           'Active': False,
           'Catched': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
      2 : {'Trainer' : "Virgilio Castro Rendón",
           'Password' : "virgilio",
           'Active': False,
           'Catched': [1,2,3,4,5,6,7,8,9]},
      3 : {'Trainer' : "José Daniel Campuzano Barajas",
           'Password' : "daniel",
           'Active': False,
           'Catched': []},
      4 : {'Trainer' : "Andrés Flores Martínez",
           'Password' : "andres",
           'Active': False,
           'Catched': []},
      5 : {'Trainer' : "Ángel Iván Gladín García",
           'Password' : "angel",
           'Active': False,
           'Catched': []},
      6 : {'Trainer' : "Miguel Concha Vázquez",
           'Password' : "miguel",
           'Active': False,
           'Catched': []}}

DB_pokemon = {
        1 : ("pikachu", "Pokémons/1.png"),
        2 : ("charizard", "Pokémons/2.png"),
        3 : ("mewtwo", "Pokémons/3.png"),
        4 : ("bulbasaur", "Pokémons/4.png"),
        5 : ("charizard", "Pokémons/5.png"),
        6 : ("blastoise", "Pokémons/6.png"),
        7 : ("caterpie", "Pokémons/7.png"),
        8 : ("rattata", "Pokémons/8.png"),
        9 : ("pidgeot", "Pokémons/9.png"),
        10 : ("oddish", "Pokémons/10.png")
}


              

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_socket(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.settimeout(600)
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
    print("envio ", message)
    conn.sendall(message)

def get_trainers():
    return "\n".join([str(k) + " : " + v["Trainer"] for k,v in DB_users.items()])

def send_welcome_message(conn):
    transmit(conn, pack('B', WELCOME))

def send_pregunta_juego(conn):
    transmit(conn, pack('B', PLAYING_QUESTION))

def get_bool_answer(conn):
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

def send_all_catched(conn):
    transmit(conn, pack('B', ALREADY_HAVE_ALL))

def send_already_have(conn):
    transmit(conn, pack('B', ALREADY_HAVE_POKEMON))

def send_not_have(conn):
    transmit(conn, pack('B', DO_NOT_HAVE_POKEMON))

def terminate(conn):
    for k,v in DB_users.items():
        print(k, v)
    terminate_session(conn)
    conn.close()

def send_attempts(conn, n, pokemon_id):
    package = pack('B', REMAINING_ATTEMPTS) + pack('B', pokemon_id) + pack('B', n)
    transmit(conn, package)

def send_successful_capture(conn):
    transmit(conn, pack('B', CAPTURED_POKEMON))

def send_ran_out_of_attempts(conn):
    transmit(conn, pack('B', NO_MORE_ATTEMPTS))

def send_image(conn, pokemon_row):
    f = open(DB_pokemon[pokemon_row][1], "rb")
    #tam_image = str(os.stat(DB_pokemon[pokemon_row][1]).st_size)
    #print("el tama;o", tam_image)
    #tam_entries = len(tam_image)
    l = f.read(1024)
    #print(l)
    image = l#pack('B', l)
    while (l):
        l = f.read(1024)
        image += l
    package = pack('B', CAPTURED_POKEMON) + pack('B', pokemon_row) + image
    transmit(conn, package)
    f.close()
    print(bytes_2_int(package))
    print(package)
    
    
    

def capture_pokemon(conn, user_id):
    pokemon_row = choose_random_pokemon()
    send_pokemon_info(conn, pokemon_row)
    answer = get_bool_answer(conn)
    if answer == YES:
        if len(DB_users[user_id]["Catched"]) == len(DB_pokemon):
            send_all_catched(conn)
            terminate(conn)
        elif pokemon_row in DB_users[user_id]["Catched"]:
            send_already_have(conn)
            capture_pokemon(conn, user_id)
        else:
            send_not_have(conn)
            captured = False
            max_attempts = randint(2, 10)
            while not captured and max_attempts > 1:
                captured = randint(0, 2) == 1
                print("lo captura" , captured)
                max_attempts -= 1
                if not captured:
                    send_attempts(conn, max_attempts, pokemon_row)
                    try_again = get_bool_answer(conn)
                    if try_again == NO:
                        break
                else:
                    send_successful_capture(conn)
            if not captured and try_again == YES:
                send_ran_out_of_attempts(conn)
                terminate(conn)
            elif not captured:
                terminate(conn)
            else:
                print("capturado y a terminar")
                DB_users[user_id]["Catched"].append(pokemon_row)
                #ENVIAR IMAGEN Y REGISTRAR POKEMON
                send_image(conn, pokemon_row)
                #conf = conn.recv(1)
                #print(conf)
                transmit(conn, pack('B', TERMINATED_SESSION))
                conn.close()
                pass

    elif answer == NO:
        conn.sendall(pack('B', TERMINATED_SESSION))
        conn.close()
        #terminate(conn)


def clientthread(conn):

    """
    msg = "hola\n"
    transmit(conn, msg.encode())
    clientreply = conn.recv(1024).decode()
    print(clientreply)
    """
    send_welcome_message(conn)
    send_pregunta_juego(conn)
    to_play = get_bool_answer(conn)
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
        if solicitud == REQUEST_CAPTURING:
            capture_pokemon(conn, user_id)

        #YA SE VA A ACABAR LA CONEXION
        DB_users[user_id]["Active"] = False
    elif to_play == NO:
        print("no quiere jugar")
        #terminate(conn)
        pac = pack('B', 32)
        conn.sendall(pack('B', 32))
        conn.close()
        print("se cerró la conexión")
        
    

if __name__ == '__main__':
    server = Server('', 9999)
    server.bind_socket()
    server.listen_socket()
    server.serve()
