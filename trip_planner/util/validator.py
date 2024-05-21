import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ValidationResult:
    error: bool
    error_msg: str


Rule = Callable[[Any], ValidationResult]


class Validator:
    def __init__(self, data: dict | object):
        self.data = data
        self.rules: dict[str, list[Rule]] = {}

    def _get_value(self, field: str) -> Any:
        if isinstance(self.data, dict):
            return self.data.get(field)
        return getattr(self.data, field)

    def set_rule(self, field: str, rules: list[Rule]) -> None:
        self.rules[field] = rules

    def validate(self) -> dict[str, ValidationResult]:
        errors: dict[str, ValidationResult] = {}
        for field, rules in self.rules.items():
            value = self._get_value(field)
            for rule in rules:
                result = rule(value)
                if field in errors:
                    errors[field].error = errors[field].error or result.error
                    errors[field].error_msg += f"\n{result.error_msg}"
                else:
                    errors[field] = result

        return errors


def min_length(length: int) -> Rule:
    def rule(value: Any) -> ValidationResult:
        if len(value) < length:
            return ValidationResult(
                True, f"Value must be at least {length} characters long."
            )
        return ValidationResult(False, "")

    return rule


def max_length(length: int) -> Rule:
    def rule(value: Any) -> ValidationResult:
        if len(value) > length:
            return ValidationResult(
                True, f"Value must be at most {length} characters long."
            )
        return ValidationResult(False, "")

    return rule


def required(value: Any) -> ValidationResult:
    if not value:
        return ValidationResult(True, "Value is required.")
    return ValidationResult(False, "")


def check_email(value: Any) -> ValidationResult:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, value):
        return ValidationResult(True, "Value must be a valid email address.")
    return ValidationResult(False, "")


def check_password(value: str) -> ValidationResult:
    """Performs the following checks on the password:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character

    Args:
        value (str): plaintext password

    Returns:
        ValidationResult
    """
    if len(value) < 8:
        return ValidationResult(True, "Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", value):
        return ValidationResult(
            True, "Password must contain at least one uppercase letter."
        )
    if not re.search(r"[a-z]", value):
        return ValidationResult(
            True, "Password must contain at least one lowercase letter."
        )
    if not re.search(r"\d", value):
        return ValidationResult(True, "Password must contain at least one number.")
    if not re.search(r"[!@#$%^&*]", value):
        return ValidationResult(
            True, "Password must contain at least one special character."
        )
    return ValidationResult(False, "")
