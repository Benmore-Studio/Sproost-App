from django import forms
from quotes.models import QuoteRequest
    

class QuoteRequestForm(forms.ModelForm):
    home_owner_id = forms.IntegerField(required=False)
    media = forms.FileField(widget=forms.ClearableFileInput(), required=False)


    class Meta:
        model = QuoteRequest
        fields = ["title", "summary", "contact_phone", "contact_username", "property_address",'quote_for', 'media']

    def __init__(self, *args, **kwargs):
        super(QuoteRequestForm, self).__init__(*args, **kwargs)

        common_attrs = {
            'class': 'w-full p-2 border border-gray-300 rounded-md focus:outline-none mt-1 focus:border-gray-500',
            'placeholder': 'Type here',
            'required': 'required'
        }
        special_field_classes = {
            'summary': 'min-h-[120px]',
            'contact_email': "h-full outline-none group-focus:oouline-none"
        }

        for field_name, field in self.fields.items():
            # Apply common attributes
            field.widget.attrs.update(common_attrs)
            # Apply special field classes if any
            if field_name in special_field_classes:
                field.widget.attrs['class'] += f' {special_field_classes[field_name]}'
            
            # Specify required attribute for specific fields
            # if field_name in ['title', 'summary', 'contact_phone', 'contact_email', 'property_address']:
            if field_name == 'summary':
                field.widget.attrs['required'] = 'required'
                field.widget.attrs['class'] += ' input'


        # Custom attributes for contact_phone
        self.fields['contact_phone'].widget.attrs.update({
            'class': 'w-10/12 rounded-md focus:outline-none mt-1 focus:border-gray-500',
            'placeholder': "+1 (555) 000-0000",
            'type': "tel"
        })

        # Custom attributes for contact_username
        self.fields['contact_username'].widget.attrs.update({
            'class': 'w-full h-full outline-none group-focus:outline-none mt-1 focus-visible:border-none border-none',
        })
