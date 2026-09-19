from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields = [
            'montant',
            'heure',
            'nb_transactions_24h',
            'distance_domicile',
            'pays_etranger',
            'nouvelle_carte',
            'reference'
        ]

        widgets = {
            'montant' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder': 'Ex: 200.5',
                'min':'0',
                'step':'0.1',
            }),
            'heure' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder': 'Ex: 14',
                'min':'0',
                'max':'23',
            }),
            'nb_transactions_24h' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder': 'Ex: 3',
                'min':'0',
            }),
            'distance_domicile' : forms.NumberInput(attrs={
                'class':'form-control',
                'placeholder': 'Ex: 4.0',
                'min':'0',
            }),
            'pays_etranger' : forms.CheckboxInput(attrs={
                'class':'form-check-input',
            }),
            'nouvelle_carte' : forms.CheckboxInput(attrs={
                'class':'form-check-input',
            }),
            'reference' : forms.TextInput(attrs={
                'class':'form-control',
                'placeholder': 'TXN-202601-002',
            }),

        }

        labels = {
            'montant': "Montant de la transaction",
            'heure': "Heure (0-23h)",
            'nb_transactions_24h':"Nb Transaction dans les 24h",
            'distance_domicile':"Distance from your home",
            'pays_etranger':"Transaction à l\'étranger",
            'nouvelle_carte':"Carte utilisée etc",
            'reference':"Reference (Optionnel)"

        }

        

