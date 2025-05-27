types = {
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'dict': dict,
    'list': list
}

restrictions = {
    'str': {
        'excluded-chars': 'excluded-chars',
        'equal': 'equal',
        'max-length': 'max-length',
        'min-length': 'min-length',
        'allowed-equalities': 'allowed-equalities',
        'excluded-equalities': 'excluded-equalities',
        'allowed-chars': 'allowed-chars'
    },
    'number': {
        'equal': 'equal',
        'max-size': 'max-size',
        'min-size': 'min-size',
        'allowed-equalities': 'allowed-equalities',
        'excluded-equalities': 'excluded-equalities'
    },
    'bool': {
        'equal': 'equal'
    },
    'list': {
        'max-length': 'max-length',
        'min-length': 'min-length',
        'allowed-items': 'allowed-items'
    },
    'dict': {
        'max-length': 'max-length',
        'min-length': 'min-length',
        'allowed-items': 'allowed-items',
        'schema': 'schema'
    },
    'fields': {
        'type': 'type',
        'required': 'required',
        'raise': 'raise',
        'try-transformation': 'try-transformation',
        'default-value': 'default-value'
    }
}