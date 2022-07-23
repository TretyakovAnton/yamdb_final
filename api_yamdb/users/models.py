from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
USER_ROLE_CHOICES = [
    (USER, 'user'),
    (ADMIN, 'admin'),
    (MODERATOR, 'moderator'),
]


class User(AbstractUser):
    bio = models.TextField(
        blank=True,
        verbose_name='Биография',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Почта пользователя',
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    role = models.CharField(
        max_length=10,
        choices=USER_ROLE_CHOICES,
        default=USER,
        verbose_name='Роль пользователя',
    )
    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        verbose_name='код подтверждения',
    )

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}'

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
