from .models import *
from django import forms


class ImageLoadForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['url', 'picture', 'width', 'height']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        DESC = {
            'url': 'Copy link',
            'picture': 'Or download from your PC',
            'width': 'Set width px',
            'height': 'Set height px',
        }

        for field in DESC.keys():
            self.fields[f'{field}'].widget.attrs.update(
                {
                    'class': 'form-control',
                    'style': ['border-bottom: 2px solid red', 'background-color: #FFFFFF', 'border: none', ],
                    'rows': 1
                 }
            )
            self.fields[f'{field}'].label = DESC[field]
