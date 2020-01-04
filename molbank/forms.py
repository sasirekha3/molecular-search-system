from django import forms
from decimal import Decimal
# from django.forms import Textarea, Textbox
from .models import molbank
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
 
class simpleSearchForm(forms.Form):
  CHOICES = ((1,'SMILES'),(2,'IUPAC'),(3,'sample_code'),(4,'molecular_formula'),(5,'solution_pt_barcode'),(6,'neat_sample_barcode'))
  simple_search_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control dropdown-toggle input-md'}), choices=CHOICES, initial=0)
  data = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)


class rangeSearchForm(forms.Form):
  CHOICES = ((1,'Molecular Weight'),(2,'ClogP'),(3,'TSPA'))
  range_search_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control dropdown-toggle input-md'}), choices=CHOICES, initial=0)
  from_ = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
  to_ = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)

class advancedSearchForm(forms.Form):
    CHOICES = ((1,'Default Substructure Search'), (2, 'Advanced Substructure Search'), (3, 'Exact Search'), (4, 'Similarity Search'), (5, 'Tautomer Search'),)
    Substructure_Search_Choices = ((1, 'Simple Substructure Search'),
                                   (2, 'Resonance Substructure Search'),
                                   (3, 'Affine Transform Search'),
                                   (4, 'Conformational Search'),
                                   )
    Exact_Search_Options = ((1, 'Distribution of electrons: bond types, atom charges, radicals, valences'),
                            (2, 'Atom isotopes'),
                            (3, 'Stereochemistry: chiral centers, stereogroups, and cis-trans bonds'),
                            (4, 'Connected fragments: disallows match of separate ions in salts'),
                            )
    Tautomer_Search_Options = ((1, 'Disable Hydrogen replacements'),
                               (2, 'Enable Ring-Chain Tautomerism'),
                               (3, 'Each boundary atom in the tautomeric chain must be one of N, O, P, S, As, Se, Sb, Te'),
                               (4, 'Carbon not from the aromatic ring at one end of the tautomeric chain, and one of N, O, P, S at the other end'),
                               (5, 'Carbon from the aromatic ring at one end of the tautomeric chain and one of N, O at the other end'),
                              )
    Similarity_Search_Choices = ((1, 'Tanimoto'),
                                 (2, 'Tversky'),
                                 (3, 'Euclid-Sub'),
                                 )
    search_type = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control dropdown-toggle input-md','onchange': 'advanced_dropdown();'}), choices=CHOICES, initial=0)
    SubStructureSearch_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=Substructure_Search_Choices, initial=1)
    ExactSearch_type = forms.MultipleChoiceField(choices=Exact_Search_Options, widget=forms.CheckboxSelectMultiple(), required=False)
    TautomerSearch_type = forms.MultipleChoiceField(choices=Tautomer_Search_Options, widget=forms.CheckboxSelectMultiple(), required=False)
    SimilaritySearch_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=Similarity_Search_Choices, initial=1)
    rmsa = forms.FloatField(required=False, initial=Decimal('1.0'))
    rmsc = forms.FloatField(required=False, initial=Decimal('1.0'))
    min_sim = forms.DecimalField(min_value=0.0, max_value=1.0, required=False, initial=Decimal('0.8'))
    TautomerSearch_Switch = forms.ChoiceField(widget=forms.RadioSelect(), choices=((1, 'Substructure Tautomer Search'), (2, 'Exact Tautomer Search'),), initial=1)


    #    search_type = forms.ChoiceField(choices=CHOICES)
    text_smiles = forms.CharField()
#    text_smiles = forms.CharField()

class addForm(forms.ModelForm):
    class Meta:
        model = molbank
        fields = ["ID","SMILES","SAMPLE_CODE"]
        labels = {
            'ID': 'Enter the ID',
            'SMILES': 'Enter the Smiles',
            'SAMPLE_CODE': 'Enter the Sample Code'
        }


class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# class Meta:
#         model = Author
#         fields = ('name', 'title', 'birth_date')
#         labels = {
#             'name': _('Writer'),
#         }
#         help_texts = {
#             'name': _('Some useful help text.'),
#         }
#         error_messages = {
#             'name': {
#                 'max_length': _("This writer's name is too long."),
#             },
#         }

class TestForm(forms.Form):
    image_data = forms.CharField(widget=forms.HiddenInput(), required=False)
