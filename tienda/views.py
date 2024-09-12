from django.shortcuts import render,redirect
from .forms import ZapatillaForm,VentaForm
from .models import Venta, Oferta


def home(request):
    return render(request, 'tienda/home.html')  


def Registrar_zapatilla(request):
    if request.method == 'POST':
        form = ZapatillaForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    else:
        form = ZapatillaForm()
        return render(request, 'tienda/Registrar_Zapatilla.html',{'form': form})
    

def RegistrarVentaView(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            zapatilla = venta.zapatilla
            zapatilla.stock -= venta.cantidad
            zapatilla.save()
            venta.save()
            return redirect('home')  
    else:
        form = VentaForm()

    return render(request, 'tienda/Registrar_venta.html', {'form': form})


def resumen_ventas_ofertas(request):
    # Obtener todas las ventas con zapatillas que tienen ofertas aplicadas
    ventas = Venta.objects.filter(
        zapatilla__oferta__isnull=False
    ).prefetch_related('zapatilla__oferta')

    # Calcular el precio final con descuento
    ventas_ofertas = []
    for venta in ventas:
        oferta = Oferta.objects.filter(
            zapatilla=venta.zapatilla,
            fecha_inicio__lte=venta.fecha_venta,
            fecha_fin__gte=venta.fecha_venta
        ).first()
        if oferta:
            descuento = oferta.descuento
            precio_original = venta.zapatilla.precio
            precio_final = precio_original - (precio_original * descuento / 100)
            ventas_ofertas.append({
                'cliente': venta.cliente,
                'modelo': venta.zapatilla.modelo,
                'marca': venta.zapatilla.marca,
                'cantidad': venta.cantidad,
                'precio_original': precio_original,
                'descuento_aplicado': descuento,
                'precio_final': precio_final,
                'fecha_venta': venta.fecha_venta
            })
        else:
            ventas_ofertas.append({
                'cliente': venta.cliente,
                'modelo': venta.zapatilla.modelo,
                'marca': venta.zapatilla.marca,
                'cantidad': venta.cantidad,
                'precio_original': venta.zapatilla.precio,
                'descuento_aplicado': 0,
                'precio_final': venta.zapatilla.precio,
                'fecha_venta': venta.fecha_venta
            })

    context = {
        'ventas_ofertas': ventas_ofertas
    }
    return render(request, 'tienda/resumen_ventas_ofertas.html', context)
