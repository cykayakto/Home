from django.forms import ModelForm
from .models import Cart


class CartModelForm(ModelForm):
	class Meta:
		model = Cart
		fields = "__all__"