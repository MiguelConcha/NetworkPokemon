IP = 0
WELCOME = 1
PLAYING_QUESTION = 2
TRAINER_LIST = 3
CHOSEN_ID = 4
PASSWORD = 5
DO_NOT_HAVE_POKEMON = 6
REQUEST_CAPTURING = 10
CAPTURING_VERIFICATION = 20
REMAINING_ATTEMPTS = 21
CAPTURED_POKEMON = 22
NO_MORE_ATTEMPTS = 23
YES = 30
NO = 31
TERMINATED_SESSION = 32
POKEMON_LIST = 33
ID_NOT_FOUND = 41
PASS_NO_MATCH = 42
ALREADY_HAVE_POKEMON = 43
ALREADY_HAVE_ALL = 44
ACTIVE_USER = 45
TIMEOUT = 46
IMAGE_RECEIVED = 33


def bytes_2_int(byte_repr):
    """
    Convierte un flujo de bytes a un entero

    Args:
      byte_repr: Arreglo de bytes

    Returns:
        (int) Regresa la conversión de bytes a entero.
    """
    return int.from_bytes(byte_repr, byteorder='little', signed=True)
