from django import forms
from django.forms import ModelForm
from materiallist.models import *
from materiallist.views import *
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages 
class MaterialsForm(forms.ModelForm):
    #import pdb;pdb.set_trace()
    class Meta:
        model=Materials
        
        fields=( 
            
        'Material_Code',
        'Material_Name',
        'Material_Location',
        'Unit_of_Measurement',
        'Maximum_Level',
        'Minimum_Level',
        'Re_order_Level',
        'Quantity')
    
class TransactionForm(forms.ModelForm):  
    class Meta:  
        model = Transactions
        fields = "__all__" 
    