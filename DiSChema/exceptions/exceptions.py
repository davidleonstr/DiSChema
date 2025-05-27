# exceptions.py - Excepciones personalizadas para DiSchema

class DiSchemaError(Exception):
    """Clase base para todas las excepciones de DiSchema"""
    pass

# ====== ERRORES DE CAMPO ======
class NoFieldError(DiSchemaError):
    """Error cuando un campo requerido no está presente"""
    def __init__(self, field_name: str):
        self.field_name = field_name
        super().__init__(f"Campo requerido '{field_name}' no encontrado")

class InvalidTypeError(DiSchemaError):
    """Error cuando un campo tiene un tipo incorrecto"""
    def __init__(self, field_name: str, expected_type: str):
        self.field_name = field_name
        self.expected_type = expected_type
        super().__init__(f"Campo '{field_name}' debe ser de tipo '{expected_type}'")

class MissingSchemaFieldError(DiSchemaError):
    """Error cuando falta un campo requerido en el esquema"""
    def __init__(self, field_name: str, missing_field: str):
        self.field_name = field_name
        self.missing_field = missing_field
        super().__init__(f"Campo '{missing_field}' faltante en el esquema para '{field_name}'")

class UnsupportedTypeError(DiSchemaError):
    """Error cuando se intenta transformar a un tipo no soportado"""
    def __init__(self, type_name: str):
        self.type_name = type_name
        super().__init__(f"Tipo '{type_name}' no soportado para transformación")

class UnexpectedProcessingError(DiSchemaError):
    """Error inesperado durante el procesamiento"""
    def __init__(self, field_name: str, original_error: str):
        self.field_name = field_name
        self.original_error = original_error
        super().__init__(f"Error inesperado procesando campo '{field_name}': {original_error}")

# ====== ERRORES DE VALIDACIÓN ======
class NoEqualError(DiSchemaError):
    """Error cuando un valor no es igual al esperado"""
    def __init__(self, actual_value, expected_value):
        self.actual_value = actual_value
        self.expected_value = expected_value
        super().__init__(f"Valor '{actual_value}' no es igual al esperado '{expected_value}'")

class ExcludedValueError(DiSchemaError):
    """Error cuando un valor está en la lista de valores excluidos"""
    def __init__(self, value, field_path: str = ""):
        self.value = value
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"Valor '{value}' está en la lista de valores excluidos{path_str}")

class NotAllowedValueError(DiSchemaError):
    """Error cuando un valor no está en la lista de valores permitidos"""
    def __init__(self, value, field_path: str = ""):
        self.value = value
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"Valor '{value}' no está en la lista de valores permitidos{path_str}")

# ====== ERRORES DE TAMAÑO/LONGITUD ======
class ExcessSizeError(DiSchemaError):
    """Error cuando un número excede el tamaño máximo"""
    def __init__(self, value, max_size=None):
        self.value = value
        self.max_size = max_size
        size_str = f" (máximo: {max_size})" if max_size else ""
        super().__init__(f"Valor '{value}' excede el tamaño máximo{size_str}")

class MissingSizeError(DiSchemaError):
    """Error cuando un número es menor al tamaño mínimo"""
    def __init__(self, value, min_size=None):
        self.value = value
        self.min_size = min_size
        size_str = f" (mínimo: {min_size})" if min_size else ""
        super().__init__(f"Valor '{value}' es menor al tamaño mínimo{size_str}")

class ExcessLengthError(DiSchemaError):
    """Error cuando una cadena o lista excede la longitud máxima"""
    def __init__(self, value, max_length=None):
        self.value = value
        self.max_length = max_length
        current_length = len(value) if hasattr(value, '__len__') else 'N/A'
        length_str = f" (máximo: {max_length}, actual: {current_length})" if max_length else ""
        super().__init__(f"Longitud excede el máximo permitido{length_str}")

class MissingLengthError(DiSchemaError):
    """Error cuando una cadena o lista es menor a la longitud mínima"""
    def __init__(self, value, min_length=None):
        self.value = value
        self.min_length = min_length
        current_length = len(value) if hasattr(value, '__len__') else 'N/A'
        length_str = f" (mínimo: {min_length}, actual: {current_length})" if min_length else ""
        super().__init__(f"Longitud es menor al mínimo requerido{length_str}")

