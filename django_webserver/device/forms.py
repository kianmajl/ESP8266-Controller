from django import forms


class TimingForm(forms.Form):
    on_time = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-field',
            'type': 'number',
            'placeholder': 500
        }
    ), required=False)
    off_time = forms.IntegerField(widget=forms.TextInput(
        attrs={
            'class': 'form-field',
            'type': 'number',
            'placeholder': 500
        }
    ), required=False)

