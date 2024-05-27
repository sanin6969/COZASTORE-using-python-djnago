from django import forms
from store.models import Product,Category

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
    def __init__(self,*args,**kwargs):
        super(ProductUpdateForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'       
        if 'is_active' not in self.fields:
            self.initial['is_active'] = True
class CategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
    