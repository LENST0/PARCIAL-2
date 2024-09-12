from django import forms
from .models import Zapatilla,Venta

class ZapatillaForm(forms.ModelForm):
    
    class Meta:
        model = Zapatilla
        fields = ['modelo', 'marca', 'talla', 'precio', 'categoria', 'proveedor', 'stock', 'stock_minimo']
        widgets = {
            'categoria': forms.Select(),  
            'proveedor': forms.Select(),  
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['zapatilla', 'cantidad', 'cliente']

    def clean(self):
        cleaned_data = super().clean()
        zapatilla = cleaned_data.get('zapatilla')
        cantidad = cleaned_data.get('cantidad')

        if zapatilla and cantidad:
            if zapatilla.stock < cantidad:
                raise forms.ValidationError(f"No hay suficiente stock. Stock actual: {zapatilla.stock}")

            if zapatilla.stock < zapatilla.stock_minimo:
                raise forms.ValidationError(f"El stock es menor que el stock mínimo, no se puede realizar la venta. Stock actual: {zapatilla.stock}")

        return cleaned_data


