from django import forms
from catalog.models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар',
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'category', 'price', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': 4})

    def _check_forbidden_words(self, value):
        lowered = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in lowered:
                raise forms.ValidationError(
                    f'Использование слова "{word}" запрещено.'
                )
        return value

    def clean_name(self):
        name = self.cleaned_data.get('name', '')
        return self._check_forbidden_words(name)

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        if description:
            self._check_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and hasattr(image, 'content_type'):
            valid_types = ['image/jpeg', 'image/png']
            if image.content_type not in valid_types:
                raise forms.ValidationError('Изображение должно быть в формате JPEG или PNG.')
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise forms.ValidationError('Размер изображения не должен превышать 5 МБ.')
        return image
