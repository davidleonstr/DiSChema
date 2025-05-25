from DiSChema import DiSchema

scheme = {
    'field_1': {
        'type': 'str',
        'max_length': 6
    },
    'field_2': {
        'type': 'int',
        'max_size': 5
    },
    'field_3': {
        'type': 'int',
        'min_size': 2
    },
    'field_4': {
        'type': 'int',
        'max_size': 5,
        'min_size': 1
    }
}

data = {
    'field_1': 'hello',
    'field_2': 4,
    'field_3': 7,
    'field_4': 9
}

test_scheme = DiSchema(scheme)

result = test_scheme.check(data)

print(str(result))