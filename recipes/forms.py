from django import forms

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = (
            'title', 'cooking_time', 'description', 'file'
        )
        exclude = ('author', 'pub_date',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
        }

    def clean(self):
        ingredientkeys = []
        for key in self.data.keys():
            if key.startswith('nameIngredient'):
                ingredientkeys.append(key)
                num = key.partition('_')[-1]
                value = self.data[f'valueIngredient_{num}']
                is_negative_number = lambda value: str(value)[0] == '-'
                if is_negative_number(value):
                    message = 'Вес ингредиента должен быть положительным.'
                    raise forms.ValidationError(message)
        if not ingredientkeys:
            message = 'Выберите хотя бы 1 ингредиент.'
            raise forms.ValidationError(message)
