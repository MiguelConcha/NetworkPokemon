# -*- coding: utf-8 -*-

import argparse
import socket
import sys
from struct import pack
from message_codes import *
import tableprint as tp

welcome_banner = """
    _.----.        ____         ,'  _\   ___    ___     ____
_,-'       `.     |    |  /`.   \,-'    |   \  /   |   |    \  |`.
\      __    \    '-.  | /   `.  ___    |    \/    |   '-.   \ |  |
 \.    \ \   |  __  |  |/    ,','_  `.  |          | __  |    \|  |
   \    \/   /,' _`.|      ,' / / / /   |          ,' _`.|     |  |
    \     ,-'/  /   \    ,'   | \/ / ,`.|         /  /   \  |     |
     \    \ |   \_/  |   `-.  \    `'  /|  |    ||   \_/  | |\    |
      \    \ \      /       `-.`.___,-' |  |\  /| \      /  | |   |
       \    \ `.__,'|  |`-._    `|      |__| \/ |  `.__,'|  | |   |
        \_.-'       |__|    `-._ |              '-.|     '-.| |   |
                                `'                            '-._|"""


class Client:
    """
    Clase hace el manejo del cliente con el servidor por medio de un socket.

    Args:
        host: El host con el que se va comunicar el socket.
        port: El puerto con el que se va comunicar el socket.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self._create_socket()

    def _create_socket(self):
        """
        Crear un INET, STREAMing socket que será usado para la 
        comunicación con el servidor.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Socket creation failed")
            sys.exit()
        print("Socket creation complete")
        return s

    def connect(self):
        """
        El socket se conecta al host y al puerto.
        """
        self.socket.connect((self.host, self.port))
        print("Connected to " + self.host)

    def receive_welcome(self):
        """
        Mostrar mensaje de bienvenida que es enviado por el servidor.
        """
        reply = self.socket.recv(1)
        if bytes_2_int(reply) == WELCOME:
            print(welcome_banner)

    def commence_protocol(self):
        """
        Iniciailiza la conexión con el prótocolo para iniciar la captura
        de pokemones.
        """
        reply = self.socket.recv(1)
        reply = bytes_2_int(reply)
        if reply == PLAYING_QUESTION:
            answer_from_client = ""
            while answer_from_client != "y" and answer_from_client != "n":
                answer_from_client = input(
                    "Quieres capturar un pokémon? (y/n): ")
            if answer_from_client == "n":
                self.socket.sendall(pack('B', NO))
                self.receive_session_termination()
            elif answer_from_client == "y":
                self.socket.sendall(pack('B', YES))
                self.receive_list()

    def receive_list(self):
        """
        Recibe la lista personas con las que se jugará.
        """
        reply = self.socket.recv(4096)
        if reply[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if reply[0] == TRAINER_LIST:
            decision = 100
            first = True
            while not self.confirmed_id(decision, first):
                print(reply[1:].decode())
                decision = int(
                    input("Elige el ID de usuario que te corresponde: "))
                if first:
                    first = False

    def confirmed_id(self, decision, first):
        """
        Confirma identificador.

        Args:
            decision: Identificador de la decisión.
            first: Si el usuario ya corresponde a un entrenador.

        Returns:
            (bool) Su el identificador ya fue confirmado.
        """
        self.socket.sendall(pack('B', CHOSEN_ID) + pack('B', decision))
        print("Mandando ID...")
        reply = self.socket.recv(1)
        if reply[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if bytes_2_int(reply) == ID_NOT_FOUND:
            if not first:
                print("No se encontró el ID especificado en la base de datos.")
            return False
        elif bytes_2_int(reply) == YES:
            if not first:
                print("El ID fue encontrado en la base de datos.")
                self.input_password()
            return True
        elif bytes_2_int(reply) == ACTIVE_USER:
            if not first:
                print(
                    "El ID del usuario corresponde a un entrenador que ya está activo.")
            return False

    def verify_pokemon(self, id_p):
        """
        Verifica si el identificaor del pokemon es válido.

        Args:
          id_p: Identificador del pokemon.
        """
        if id_p > 9 or id_p < 1:
            self.close_connection()
            print("Ocurrió un error de transporte con el socket.")

    def verify_img_code(self, code):
        """
        Verifica si el código el código es de una imagen.

        Args:
          code: Código de la imágen.
        """
        if bytes_2_int(code) == -119:
            self.close_connection()
            print("Ocurrió un error de transporte con el socket.")

    def input_password(self):
        """
        Le pide al usuario su contraseña.
        """
        first = True
        password = ""
        while not self.password_confirmed(password, first):
            password = input("Contraseña: ")
            first = False

    def password_confirmed(self, password, first):
        """
        Verifica la contraseña para así permitir el acceso al juego.

        Args:
            password: Contraseña del usuario
            first: Si es la primera vez que estaba dentro

        Returns:
            (bool) Si pudo acceder a jugar.
        """
        self.socket.sendall(pack('B', PASSWORD) + password.encode())
        reply = self.socket.recv(1)
        if reply[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        print("Recibí respuesta")
        if bytes_2_int(reply) == PASS_NO_MATCH:
            if not first:
                print("No coincide la contraseña.")
            return False
        elif bytes_2_int(reply) == YES:
            if not first:
                print("Estás dentro.")

                self.receive_captured_list()

                self.request_capturing()
            return True

    def request_capturing(self):
        """
        Pide que se pueda capturar un pokemon.
        """
        self.socket.sendall(pack('B', REQUEST_CAPTURING))
        print("ya mande solicitud")
        self.receive_pokemon_suggestion()

    def receive_pokemon_suggestion(self):
        """
        Le pregunta al usuario si quiere capturar a ese pokemon.
        """
        reply = self.socket.recv(1024)
        if reply[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if reply[0] == CAPTURING_VERIFICATION:
            answer = ""
            while answer != "y" and answer != "n":
                answer = input("Quieres capturar al pokemón " +
                               reply[2:].decode() + "? (y/n): ")
            self.send_capturing_answer(answer)
        else:
            raise Exception("Esperaba CAPTURING_VERIFICATION")

    def send_capturing_answer(self, answer):
        """
        Envía al servidor si sí fue capturado o no el pokemon.

        Args:
            answer: Respuesta de si se ha capturado.
        """
        if answer == "y":
            self.socket.sendall(pack('B', YES))
            self.receive_capturing_validation()
        elif answer == "n":
            self.socket.sendall(pack('B', NO))
            self.receive_session_termination()

    def receive_capturing_validation(self):
        """
        Muestra las posibles opciones sobre la captura de los pokemones
        tales conmo que lo has capturado o no.
        """
        reply = self.socket.recv(1)
        if reply[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if bytes_2_int(reply) == ALREADY_HAVE_ALL:
            print("Ya tenías todos los pokémones. Has completado el juego.")
            self.receive_session_termination()

        elif bytes_2_int(reply) == ALREADY_HAVE_POKEMON:
            print("Ya tienes el pokémon sugerido. Intentaré encontrarte otro.")
            self.receive_pokemon_suggestion()

        elif bytes_2_int(reply) == DO_NOT_HAVE_POKEMON:
            print("Tu pokédex no reconoce a este pokémon. Intenta capturarlo!")
            captured = False
            while not captured:
                captured = self.verify_capture()
                if captured:
                    break
                again = ""
                while again != "y" and again != "n":
                    again = input("Quieres tratar de nuevo? (y/n): ")
                if again == "n":
                    self.socket.sendall(pack('B', NO))
                    self.receive_session_termination()
                elif again == "y":
                    self.socket.sendall(pack('B', YES))
            if captured:
                print("Lo capturaste")
                # imagen
                self.receive_image()
                # self.send_reception_image()
                self.receive_session_termination()

    def send_reception_image(self):
        """
        Muestra un mensaje de que ya envió la imagen.
        """
        print("voy a enviar")

        self.socket.sendall(pack('B', IMAGE_RECEIVED))
        print("ya envié", str(IMAGE_RECEIVED))

    def receive_image(self):
        """
        Recibe la imagen del pokemon que fue enviada por el servidor.
        """
        code = self.socket.recv(1)
        self.verify_img_code(code)
        print("code", code)
        if code[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        idpokemon = bytes_2_int(self.socket.recv(1))
        self.verify_pokemon(idpokemon)
        print("id", idpokemon)
        tam_image = bytes_2_int(self.socket.recv(4))
        #tam_image = self.socket.recv(4)
        f = open(str(idpokemon) + ".png", 'wb')
        l = 1
        while(l):
            l = self.socket.recv(1024)
            # while (l):
            f.write(l)
            #l = self.socket.recv(1024)
        print("Se guardó una imagen del pokémon capturado en el archivo " +
              str(idpokemon) + ".png.")
        f.close()

        print("Sesión terminada.")
        reply = self.socket.recv(1)
        self.close_connection()

    def receive_captured_list(self):
        """
        Muestra los pokemones capturados del socket.
        """
        reply = self.socket.recv(4096)
        print(reply)
        # if reply[0] == POKEMON_LIST:
        tp.banner("Pokédex")
        print(reply[1:].decode())

    def verify_capture(self):
        """
        Verifica si se capturó un pokmeon.

        Returns:
            (bool) Si se capturó un pokmeon.
        """
        reply = self.socket.recv(3)
        if reply[0] == TIMEOUT:
            print("Ocurrió un timeout en la conexión")
            self.close_connection()
        if reply[0] == REMAINING_ATTEMPTS:
            print("No lo capturaste. Te quedan " +
                  str(reply[-1]) + " intentos.")
            return False
        elif reply[0] == CAPTURED_POKEMON:
            return True
        elif reply[0] == NO_MORE_ATTEMPTS:
            print("Se acabaron los intentos.")
            reply = self.socket.recv(1)
            self.close_connection()

    def receive_session_termination(self):
        """
        Recibe por el socket el estado de que la sesión ya se ha terminado
        """
        reply = self.socket.recv(1)
        if bytes_2_int(reply) == TERMINATED_SESSION or bytes_2_int(reply) == TIMEOUT:
            print(reply)
            print("Sesión terminada: " +
                  ("timeout" if bytes_2_int(reply) == TIMEOUT else ""))
            self.close_connection()
        else:
            raise Exception("Esperaba TERMINATION")

    def close_connection(self):
        """
        Cierra la conexión con el socket.
        """
        self.socket.close()
        print("Conexión cerrada.")
        exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, help='Dirección del host')
    args = parser.parse_args()
    host_arg = args.host
    host = 'localhost' if host_arg is None else host_arg

    client = Client(host, 9999)
    client.connect()

    client.receive_welcome()
    client.commence_protocol()
