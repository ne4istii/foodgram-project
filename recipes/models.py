from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from pytils.translit import slugify


User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
        help_text='Введите название ингредиента',
    )
    dimension = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        help_text='Введите имя тега',
        max_length=50, 
        unique=True
    )
    color = models.CharField(
        verbose_name='Цвет',
        help_text='Введите цвет для тега',
        max_length=50, 
    )
    slug = models.SlugField(
        verbose_name='Тег',
        auto_created=True,
        help_text='Введите слаг для тега',
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE, 
        related_name='recipes',
        help_text='Выберите автора рецепта',
    )
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Укажите подробное описание рецепта',
    )
    file = models.ImageField(
        verbose_name='Загрузить фото',
        help_text='Загрузите фото приготовленного рецепта',
        upload_to='recipes/',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='IngredientRecipe',
        help_text='Выберите один или несколько ингредиентов',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        help_text='Выберите один или несколько ингредиентов тегов',
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(limit_value=1)],
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
    )
    slug = models.SlugField(
        verbose_name='Ссылка',
        auto_created=True,
        help_text=(
            'Заполняется автоматически по названию рецепта'
        ),       
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)  
    
    def __str__(self): 
        return self.title  
    
    def list_tags(self):
        return self.tags.values_list('name', flat=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Название',
        on_delete=models.CASCADE,
        related_name='ingredientsrecipe'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredientsrecipe' 
    )
    amount = models.DecimalField(
        verbose_name='Количество',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(float('0.01'))]
    )

    def __str__(self): 
        return f'{self.recipe.title} содержится {self.ingredient.title} \
            в количестве {self.amount}'
        

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE, 
        related_name='follower',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE, 
        related_name='following',
        help_text='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'author']

    def __str__(self): 
        return f'{self.user.username} подписан на автора: \
            {self.author.username}'

    @property
    def has_following(self):
        return self.author.following.filter(
            user__id=self.user.id
        ).exists()


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE, 
        related_name='purchases',
        help_text='Покупки пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='purchases',
        help_text='Добавленные к покупке рецепты',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        unique_together = ['user', 'recipe']
        ordering = ('-recipe__pub_date',)
        
    def __str__(self): 
        return f'{self.user.username} добавил в покупки: {self.recipe.title}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE, 
        related_name='favorites',
        help_text='Избранное пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text='Добавленные в избранное рецепты',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        unique_together = ['user', 'recipe']
        ordering = ('-recipe__pub_date',)

    def __str__(self): 
        return f'{self.user.username} добавил в избранное: {self.recipe.title}'
