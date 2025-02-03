from django import forms
from order.models import Addres,Order
import re



class addressForm(forms.ModelForm):
    class Meta:
        model = Addres
        fields = ['phone','city','muncipality','tol','landmark']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        
        # Ensure the phone number is 10 digits long and starts with 9
        if len(str(phone)) != 10 or not str(phone).startswith('9'):
            raise forms.ValidationError("Phone number must be 10 digits long and start with '9'.")
        
        # Check if the phone number contains only digits
        if not re.match(r'^\d{10}$', str(phone)):
            raise forms.ValidationError("Phone number must contain only digits.")
        
        return phone