# ====== ERRORES DE STRING ======
class ExcludedCharactersError(DiSchemaError):
    """Error cuando una cadena contiene caracteres excluidos"""
    def __init__(self, value, excluded_char=None):
        self.value = value
        self.excluded_char = excluded_char
        char_str = f" (carácter: '{excluded_char}')" if excluded_char else ""
        super().__init__(f"Cadena '{value}' contiene caracteres excluidos{char_str}")

class NotAllowedCharacterError(DiSchemaError):
    """Error cuando una cadena contiene caracteres no permitidos"""
    def __init__(self, character: str, field_path: str = ""):
        self.character = character
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"Carácter '{character}' no está permitido{path_str}")

class InvalidAllowedCharsTypeError(DiSchemaError):
    """Error cuando 'allowed-chars' no es una lista"""
    def __init__(self, field_path: str = ""):
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"'allowed-chars' debe ser una lista{path_str}")

class InvalidExcludedCharsTypeError(DiSchemaError):
    """Error cuando 'excluded-chars' no es una lista"""
    def __init__(self, field_path: str = ""):
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"'excluded-chars' debe ser una lista{path_str}")

# ====== ERRORES DE LISTA/DICCIONARIO ======
class InvalidAllowedItemsTypeError(DiSchemaError):
    """Error cuando 'allowed-items' no es una lista"""
    def __init__(self, field_path: str = ""):
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"'allowed-items' debe ser una lista{path_str}")

class InvalidAllowedTypesError(DiSchemaError):
    """Error cuando un item de lista no tiene un tipo permitido"""
    def __init__(self, list_value, position: int, expected_types=None):
        self.list_value = list_value
        self.position = position
        self.expected_types = expected_types
        types_str = f" (tipos permitidos: {expected_types})" if expected_types else ""
        super().__init__(f"Item en posición {position} tiene tipo no permitido{types_str}")

class InvalidItemSchemaError(DiSchemaError):
    """Error cuando un item no coincide con ningún esquema permitido"""
    def __init__(self, position: int, field_path: str = ""):
        self.position = position
        self.field_path = field_path
        super().__init__(f"Item en posición {position} ({field_path}) no coincide con ningún esquema permitido")

class InvalidValueSchemaError(DiSchemaError):
    """Error cuando un valor de diccionario no coincide con ningún esquema permitido"""
    def __init__(self, key: str, field_path: str = ""):
        self.key = key
        self.field_path = field_path
        super().__init__(f"Valor para clave '{key}' ({field_path}) no coincide con ningún esquema permitido")

# ====== ERRORES DE VALIDACIÓN ANIDADA ======
class MaxNestingExceededError(DiSchemaError):
    """Error cuando se excede el máximo nivel de anidación"""
    def __init__(self, field_path: str = "", max_nesting: int = 100):
        self.field_path = field_path
        self.max_nesting = max_nesting
        super().__init__(f"Máximo nivel de anidación ({max_nesting}) excedido en '{field_path}'")

class NestedValidationError(DiSchemaError):
    """Error durante la validación de estructura anidada"""
    def __init__(self, field_path: str, original_error: str):
        self.field_path = field_path
        self.original_error = original_error
        super().__init__(f"Error validando estructura anidada en '{field_path}': {original_error}")

class NestedSchemaValidationError(DiSchemaError):
    """Error en validación de esquema anidado"""
    def __init__(self, field_path: str = ""):
        self.field_path = field_path
        super().__init__(f"Errores de validación en esquema anidado de '{field_path}'")

# ====== ERRORES DE TIPO NULL ======
class NullValueError(DiSchemaError):
    """Error cuando un valor es None y no debería serlo"""
    def __init__(self, value_type: str, field_path: str = ""):
        self.value_type = value_type
        self.field_path = field_path
        path_str = f" en '{field_path}'" if field_path else ""
        super().__init__(f"{value_type} no puede ser None{path_str}")

# ====== ERRORES DE TIPO DE DATOS ======
class InvalidDataTypeError(DiSchemaError):
    """Error cuando un campo no es del tipo de datos esperado"""
    def __init__(self, field_path: str, expected_type: str, actual_type: str = ""):
        self.field_path = field_path
        self.expected_type = expected_type
        self.actual_type = actual_type
        type_str = f" (actual: {actual_type})" if actual_type else ""
        super().__init__(f"El campo debe ser {expected_type} en '{field_path}'{type_str}")