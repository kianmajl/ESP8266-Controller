from django import forms


class RGBForm(forms.Form):
    red = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-field',
            'type': 'number',
        }
    ))
    green = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-field',
            'type': 'number',
        }
    ))
    blue = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-field',
            'type': 'number',
        }
    ))

