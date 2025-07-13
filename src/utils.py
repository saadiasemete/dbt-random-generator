import random 

def generate_random_letter():
    A = 65 
    Z = 90
    a = 97
    z = 122
    return chr(random.choice([random.randint(A, Z), random.randint(a, z)]))

def randstr(len: int=16) -> str:
    return ''.join(generate_random_letter() for _ in range(len))

def generate_field_name_type(types: list=['str', 'int', 'float']):
    return {
        'name': randstr(),
        'type': random.choice(types),
    }

def random_piece_of_data(type_: str):
    match type_:
        case 'str':
            return randstr()
        case 'int':
            return random.randint(-127, 128)
        case 'float':
            return random_piece_of_data('int')*random.random()
        case _:
            raise NotImplementedError(type_)