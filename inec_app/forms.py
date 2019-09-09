from django import forms
from inec_app.models import AnnouncedPuResults

error = 'alert alert-danger' 

class AnnouncedPuResultsForm(forms.ModelForm):
    polling_unit_uniqueid = forms.CharField(
        max_length=50,  
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control input-lg',
                'placeholder' : 'PU Unique ID',
                'autocomplete' : 'off',
                'autofocus': True,
                'max_length' : 50,
            }
        ),
        required = True,
        label = '',
    )
    
    party_abbreviation = forms.CharField(
        max_length=4,
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control input-lg',
                'placeholder' : 'Party Abbreviation',
                'autocomplete' : 'off',
                'max_length' : 4,
            }
        ),
        required = True,
        label = '',
    )
    
    party_score = forms.IntegerField(
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control input-lg',
                'placeholder' : 'Party Score',
                'autocomplete' : 'off',
            }
        ),
        required = True,
        label = '',
    )
    
    entered_by_user = forms.CharField(
        max_length=50,
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control input-lg',
                'placeholder' : 'Entered By',
                'autocomplete' : 'off',
                'max_length' : 50,
            }
        ),
        required = True,
        label = '', 
    )
    
    date_entered = forms.DateTimeField(
        widget = forms.SelectDateWidget(
            attrs = {
                'class' : 'form-control',
                'style': 'width: 33%; display: inline-block;'
            }
        ),
        label = '',
    )
    
    user_ip_address = forms.CharField(
        max_length=50,
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control input-lg',
                'placeholder' : 'IP Address',
                'autocomplete' : 'off',
                'max_length' : 50,
            }
        ),
        required = False,
        label = '',
    )

    class Meta:
        model = AnnouncedPuResults
        fields = [
            'polling_unit_uniqueid',
            'party_abbreviation',
            'party_score',
            'entered_by_user',
            'date_entered',
            'user_ip_address',
        ]
 
       
