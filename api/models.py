from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    USER_TYPE_CHOICES = (
        ("admin", "Admin"),
        ("user", "User"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"


class Report(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="reports",
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "admin"},
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Purchase(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="purchases",
        on_delete=models.CASCADE,
        limit_choices_to={"user_type": "user"},
    )
    item = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item} - {self.price}"
