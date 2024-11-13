# finanzas/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def custom_intcomma(value):
    try:
        value = f"{value:,.2f}"  # Aplica coma como separador de miles y punto para decimales
        
        return value.replace(",", "_").replace(".", ",").replace("_", ".")  # Reemplaza la coma por punto y el punto decimal por coma
    except (ValueError, TypeError):
        return value
