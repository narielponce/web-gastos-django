# forms.py
import locale
from django import forms
import datetime
from .models import Transaccion

# Establecer configuración regional en español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class TransaccionForm(forms.ModelForm):
    numero_cuotas = forms.IntegerField(required=False, min_value=1, label="Cantidad de cuotas")

    class Meta:
        model = Transaccion
        fields = ['integrante', 'categoria', 'descripcion', 'metodo_pago', 'tipo', 'monto', 'fecha_transaccion', 'estado']
        widgets = {
            'fecha_transaccion': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        metodo_pago = cleaned_data.get("metodo_pago")
        numero_cuotas = cleaned_data.get("numero_cuotas")

        # Validación: Si es cuotificado, debe tener número de cuotas y ser con tarjeta de crédito
        if estado == "Cuotificado" and (not numero_cuotas or metodo_pago.tipo != "Tarjeta Crédito"):
            raise forms.ValidationError("Para un gasto cuotificado, el método de pago debe ser 'Tarjeta Crédito' y debe especificar el número de cuotas.")
        return cleaned_data

class FiltroCuotasForm(forms.Form):
    mes = forms.ChoiceField(choices=[(str(i), datetime.date(1900, i, 1).strftime('%B')) for i in range(1, 13)], label="Mes")
    año = forms.IntegerField(min_value=2020, max_value=2100, initial=datetime.date.today().year, label="Año")