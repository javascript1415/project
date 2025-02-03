from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price','image','quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        
        def clean_image(self):
            image = self.cleaned_data["image"]
            if not image:
                raise forms.ValidationError('image:product image is required')
            return image
        