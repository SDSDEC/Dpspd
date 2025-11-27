from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    USER_TYPES = [
        ('CLIENT', 'Клиент'),
        ('MANAGER', 'Менеджер'),
        ('ADMIN', 'Администратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(
        max_length=200,
        verbose_name="ФИО",
        validators=[
            RegexValidator(
                regex='^[А-Яа-яёЁ\\s\\-]+$',
                message='ФИО должно содержать только кириллические буквы, пробелы и дефис'
            )
        ]
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        default='CLIENT',
        verbose_name="Тип пользователя"
    )

    agreement = models.BooleanField(
        default=False,
        verbose_name="Согласие на обработку персональных данных"
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.full_name} ({self.get_user_type_display()})"

    def is_admin(self):
        return self.user_type == 'ADMIN' or self.user.is_staff

    def is_manager(self):
        return self.user_type == 'MANAGER'

    def is_client(self):
        return self.user_type == 'CLIENT'

class RoomPlan(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('IN_PROGRESS', 'Принято в работу'),
        ('COMPLETED', 'Выполнено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_plans', verbose_name="Пользователь")
    title = models.CharField(max_length=255, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание помещения")

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    plan_file = models.ImageField(
        upload_to='room_plans/',
        blank=True,
        null=True,
        verbose_name="Фото помещения или план",
        help_text="Форматы: JPG, JPEG, PNG, BMP. Максимальный размер: 2MB"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        verbose_name="Статус заявки"
    )

    design_image = models.ImageField(
        upload_to='designs/',
        blank=True,
        null=True,
        verbose_name="Дизайн-проект"
    )
    admin_comment = models.TextField(blank=True, verbose_name="Комментарий администратора")

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_applications',
        verbose_name="Назначена"
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ['-upload_date']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def can_be_deleted(self):
        return self.status == 'NEW'