import pickle

DB_users = {
    1: {'Trainer': "Paulo Contreras Flores",
        'Password': "paulo",
        'Active': False,
        'Catched': []},
    2: {'Trainer': "Virgilio Castro Rendón",
        'Password': "virgilio",
        'Active': False,
        'Catched': []},
    3: {'Trainer': "José Daniel Campuzano Barajas",
        'Password': "daniel",
        'Active': False,
        'Catched': []},
    4: {'Trainer': "Andrés Flores Martínez",
        'Password': "andres",
        'Active': False,
        'Catched': []},
    5: {'Trainer': "Ángel Iván Gladín García",
        'Password': "angel",
        'Active': False,
        'Catched': []},
    6: {'Trainer': "Miguel Concha Vázquez",
        'Password': "miguel",
        'Active': False,
        'Catched': []}}


def save_obj(obj, name):
    """
      Serializa un objeto para guardarlo en memoria.

    Args:
      obj: El objeto a guardar.
      name: El nombre de como se va a guardar el objeto que se serializó.
    """
    with open('DB/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
    save_obj(DB_users, "db")
