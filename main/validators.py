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
            raise DjangoValidationError("Provided data failed JSON schema check")