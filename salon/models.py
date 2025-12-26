from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Service(models.Model):
    name = models.CharField(
        'Название услуги',
        max_length=200,
        help_text='Введите название услуги'
    )
    description = models.TextField(
        'Описание',
        help_text='Добавьте описание услуги'
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        help_text='Укажите цену услуги'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Master(models.Model):
    name = models.CharField(
        'Имя мастера',
        max_length=100
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        help_text='Расскажите о мастере'
    )
    photo = models.ImageField(
        'Фото',
        upload_to='masters/',
        blank=True,
        null=True,
        help_text='Загрузите фото мастера'
    )
    services = models.ManyToManyField(
        Service,
        through='MasterService',
        related_name='masters',
        verbose_name='Услуги мастера'
    )

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'
        ordering = ('name',)

    def __str__(self):
        return self.name


class MasterService(models.Model):
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='master_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='master_services'
    )
    duration = models.PositiveIntegerField(
        'Продолжительность (в минутах)',
        help_text='Укажите продолжительность услуги в минутах'
    )

    class Meta:
        verbose_name = 'Услуга мастера'
        verbose_name_plural = 'Услуги мастеров'
        unique_together = ('master', 'service')

    def __str__(self):
        return f'{self.master.name} - {self.service.name}'


class Appointment(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'PL', 'Запланировано'
        COMPLETED = 'CO', 'Завершено'
        CANCELLED = 'CA', 'Отменено'

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Клиент'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments',
        verbose_name='Мастер'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments',
        verbose_name='Услуга'
    )
    date_time = models.DateTimeField(
        'Дата и время'
    )
    status = models.CharField(
        'Статус',
        max_length=2,
        choices=Status.choices,
        default=Status.PLANNED
    )

    @property
    def total_cost(self):
        return self.service.price if self.service else 0

    class Meta:
        verbose_name = 'Запись на приём'
        verbose_name_plural = 'Записи на приём'
        ordering = ('-date_time',)

    def __str__(self):
        return f'Запись {self.id} на {self.date_time} к {self.master}'


class Review(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name='Запись'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Мастер',
        null=True, # временно разрешаем null
        blank=True
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Напишите ваш отзыв'
    )
    rating = models.PositiveSmallIntegerField(
        'Рейтинг',
        choices=[(i, i) for i in range(1, 6)],
        help_text='Оцените от 1 до 5'
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(
                fields=['appointment', 'author'],
                name='unique_review_per_appointment_author'
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author} на запись {self.appointment.id}'

    def save(self, *args, **kwargs):
        if self.appointment:
            self.master = self.appointment.master
        super().save(*args, **kwargs)
