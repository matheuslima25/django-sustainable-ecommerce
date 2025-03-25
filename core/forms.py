from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms

from .constants import COLORS
from .models import Brand, Product, Review


class ProductForm(forms.ModelForm):
    colors = forms.MultipleChoiceField(
        choices=[(name, name.capitalize()) for name, hex in COLORS],
        required=False,
        widget=forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '6',  # número de opções visíveis
            }),
        label="Cores Disponíveis"
    )

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
            'brand': 'Marca',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            *self.fields,
            Submit('submit', 'Salvar', css_class='btn btn-success')
        )

        # Preenche os valores do campo colors se estiver editando
        if self.instance and self.instance.colors:
            self.initial['colors'] = self.instance.colors

    def clean_colors(self):
        # Garante que seja salvo como lista JSON
        return self.cleaned_data.get('colors', [])


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


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        labels = {
            'name': 'Nome da Marca',
        }
