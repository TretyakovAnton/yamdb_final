from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Жанр'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения',
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год выхода',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        max_length=200)
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанры',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MinValueValidator(
                1,
                message='Оценка должна быть от 1 до 10'
            ),
            MaxValueValidator(
                10,
                message='Оценка должна быть от 1 до 10'
            )
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        db_index=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique review'
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return f'Пользователь {self.author} оставил отзыв {self.text}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments',
        verbose_name='Отзыв'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        db_index=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )

    def __str__(self):
        return f'Пользователь {self.author} оставил отзыв {self.text}'
