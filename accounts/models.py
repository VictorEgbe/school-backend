from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_delete
from phonenumber_field.modelfields import PhoneNumberField

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


def upload_location(instance, filename):
    return f'users/photos/{instance.get_full_name()}/{filename}'


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    phone = PhoneNumberField(unique=True, blank=False, null=False, error_messages={
        "unique": _("A user with that phone number already exists."),
    })
    gender = models.CharField(choices=GENDER, max_length=6)
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        null=True,
        blank=True,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'username']
    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.get_full_name()

    def get_image_url(self):
        if self.image:
            return self.image.url
        return None

    def get_response_data(self):
        return {
            'id': self.id,
            'fullName': self.get_full_name(),
            'phone': self.phone.as_national,
            'gender': self.gender,
            'image': self.get_image_url(),
            'username': self.username,
            'isAdmin': self.is_staff,
            'email': self.email,
            'createdAt': self.created_at
        }


@receiver(post_delete, sender=User)
def deleted_user_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()
