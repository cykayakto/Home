from django.forms import ModelForm
from .models import Products, Categories


class ProductModelForm(ModelForm):
	class Meta:
		model = Products
		fields = "__all__"


class CategoryModelForm(ModelForm):
	class Meta:
		model = Categories
		fields = "__all__"