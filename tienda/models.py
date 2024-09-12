from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=40)
    contacto = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(default='', blank=True)

    def __str__(self):
        return self.nombre


class Zapatilla(models.Model):
    modelo = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    talla = models.CharField(max_length=5)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    stock = models.IntegerField(default=1)
    stock_minimo = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.modelo} - {self.precio} $'

class Venta(models.Model):
    zapatilla = models.ForeignKey(Zapatilla, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    cliente = models.CharField(max_length=100)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total = self.zapatilla.precio * self.cantidad
        if self.zapatilla.stock < self.cantidad:
            raise ValueError("No hay suficiente stock para completar la venta.")
        self.zapatilla.stock -= self.cantidad
        self.zapatilla.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.zapatilla.nombre} - {self.cliente}"
    
class Oferta(models.Model):
    zapatilla = models.ForeignKey(Zapatilla, on_delete=models.CASCADE)
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(default=timezone.now)
