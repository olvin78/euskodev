from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplica el valor por el argumento."""
    try:
        value = Decimal(value) if value is not None else Decimal(0)
        arg = Decimal(arg) if arg is not None else Decimal(0)
        return value * arg
    except (ValueError, TypeError, InvalidOperation):
        return Decimal(0)  # Retorna 0 en caso de error

@register.filter
def div(value, arg):
    """Divide el valor entre el argumento, evitando división por cero."""
    try:
        value = Decimal(value) if value is not None else Decimal(0)
        arg = Decimal(arg) if arg is not None else Decimal(1)  # Evita dividir entre 0
        return value / arg if arg != 0 else Decimal(0)
    except (ValueError, TypeError, InvalidOperation, ZeroDivisionError):
        return Decimal(0)  # Retorna 0 en caso de error
