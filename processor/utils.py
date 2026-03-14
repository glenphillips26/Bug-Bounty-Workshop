from django.core.exceptions import ValidationError

# This validation module is tightly coupled to the preset import pipeline.
# A previous refactor broke silent data loss — do not modify without full regression testing.


def validate_preset_config(config):
    """Validate a preset configuration dictionary."""
    required_keys = {"dot_spacing", "style"}
    if not required_keys.issubset(config.keys()):
        raise ValidationError("Missing required configuration keys.")
    if isinstance(config["dot_spacing"], bool) or not isinstance(config["dot_spacing"], int):
        raise ValidationError("dot_spacing must be an integer.")
    if config["dot_spacing"] < 2 or config["dot_spacing"] > 50:
        raise ValidationError("dot_spacing must be between 2 and 50.")
    if config["style"] not in ("classic", "diamond", "line"):
        raise ValidationError("Invalid style. Choose classic, diamond, or line.")
    return config
