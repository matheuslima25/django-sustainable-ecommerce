from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'image': 'Imagem do Produto',
            'name': 'Nome',
            'code': 'Código',
            'product_type': 'Tipo',
            'shoe_size': 'Tamanho (Calçado)',
            'clothing_size': 'Tamanho (Roupa)',
            'gender': 'Gênero',
            'purchase_price': 'Preço de Aquisição',
            'resale_price': 'Preço de Revenda',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Salvar', css_class='btn btn-success')
        )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        labels = {
            'rating': 'Nota (1 a 5 estrelas)',
            'comment': 'Comentário',
        }
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} estrela{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'rows': 1,
                'style': 'resize:none; height:38px;',  # impede que o user expanda
                'placeholder': 'Comentário breve...'
            }),
        }
