"""TCRUtils-specific errors"""

class error:
  class ConfigurationError(ValueError):
    """Used when a user-provided configuration causes an invalid state."""

for attr_name, attr_value in error.__dict__.items():
    if not attr_name.startswith("__"):
        globals()[attr_name] = attr_value

__all__ = [x for x in globals() if not x.startswith('_') and x != error.__name__]