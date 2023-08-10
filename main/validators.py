from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError as DjangoValidationError

from jsonschema import validate, ValidationError

JSONSCHEMA = {
    "type": "object",
    "properties": {
        "article": {"type": "string"},
        "amount": {"type": "number"}
    },
    "required": ["article", "amount"],
    "additionalProperties": False
}

class ArticleJSONValidator(BaseValidator):
    def compare(self, input_value, schema):
        try:
            validate(input_value, schema)
        except ValidationError:
            raise DjangoValidationError("Данные не соответствую заданному формату JSON")
        
def validate_no_spaces(value):
    if len(value.split(' ')) != 1:
        raise DjangoValidationError(
            f'В названии {value} не должно быть пробелов'
        )