import copy
from .exceptions import *
from .properties import restrictions, types

class DiSchema:
    def __init__(self, scheme: dict, stop: bool = False) -> None:
        self.scheme = scheme
        self.restrictions = restrictions
        self.stop = stop
        self.errors = []
        self._nesting_level = 0  # Control de profundidad para evitar recursión infinita
        self._max_nesting = 100  # Límite máximo de anidación

        self.selectors = {
            'str': self.strings,
            'int': self.numbers,
            'float': self.numbers,
            'list': self.lists,
            'bool': self.booleans,
            'dict': self.dicts
        }
    
    def check(self, data: dict) -> dict:
        """Valida los datos según el esquema definido"""
        self.errors.clear()
        self._nesting_level = 0

        # Usar deep copy para evitar mutaciones accidentales
        processed_data = {
            'original': data,
            'copy': copy.deepcopy(data)
        }

        for field, scheme in self.scheme.items():
            try:
                # Paso 1: Procesar campo (verificar existencia, valores por defecto)
                result = self._process_field(field, processed_data['copy'], scheme)
                if isinstance(result, Exception):
                    if self._should_stop_on_error(scheme, result):
                        return self._create_error_response(processed_data, result)
                    self.errors.append(result)
                    continue
                
                processed_data['copy'] = result

                # Paso 2: Transformar tipo si es necesario y está permitido
                if self._needs_transformation(field, processed_data['copy'], scheme):
                    result = self._transform_field(field, processed_data['copy'], scheme)
                    if isinstance(result, Exception):
                        if self._should_stop_on_error(scheme, result):
                            return self._create_error_response(processed_data, result)
                        self.errors.append(result)
                        continue
                    processed_data['copy'] = result

                # Paso 3: Validar tipo final
                if not self._validate_type(field, processed_data['copy'], scheme):
                    error = InvalidTypeError(field, scheme['type'])
                    if self._should_stop_on_error(scheme, error):
                        return self._create_error_response(processed_data, error)
                    self.errors.append(error)
                    continue

                # Paso 4: Validaciones específicas por tipo (incluyendo anidaciones)
                field_value = processed_data['copy'][field]
                field_type = type(field_value).__name__
                
                if field_type in self.selectors:
                    result = self.selectors[field_type](field_value, scheme, field_path=field)
                    if isinstance(result, Exception):
                        if self._should_stop_on_error(scheme, result):
                            return self._create_error_response(processed_data, result)
                        self.errors.append(result)
                        continue

            except Exception as e:
                # Capturar errores inesperados
                error = Exception(f"Error inesperado procesando campo '{field}': {str(e)}")
                if self._should_stop_on_error(scheme, error):
                    return self._create_error_response(processed_data, error)
                self.errors.append(error)
                continue

        return self._create_response(processed_data, self.errors)

    def _process_field(self, field: str, data: dict, scheme: dict) -> dict | Exception:
        """Procesa un campo: verifica existencia, maneja valores por defecto"""
        # Verificar que el esquema tenga los campos requeridos
        if restrictions['fields']['required'] not in scheme:
            return AttributeError(f"Campo 'required' faltante en el esquema para '{field}'")
        
        if restrictions['fields']['type'] not in scheme:
            return AttributeError(f"Campo 'type' faltante en el esquema para '{field}'")

        field_exists = field in data
        is_required = scheme['required']
        has_default = restrictions['fields']['default-value'] in scheme

        # Caso 1: Campo faltante y requerido
        if not field_exists and is_required:
            return NoFieldError(field)
        
        # Caso 2: Campo faltante, no requerido, pero con valor por defecto
        if not field_exists and not is_required and has_default:
            data[field] = scheme['default-value']
        
        # Caso 3: Campo faltante, no requerido, sin valor por defecto - saltar validación
        if not field_exists and not is_required and not has_default:
            return data  # No procesar este campo
        
        return data

    def _needs_transformation(self, field: str, data: dict, scheme: dict) -> bool:
        """Determina si un campo necesita transformación de tipo"""
        if field not in data:
            return False
        
        current_type = type(data[field]).__name__
        expected_type = scheme['type']
        has_transformation = restrictions['fields']['try-transformation'] in scheme and scheme['try-transformation']
        
        return current_type != expected_type and has_transformation

    def _transform_field(self, field: str, data: dict, scheme: dict) -> dict | Exception:
        """Transforma el tipo de un campo"""
        if field not in data:
            return data
            
        expected_type = scheme['type']
        
        # Verificar que el tipo objetivo existe en types
        if expected_type not in types:
            return Exception(f"Tipo '{expected_type}' no soportado para transformación")
        
        try:
            original_value = data[field]
            # Manejar valores None
            if original_value is None and expected_type != 'NoneType':
                return InvalidTypeError(field, expected_type)
            
            data[field] = types[expected_type](original_value)
            return data
        except (ValueError, TypeError) as e:
            return InvalidTypeError(field, expected_type)

    def _validate_type(self, field: str, data: dict, scheme: dict) -> bool:
        """Valida que el campo tenga el tipo correcto"""
        if field not in data:
            return True  # Campo no existe, no validar tipo
        
        current_type = type(data[field]).__name__
        expected_type = scheme['type']
        
        return current_type == expected_type

    def _should_stop_on_error(self, scheme: dict, error: Exception) -> bool:
        """Determina si se debe detener el procesamiento en caso de error"""
        should_raise = restrictions['fields']['raise'] in scheme and scheme['raise']
        if should_raise:
            raise error
        return self.stop

    def _create_error_response(self, data: dict, error: Exception) -> dict:
        """Crea una respuesta de error cuando se debe detener el procesamiento"""
        return {
            'data': data,
            'errors': [error],
            'valid': False
        }

    def _create_response(self, data: dict, errors: list) -> dict:
        """Crea la respuesta final del procesamiento"""
        valid = len(errors) == 0
        return {
            'data': data,
            'errors': errors,
            'valid': valid
        }

    def _validate_nested_structure(self, data, schema, field_path: str = "") -> list:
        """Valida estructuras anidadas recursivamente"""
        nested_errors = []
        
        # Control de profundidad para evitar recursión infinita
        self._nesting_level += 1
        if self._nesting_level > self._max_nesting:
            nested_errors.append(Exception(f"Máximo nivel de anidación excedido en '{field_path}'"))
            self._nesting_level -= 1
            return nested_errors

        try:
            # Crear un sub-validador para la estructura anidada
            if isinstance(schema, dict) and 'type' in schema:
                # Es un esquema de campo simple
                sub_validator = DiSchema({"nested_field": schema}, stop=False)
                result = sub_validator.check({"nested_field": data})
                
                if not result['valid']:
                    for error in result['errors']:
                        # Actualizar el path del error para reflejar la anidación
                        error_msg = str(error).replace("nested_field", field_path)
                        nested_errors.append(Exception(error_msg))
            
            elif isinstance(schema, dict):
                # Es un esquema completo (dict con múltiples campos)
                sub_validator = DiSchema(schema, stop=False)
                result = sub_validator.check(data)
                
                if not result['valid']:
                    for error in result['errors']:
                        # Actualizar el path del error
                        error_msg = f"{field_path}.{str(error)}"
                        nested_errors.append(Exception(error_msg))
        
        except Exception as e:
            nested_errors.append(Exception(f"Error validando estructura anidada en '{field_path}': {str(e)}"))
        
        finally:
            self._nesting_level -= 1
        
        return nested_errors

    def numbers(self, field, scheme, field_path: str = "") -> bool | Exception:
        """Validaciones específicas para números (int/float)"""
        if field is None:
            return Exception(f"Valor numérico no puede ser None en '{field_path}'")
        
        if restrictions['number']['equal'] in scheme:
            if field != scheme['equal']:
                return NoEqualError(field, scheme['equal'])
        
        if restrictions['number']['excluded-equalities'] in scheme:
            if field in scheme['excluded-equalities']:
                return Exception(f"Valor {field} está en la lista de valores excluidos en '{field_path}'")
        
        if restrictions['number']['allowed-equalities'] in scheme:
            if field not in scheme['allowed-equalities']:
                return Exception(f"Valor {field} no está en la lista de valores permitidos en '{field_path}'")
                    
        if restrictions['number']['max-size'] in scheme:
            if field > scheme['max-size']:
                return ExcessSizeError(field)
                    
        if restrictions['number']['min-size'] in scheme:
            if field < scheme['min-size']:
                return MissingSizeError(field)
        
        return True

    def strings(self, field, scheme, field_path: str = "") -> bool | Exception:
        """Validaciones específicas para strings"""
        if field is None:
            return Exception(f"String no puede ser None en '{field_path}'")
        
        if restrictions['str']['excluded-chars'] in scheme:
            excluded_chars = scheme['excluded-chars']
            if not isinstance(excluded_chars, list):
                return Exception(f"'excluded-chars' debe ser una lista en '{field_path}'")
            
            for char in excluded_chars:
                if char in field:
                    return ExcludedCharactersError(field)
        
        if restrictions['str']['allowed-chars'] in scheme:
            allowed_chars = scheme['allowed-chars']
            if not isinstance(allowed_chars, list):
                return Exception(f"'allowed-chars' debe ser una lista en '{field_path}'")
            
            for char in field:
                if char not in allowed_chars:
                    return Exception(f"Carácter '{char}' no está permitido en '{field_path}'")
                        
        if restrictions['str']['equal'] in scheme:
            if field != scheme['equal']:
                return NoEqualError(field, scheme['equal'])
        
        if restrictions['str']['excluded-equalities'] in scheme:
            if field in scheme['excluded-equalities']:
                return Exception(f"Valor '{field}' está en la lista de valores excluidos en '{field_path}'")
        
        if restrictions['str']['allowed-equalities'] in scheme:
            if field not in scheme['allowed-equalities']:
                return Exception(f"Valor '{field}' no está en la lista de valores permitidos en '{field_path}'")

        if restrictions['str']['max-length'] in scheme:
            if len(field) > scheme['max-length']:
                return ExcessLengthError(field)
                    
        if restrictions['str']['min-length'] in scheme:
            if len(field) < scheme['min-length']:
                return MissingLengthError(field)
            
        return True

    def booleans(self, field, scheme, field_path: str = "") -> bool | Exception:
        """Validaciones específicas para booleanos"""
        if field is None:
            return Exception(f"Booleano no puede ser None en '{field_path}'")
            
        if restrictions['bool']['equal'] in scheme:
            if field != scheme['equal']:
                return NoEqualError(field, scheme['equal'])
            
        return True
    

    def lists(self, field, scheme, field_path: str = "") -> bool | Exception:
        """Validaciones específicas para listas con soporte completo de anidación"""
        if field is None:
            return Exception(f"Lista no puede ser None en '{field_path}'")
            
        if not isinstance(field, list):
            return Exception(f"El campo debe ser una lista en '{field_path}'")
            
        if restrictions['list']['max-length'] in scheme:
            if len(field) > scheme['max-length']:
                return ExcessLengthError(field)
                    
        if restrictions['list']['min-length'] in scheme:
            if len(field) < scheme['min-length']:
                return MissingLengthError(field)
        
        # Validación de items permitidos - VERSIÓN CORREGIDA Y UNIFICADA
        if restrictions['list']['allowed-items'] in scheme:
            allowed_items = scheme['allowed-items']
            if not isinstance(allowed_items, list):
                return Exception(f"'allowed-items' debe ser una lista en '{field_path}'")
            
            for position, item in enumerate(field):
                item_path = f"{field_path}[{position}]"
                valid_item = False
                accumulated_errors = []
                
                for allowed_schema in allowed_items:
                    if isinstance(allowed_schema, dict):
                        # Es un esquema completo - validar recursivamente
                        nested_errors = self._validate_nested_structure(item, allowed_schema, item_path)
                        
                        if len(nested_errors) == 0:
                            valid_item = True
                            break
                        else:
                            # Acumular errores pero no agregarlos aún
                            accumulated_errors.extend(nested_errors)
                            
                    elif isinstance(allowed_schema, str):
                        # Es un tipo simple - verificar tipo directo
                        if type(item).__name__ == allowed_schema:
                            valid_item = True
                            break
                
                # Si ningún esquema funcionó, el item es inválido
                if not valid_item:
                    # Agregar los errores acumulados a self.errors
                    for error in accumulated_errors:
                        self.errors.append(error)
                    
                    # También devolver un error específico para este item
                    return Exception(f"Item en posición {position} ({item_path}) no coincide con ningún esquema permitido")
        
        return True

    def dicts(self, field, scheme, field_path: str = "") -> bool | Exception:
        """Validaciones específicas para diccionarios con soporte completo de anidación"""
        if field is None:
            return Exception(f"Diccionario no puede ser None en '{field_path}'")
            
        if not isinstance(field, dict):
            return Exception(f"El campo debe ser un diccionario en '{field_path}'")
            
        if restrictions['dict']['max-length'] in scheme:
            if len(field) > scheme['max-length']:
                return ExcessLengthError(field)
                    
        if restrictions['dict']['min-length'] in scheme:
            if len(field) < scheme['min-length']:
                return MissingLengthError(field)
        
        # Validación de esquema anidado completo
        if restrictions['dict']['schema'] in scheme:
            nested_schema = scheme['schema']
            if isinstance(nested_schema, dict):
                nested_path = f"{field_path}"
                nested_errors = self._validate_nested_structure(field, nested_schema, nested_path)
                
                if nested_errors:
                    for error in nested_errors:
                        self.errors.append(error)
                    return Exception(f"Errores de validación en esquema anidado de '{field_path}'")
        
        # Validación de items permitidos (cada valor del dict debe coincidir con algún esquema)
        if restrictions['dict']['allowed-items'] in scheme:
            allowed_items = scheme['allowed-items']
            if not isinstance(allowed_items, list):
                return Exception(f"'allowed-items' debe ser una lista en '{field_path}'")
            
            for key, value in field.items():
                value_path = f"{field_path}.{key}"
                valid_item = False
                
                for allowed_schema in allowed_items:
                    if isinstance(allowed_schema, dict):
                        # Validar recursivamente cada valor
                        nested_errors = self._validate_nested_structure(value, allowed_schema, value_path)
                        
                        if len(nested_errors) == 0:
                            valid_item = True
                            break
                        else:
                            # Agregar errores de anidación si ningún esquema funciona
                            for nested_error in nested_errors:
                                self.errors.append(nested_error)
                
                if not valid_item:
                    return Exception(f"Valor para clave '{key}' ({value_path}) no coincide con ningún esquema permitido")
        
        return True