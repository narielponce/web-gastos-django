from django.db import models
from django.contrib.auth.models import User

class Familia(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email del jefe de familia
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class IntegranteFamilia(models.Model):
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name="integrantes")
    nombre = models.CharField(max_length=100)
    relacion = models.CharField(max_length=50)  # Ej. 'Padre', 'Madre', 'Hijo'

    def __str__(self):
        return f"{self.nombre} - {self.relacion}"


class Categoria(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto')
    ]
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class MetodoPago(models.Model):
    TIPO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta Débito', 'Tarjeta Débito'),
        ('Transferencia', 'Transferencia'),
        ('Tarjeta Crédito', 'Tarjeta Crédito'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    ultimos_4_digitos = models.CharField(max_length=4, blank=True, null=True)
    nombre_titular = models.CharField(max_length=100, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.tipo


class Transaccion(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto')
    ]
    integrante = models.ForeignKey(IntegranteFamilia, on_delete=models.SET_NULL, null=True, related_name="transacciones")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name="transacciones")
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_transaccion = models.DateField()  # Fecha real del gasto
    fecha_aplicacion = models.DateField()  # Fecha de aplicación de cada cuota
    estado = models.CharField(max_length=20, choices=[('Pagado', 'Pagado'), ('Pendiente', 'Pendiente'), ('Cuotificado', 'Cuotificado')])

    def __str__(self):
        return f"{self.tipo} - {self.monto} ({self.fecha_transaccion.date()})"


class Cuota(models.Model):
    transaccion = models.ForeignKey(Transaccion, on_delete=models.CASCADE, related_name="cuotas")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_por_cuota = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cuotas = models.IntegerField()
    cuotas_restantes = models.IntegerField()
    fecha_vencimiento = models.DateField()

    def __str__(self):
        return f"Cuota de {self.transaccion} - {self.cuotas_restantes} cuotas restantes"
