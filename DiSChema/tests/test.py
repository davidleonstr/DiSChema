from DiSChema import DiSchema

scheme_nested_list = {
    'users': {
        'type': 'list',
        'required': True,
        'allowed-items': [
            {
                'name': {'type': 'str', 'required': True, 'min-length': 1},
                'age': {'type': 'int', 'required': True, 'min-size': 0},
                'address': {
                    'type': 'dict',
                    'required': False,
                    'schema': {
                        'street': {'type': 'str', 'required': True},
                        'city': {'type': 'str', 'required': True},
                        'coordinates': {
                            'type': 'dict',
                            'required': False,
                            'schema': {
                                'lat': {'type': 'float', 'required': True},
                                'lng': {'type': 'float', 'required': True}
                            }
                        }
                    }
                }
            }
        ]
    }
}

data = {
    'users': [
        {
            'name': 'Juan',
            'age': 90,
            'address': {
                'street': 'Calle 123',
                'city': 'Madrid',
                'coordinates': {
                    'lat': 40.4168,
                    'lng': -3.7038
                }
            }
        }
    ]
}

validator = DiSchema(scheme_nested_list, stop=False)
result = validator.check(data)
print(f"Válido: {result['valid']}")
print(f"Errores: {result['errors']}")