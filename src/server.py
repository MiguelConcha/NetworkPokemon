# -*- coding: utf-8 -*-

import socket
import os
import sys
from message_codes import *
from _thread import *
from struct import pack
from random import randint
from socket import timeout
import pickle

DB_pokemon = {
    1: ("pikachu", "assets/1.png"),
    2: ("charizard", "assets/2.png"),
    3: ("mewtwo", "assets/3.png"),
    4: ("bulbasaur", "assets/4.png"),
    5: ("squirtle", "assets/5.png"),
    6: ("blastoise", "assets/6.png"),
    7: ("caterpie", "assets/7.png"),
    8: ("pidgeot", "assets/8.png"),
    9: ("oddish", "assets/9.png")
}

def load_obj(name):
    """Carga la base de datos que es un diccionario.

    Args:
        name: Nombre de la base de datos

    Returns:
        El objeto que se serializó.

    """
    with open('DB/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_obj(obj, name):
    """Serializa un diccionario que guarda el estdo actual de la base de datos.

    Args:
        obj: Diccionario a serializar.
        name: El nombre de la base de datos.
    """
    with open('DB/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


class Server:
    """Clase que manejara la conexión del servidor, así como actualizar
    los estados del socket usado.

    Args:
        host: La dirección con la que se hará la conexión.
        port: El puerto en el que se llevará la comunicación.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bind_socket(self):
        """
        Hace un enlace usando el soccket.
        """
        try:
            self.socket.bind((self.host, self.port))
            # self.socket.settimeout(600)
        except socket.error:
            print("Error en el binding.")
            sys.exit()
        print("Binding completado.")

    def listen_socket(self):
        """
        Para activar el socket.
        """
        self.socket.listen(5)
        print("El socket está listo.")

    def serve(self):
        """
        Empezar a efectiar la comunicación.
        """
        while True:
            conn, addr = self.socket.accept()
            conn.settimeout(60)
            print("Conexión con: " + addr[0] + ":" + str(addr[1]))
            start_new_thread(clientthread, (conn,))


def transmit(conn, message):
    """
    Enviar un mensaje.

    Args:
      conn: Un objeto socket que es usado para enviar/recibir información
      message: Mensaje o código de envío.
    """
    conn.sendall(message)


def get_trainers():
    """ 
    Obtener entrenadores en una cadena formateada

    Returns:
        Un (str) con los entrenadores de la base de datos.
    """
    return "\n".join([str(k) + " : " + v["Trainer"] for k, v in DB_users.items()])


def send_welcome_message(conn):
    """
    Envía mensaje de bienvenida por medio de un socket.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', WELCOME))


def send_pregunta_juego(conn):
    """
    Envía un pregunta por medio de un socket.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', PLAYING_QUESTION))


def get_bool_answer(conn):
    """
    Obtiene la la respuesta que se recibió.

    Args:
        conn: Un socket que es usado para enviar/recibir información.

    Returns:
        (bool) diciendo el esrado que recibió.
    """
    return bytes_2_int(conn.recv(1))


def terminate_session(conn):
    """
    Terminar sersión con el cliente.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', TERMINATED_SESSION))


def send_trainers(conn):
    """
    Enviá entrenadores disponibles.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', TRAINER_LIST) + get_trainers().encode())


def get_user_id(conn):
    """
    Obtiene el identificador del entrenador pokemon.

    Args:
        conn: Un socket que es usado para enviar/recibir información.

    Returns:
        Entrenador escogido.
    """
    user_id = conn.recv(2)
    if user_id[0] == CHOSEN_ID:
        return user_id[1]
    raise Exception("Esperaba choosen id")


def get_user_pwd(conn):
    """
    Obtiene la contraseña del usuario

    Args:
        conn: Un socket que es usado para enviar/recibir información.

    Returns:
        La contraseña de un entrenador.
    """
    user_pwd = conn.recv(1024)
    if user_pwd[0] == PASSWORD:
        return user_pwd[1:].decode()
    raise Exception("Esperaba PASSWORD")


def send_id_no_encontrado(conn):
    """
    Envía por el socket que no que identificador no fue encontrado.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', ID_NOT_FOUND))


def send_active_user(conn):
    """
    Envía por el socket que el usuario está activo.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', ACTIVE_USER))


def send_confirmation(conn):
    """
    Envía por el socket una confirmación del lado del servidor.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', YES))


def send_pass_no_match(conn):
    """
    Envía por el socket que la contraseña no fue válida.

    Args:
      conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', PASS_NO_MATCH))


def get_solicitud(conn):
    """
    Obtiene por el socket la solicitud.

    Args:
        conn: Un socket que es usado para enviar/recibir información.

    Returns:
        (int) El número de la solicitud.
    """
    solicitud = conn.recv(1)
    return bytes_2_int(solicitud)


def choose_random_pokemon():
    """
    Reegresa un número aleatorio entre [1, len(DB_pokemon)].

    Returns:
        (int) Numero positivo entre [1, len(DB_pokemon)].
    """
    return randint(1, len(DB_pokemon))


def send_pokemon_info(conn, pokemon_row):
    """
    Envía por el socket la fila de los pokemones.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
        pokemon_row: la fila de los pokemones.
    """
    info = pack('B', CAPTURING_VERIFICATION) + \
        pack('B', pokemon_row) + DB_pokemon[pokemon_row][0].encode()
    transmit(conn, info)


def send_all_catched(conn):
    """
    Envía por el socket que todos los pokemones fueron capturados.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', ALREADY_HAVE_ALL))


def send_already_have(conn):
    """
    Envía por el socket que ya se tiene al pokemon.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', ALREADY_HAVE_POKEMON))


def send_not_have(conn):
    """
    Envía por el socket que no está el pokemon.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', DO_NOT_HAVE_POKEMON))


def terminate(conn):
    """
    Termina la conexioón con el socket.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    terminate_session(conn)
    conn.close()


def send_attempts(conn, n, pokemon_id):
    """
    Envía el número de intentos con el id del pokemon.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
        pokemon_id: Identificador del pokenon.
        n: Número de intentos.
    """
    package = pack('B', REMAINING_ATTEMPTS) + \
        pack('B', pokemon_id) + pack('B', n)
    transmit(conn, package)


def send_successful_capture(conn):
    """
    Envía por el socket que la captura fue exitosa.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', CAPTURED_POKEMON))


def send_ran_out_of_attempts(conn):
    """
    Envía por el socket que se ha excedido el número de intentos.

    Args:
      conn: Un socket que es usado para enviar/recibir información.
    """
    transmit(conn, pack('B', NO_MORE_ATTEMPTS))


def send_image(conn, pokemon_row):
    """
    Envía por el socket que la imagen del pomekemon.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
        pokemon_row: La fila del pokemon. 
    """
    f = open(DB_pokemon[pokemon_row][1], "rb")
    tam_image = os.stat(DB_pokemon[pokemon_row][1]).st_size
    pack_tam = pack("<L", tam_image)
    #tam_entries = len(tam_image)
    l = f.read(1024)
    # print(l)
    image = l  # pack('B', l)
    while (l):
        l = f.read(1024)
        image += l
    package = pack('B', CAPTURED_POKEMON) + \
        pack('B', pokemon_row) + pack_tam + image
    transmit(conn, package)
    f.close()


def send_captured_pokemons(conn, id_user):
    """
    Envía los pokemones capturados por el socker

    Args:
        conn: Un socket que es usado para enviar/recibir información.
        id_user: Identificador del usuario.
    """
    transmit(conn, pack('B', POKEMON_LIST) +
             ' '.join(DB_users[id_user]['Catched']).encode())


def capture_pokemon(conn, user_id):
    """
    Captura a un pokemon con el identificador del usuario y dice si sí
    lo capturar.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
        user_id: Identificador del usuario.
    """
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
            max_attempts = randint(4, 20)
            while not captured and max_attempts > 1:
                captured = randint(0, 10) == 1
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
                DB_users[user_id]["Catched"].append(DB_pokemon[pokemon_row][0])
                save_obj(DB_users, "db")
                # ENVIAR IMAGEN Y REGISTRAR POKEMON
                send_image(conn, pokemon_row)
                #conf = conn.recv(1)
                # print(conf)
                transmit(conn, pack('B', TERMINATED_SESSION))
                conn.close()
                pass

    elif answer == NO:
        conn.sendall(pack('B', TERMINATED_SESSION))
        conn.close()
        # terminate(conn)


def clientthread(conn):
    """
    Función que va a ser llamada para manejar la conexión de cada cliente.

    Args:
        conn: Un socket que es usado para enviar/recibir información.
    """
    try:
        send_welcome_message(conn)
        send_pregunta_juego(conn)
        to_play = get_bool_answer(conn)
        user_id = -1
        if to_play == YES:
            send_trainers(conn)
            # GET USER FROM CLIENT
            user_id = get_user_id(conn)
            while user_id not in DB_users.keys() or DB_users[user_id]["Active"]:
                if user_id not in DB_users.keys():
                    send_id_no_encontrado(conn)
                elif DB_users[user_id]["Active"]:
                    send_active_user(conn)
                user_id = get_user_id(conn)
            DB_users[user_id]["Active"] = True
            save_obj(DB_users, "db")
            send_confirmation(conn)

            # GET PASSWD FROM CLIENT
            user_pwd = get_user_pwd(conn)
            while not DB_users[user_id]["Password"] == user_pwd:
                send_pass_no_match(conn)
                user_pwd = get_user_pwd(conn)
            send_confirmation(conn)

            send_captured_pokemons(conn, user_id)
            # INICIA CAPTURA DE POKEMON

            solicitud = get_solicitud(conn)
            if solicitud == REQUEST_CAPTURING:
                capture_pokemon(conn, user_id)

            # YA SE VA A ACABAR LA CONEXION
            DB_users[user_id]["Active"] = False
            save_obj(DB_users, "db")
        elif to_play == NO:
            # terminate(conn)
            pac = pack('B', 32)
            conn.sendall(pack('B', 32))
            conn.close()
            print("se cerró la conexión")
    except timeout:
        transmit(conn, pack('B', TIMEOUT))
        conn.close()
        print("timeout")

if __name__ == '__main__':
    DB_users = load_obj("db")
    print(DB_users)

    server = Server('', 9999)
    server.bind_socket()
    server.listen_socket()
    server.serve()
