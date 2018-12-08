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

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = self._create_socket()

    def _create_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Socket creation failed")
            sys.exit()
        print("Socket creation complete")
        return s

    def connect(self):
        self.socket.connect((self.host, self.port))
        print("Connected to " + self.host)

    def receive_welcome(self):
        reply = self.socket.recv(1)
        if bytes_2_int(reply) == WELCOME:
            print(welcome_banner)

    def commence_protocol(self):
        reply = self.socket.recv(1)
        if bytes_2_int(reply) == PLAYING_QUESTION:
            answer_from_client = ""
            while answer_from_client != "y" and answer_from_client != "n":
                answer_from_client = input("Quieres capturar un pokémon? (y/n): ")
            if answer_from_client == "n":
                self.socket.sendall(pack('B', NO))
                self.receive_session_termination()
            elif answer_from_client == "y":
                self.socket.sendall(pack('B', YES))
                self.receive_list()

    def receive_list(self):
        reply = self.socket.recv(4096)
        if reply[0] == TRAINER_LIST:
            decision = 100
            first = True
            while not self.confirmed_id(decision, first):
                print(reply[1:].decode())
                decision = int(input("Elige el ID de usuario que te corresponde: "))
                if first:
                    first = False
            print("ok")

    def confirmed_id(self, decision, first):
        self.socket.sendall(pack('B', CHOSEN_ID) + pack('B', decision))
        print("Mandando ID...")
        reply = self.socket.recv(1)
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
                print("El ID del usuario corresponde a un entrenador que ya está activo.")
            return False

    def input_password(self):
        first = True
        password = ""
        while not self.password_confirmed(password, first):
            password = input("Contraseña: ")
            first = False
            
    def password_confirmed(self, password, first):
        self.socket.sendall(pack('B', PASSWORD) + password.encode())
        reply = self.socket.recv(1)
        print("Recibí respuesta")
        if bytes_2_int(reply) == PASS_NO_MATCH:
            if not first:
                print("No coincide la contraseña.")
            return False
        elif bytes_2_int(reply) == YES:
            if not first:
                print("Estás dentro.")
                self.request_capturing()
            return True

    def request_capturing(self):
        self.socket.sendall(pack('B', REQUEST_CAPTURING))
        self.receive_pokemon_suggestion()

    def receive_pokemon_suggestion(self):
        reply = self.socket.recv(2)
        if reply[0] == CAPTURING_VERIFICATION:
            print("Quieres capturar al pokemón " + map(reply[1]) + "?")
        raise Exception("Esperaba CAPTURING_VERIFICATION")

    def receive_session_termination(self):
        reply = self.socket.recv(1)
        if bytes_2_int(reply) == TERMINATED_SESSION:
            print("Sesión terminada.")
            self.close_connection()

    def close_connection(self):
        self.socket.close()
        print("Conexión cerrada.")

if __name__ == '__main__':
    
    #host = input("Host: ")
    #port = int(input("Port: "))
    client = Client("192.168.1.66", 9999)
    client.connect()
    
    client.receive_welcome()
    client.commence_protocol()

    
