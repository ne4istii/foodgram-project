from django import forms

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        to_field_name = 'slug'
    )

    class Meta:
        model = Recipe
        fields = ('title', 'cooking_time', 'description', 'file')
        exclude = ('author', 'pub_date',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
        }
