from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission)


class CPOVCUserManager(BaseUserManager):

    def _create_user(self, workforce_id, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not workforce_id:
            raise ValueError('The given workforce ID must be set')

        user = self.model(workforce_id=workforce_id,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, workforce_id, password=None, **extra_fields):
        return self._create_user(workforce_id, password, False, False,
                                 **extra_fields)

    def create_superuser(self, workforce_id, password, **extra_fields):
        return self._create_user(workforce_id, password, True, True,
                                 **extra_fields)


class AppUser(AbstractBaseUser, PermissionsMixin):
    reg_person = models.ForeignKey('cpovc_registry.RegPerson', null=True)
    workforce_id = models.CharField(max_length=20, unique=True)
    national_id = models.CharField(max_length=15, null=True, blank=True)
    designated_phone_number = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)
    password_changed_timestamp = models.DateTimeField(null=True)

    objects = CPOVCUserManager()
    USERNAME_FIELD = 'workforce_id'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'

    def get_full_name(self):
        """
        TO DO - Get this from persons table but for now just use
        Workforce ID
        """
        return self.workforce_id

    def get_short_name(self):
        """
        Return Workforce ID if exists or not
        """
        return self.workforce_id

    def get_username(self):
        """
        Return National ID if exists else Workforce ID
        """
        if self.national_id:
            return self.national_id
        elif self.workforce_id:
            return self.workforce_id
        else:
            return None

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class CPOVCPermission(Permission):
    permission_description = models.CharField(max_length=255)
    permission_set = models.CharField(max_length=100)
    permission_type = models.CharField(max_length=50, blank=True)
    restricted_to_self = models.BooleanField(blank=True, default=False)
    restricted_to_org_unit = models.BooleanField(blank=True, default=False)
    restricted_to_geo = models.BooleanField(blank=True, default=False)
    timestamp_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auth_permission_detail'


class CPOVCRole(Group):
    group_id = models.CharField(max_length=5)
    group_name = models.CharField(max_length=100)
    group_description = models.CharField(max_length=255)
    restricted_to_org_unit = models.BooleanField(blank=True, default=False)
    restricted_to_geo = models.BooleanField(blank=True, default=False)
    automatic = models.BooleanField(default=False)
    timestamp_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'auth_group_detail'


class CPOVCUserRoleGeoOrg(models.Model):
    # Put here to avoid cyclic imports because of User model
    from cpovc_registry.models import RegPersonsGeo, RegOrgUnit
    user = models.ForeignKey(AppUser)
    group = models.ForeignKey(CPOVCRole)
    org_unit = models.ForeignKey(RegOrgUnit, null=True)
    area = models.ForeignKey(RegPersonsGeo, null=True)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    void = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user_groups_geo_org'
