from django.shortcuts import redirect, render
from finanzas.forms import FiltroCuotasForm, TransaccionForm
from rest_framework import viewsets
from .models import Familia, IntegranteFamilia, Categoria, MetodoPago, Transaccion, Cuota
from .serializers import FamiliaSerializer, IntegranteFamiliaSerializer, CategoriaSerializer, MetodoPagoSerializer, TransaccionSerializer, CuotaSerializer
from dateutil.relativedelta import relativedelta
from django.db.models import Sum

# class FamiliaViewSet(viewsets.ModelViewSet):
    # queryset = Familia.objects.all()
    # serializer_class = FamiliaSerializer


class IntegranteFamiliaViewSet(viewsets.ModelViewSet):
    queryset = IntegranteFamilia.objects.all()
    serializer_class = IntegranteFamiliaSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer


class TransaccionViewSet(viewsets.ModelViewSet):
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer


class CuotaViewSet(viewsets.ModelViewSet):
    queryset = Cuota.objects.all()
    serializer_class = CuotaSerializer

def cargar_transaccion(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            transaccion = form.save(commit=False)
            numero_cuotas = form.cleaned_data.get('numero_cuotas')

            # Si la transacción es cuotificada, calcular el monto de cada cuota
            if transaccion.estado == 'Cuotificado' and numero_cuotas:
                monto_por_cuota = transaccion.monto / numero_cuotas

                # Crear transacciones para cada cuota con fecha_aplicacion específica
                for i in range(1, numero_cuotas + 1):
                    fecha_aplicacion = transaccion.fecha_transaccion + relativedelta(months=i)
                    fecha_aplicacion = fecha_aplicacion.replace(day=3)  # Fijar el día de aplicación al 3

                    Transaccion.objects.create(
                        integrante=transaccion.integrante,
                        categoria=transaccion.categoria,
                        metodo_pago=transaccion.metodo_pago,
                        tipo=transaccion.tipo,
                        descripcion=transaccion.descripcion + ' Cuota ' + str(i) + ' de ' + str(numero_cuotas),
                        monto=monto_por_cuota,
                        fecha_transaccion=transaccion.fecha_transaccion,  #  Fecha real del gasto
                        fecha_aplicacion=fecha_aplicacion,
                        estado='Pendiente'
                    )
            else:
                # Si no es cuotificado, simplemente guarda la transacción como siempre
                transaccion.fecha_aplicacion = transaccion.fecha_transaccion
                transaccion.save()

            return redirect('lista_transacciones')
    else:
        form = TransaccionForm()
    return render(request, 'transacciones/cargar.html', {'form': form})

def lista_transacciones(request):
    transacciones = Transaccion.objects.all().order_by('-fecha_aplicacion')
    return render(request, 'transacciones/lista.html', {'transacciones': transacciones})

def dashboard(request):
    return render(request, 'dashboard.html')

def gastos_ingresos(request):
    total_ingresos = Transaccion.objects.filter(tipo='Ingreso').aggregate(Sum('monto'))['monto__sum']
    total_ingresos = total_ingresos or 0
    
    total_gastos = Transaccion.objects.filter(tipo='Gasto').aggregate(Sum('monto'))['monto__sum']
    total_gastos = total_gastos or 0
    
    saldo = total_ingresos - total_gastos
    
    return render(request, 'transacciones/informe-uno.html', {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'saldo': saldo
        })
    
def informe_compras_tarjeta(request):
    transacciones = None
    total_gastos = 0
    form = FiltroCuotasForm(request.GET or None)
    
    if form.is_valid():
        mes = int(form.cleaned_data['mes'])
        año = form.cleaned_data['año']
        
        # Filtrar las transacciones de tipo cuotificado con método de pago "Tarjeta Crédito"
        transacciones = Transaccion.objects.filter(
            metodo_pago__tipo='Tarjeta Crédito',
            estado='Pendiente',
            fecha_aplicacion__year=año,
            fecha_aplicacion__month=mes
        )
        
        # Calcular la suma total de los gastos
        total_gastos = transacciones.aggregate(Sum('monto'))['monto__sum'] or 0

    return render(request, 'transacciones/informe_compras_tarjeta.html', {
        'form': form,
        'transacciones': transacciones,
        'total_gastos': total_gastos
    })
        
