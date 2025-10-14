def validate_positive_number(value, field_name):
    """Ensure the value is a positive number."""
    try:
        val = float(value)
        if val < 0:
            raise ValueError(f"{field_name} must be positive")
        return val
    except ValueError:
        raise ValueError(f"{field_name} must be a valid number")
