from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import SET_NULL


class ShippingAddressModel(models.Model):
    first_line_of_address = models.CharField(max_length=200)
    seccond_line_of_address = models.CharField(max_length=200)
    postcode = models.CharField(max_length=8)
    city = models.CharField(max_length=200, null=True)


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    password=None,
                    firstName=None,
                    lastName=None,
                    is_staff=False,
                    is_admin=False,
                    shipping_address=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(email=self.normalize_email(email))
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.firstName = firstName
        user_obj.lastName = firstName
        user_obj.shipping_address = shipping_address

        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255, blank=True, null=True)
    lastName = models.CharField(max_length=255, blank=True, null=True)
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    shipping_address = models.ForeignKey(ShippingAddressModel,
                                         on_delete=SET_NULL,
                                         null=True)

    USERNAME_FIELD = 'email'  # username
    # USERNAME_FIELD and password are required by default
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
