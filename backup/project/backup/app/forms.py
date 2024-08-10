from django import forms

class MessageForm(forms.Form):
    content = forms.CharField(label='Message', max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message here...'}))