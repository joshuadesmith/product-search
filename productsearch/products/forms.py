from django import forms


class SearchForm(forms.Form):
    """
    Form for basic search
    """
    description = forms.CharField(label='Description', max_length=200, required=False)


class AdvancedSearchForm(forms.Form):
    """
    Form for advanced search
    """
    id_num = forms.IntegerField(required=False)
    description = forms.CharField(label='Description', max_length=200, required=False)
    department = forms.CharField(label='Department', max_length=20, required=False)
    last_sold_min = forms.DateField(label='Last Sold Min', required=False)
    last_sold_max = forms.DateField(label='Last Sold Max', required=False)
    shelf_life_min = forms.IntegerField(label='Shelf Life Min', required=False)
    shelf_life_max = forms.IntegerField(label='Shelf Life Max', required=False)
    price_min = forms.DecimalField(label='Price Min', required=False)
    price_max = forms.DecimalField(label='Price Max', required=False)
    cost_min = forms.DecimalField(label='Cost Min', required=False)
    cost_max = forms.DecimalField(label='Cost Max', required=False)


class BulkUploadForm(forms.Form):
    file = forms.FileField(required=True, widget=forms.FileInput)
