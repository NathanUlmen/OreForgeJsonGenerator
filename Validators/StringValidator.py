from Validators.Validator import ValidationResult, Validator


class StringValidator(Validator):
    def __init__(self, parentFieldName: str):
        super().__init__(parentFieldName)

    def validate(self, inputData) -> ValidationResult:
        return ValidationResult() if inputData is not None and len(inputData) > 0 else ValidationResult(self.fieldName + " is empty.")