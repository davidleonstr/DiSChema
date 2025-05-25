from .exceptions import *
from .properties import restrictions

class DiSchema:
    def __init__(self, fields_scheme: dict) -> None:
        self.fields_scheme = fields_scheme
        self.restrictions = restrictions
    
    def check(self, data: dict) -> bool | Exception:
        for field, scheme in self.fields_scheme.items():
            if field not in data:
                return NoFieldError(no_field(field))
            
            if type(data[field]).__name__ != scheme['type']:
                return InvalidTypeError(invalid_type(field, scheme['type']))
            
            if type(data[field]).__name__ == 'str':
                if restrictions['str']['excluded_chars'] in scheme:
                    for char in scheme['excluded_chars']:
                        if char in list(data[field]):
                            return ExcludedCharactersError(excluded_characters(field))
                        
                if restrictions['str']['equal'] in scheme:
                    if data[field] != scheme['equal']:
                        return NoEqualError(no_equal(field, scheme['equal']))

                if restrictions['str']['max_length'] in scheme:
                    if len(data[field]) > scheme['max_length']:
                        return ExcessLengthError(exccess_length(field))
                    
                if restrictions['str']['min_length'] in scheme:
                    if len(data[field]) < scheme['max_length']:
                        return MissingLengthError(missing_length(field))
                    
            if type(data[field]).__name__ == 'int' or type(data[field]).__name__ == 'float':
                if restrictions['number']['equal'] in scheme:
                    if data[field] != scheme['equal']:
                        return NoEqualError(no_equal(field, scheme['equal']))
                    
                if restrictions['number']['max_size'] in scheme:
                    if data[field] > scheme['max_size']:
                        return ExcessSizeError(exccess_size(field))
                    
                if restrictions['number']['min_size'] in scheme:
                    if data[field] < scheme['min_size']:
                        return MissingSizeError(missing_size(field))
                    
            if type(data[field]).__name__ == 'bool':
                if restrictions['bool']['equal'] in scheme:
                    if data[field] != scheme['equal']:
                        return ValueError(f"The field {field} is not equal of '{scheme['equal']}'")
                    
            if type(data[field]).__name__ == 'list':
                if restrictions['str']['max_length'] in scheme:
                    if len(data[field]) > scheme['max_length']:
                        return ExcessLengthError(exccess_length(field))
                    
                if restrictions['str']['min_length'] in scheme:
                    if len(data[field]) < scheme['max_length']:
                        return MissingLengthError(missing_length(field))
                    
                if restrictions['list']['allowed_types'] in scheme:
                    position = 0
                    for item in data[field]:
                        if not type(item).__name__ in scheme['allowed_types']:
                            return InvalidAllowedTypesError(invalid_allowed_types(field, position))
                        position += 1
                    del position           
        return True
    
"""
fields_scheme = {
    'field_restricted_str': {
        'type': 'str',
        'excluded_chars': list[str],
        'equal': str,
        'max_length': int,
        'min_length': int
    },
    'field_restricted_number_int': {
        'type': 'int',
        'max_size': int | bool,
        'min_size': int | bool,
        'equal': int | bool
    },
    'field_restricted_number_float': {
        'type': 'float',
        'max_size': int | bool,
        'min_size': int | bool,
        'equal': int | bool
    },
    'field_restricted_bool': {
        'type': 'bool',
        'equal': bool
    }
    'field_restricted_list': {
        'type': 'list',
        'max_length': int | bool,
        'min_length': int | bool,
        'allowed_types': list['type', 'type']
    }
}
"""