from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission)
from datetime import datetime


class CPOVCUserManager(BaseUserManager):

    def create_user(self, username, reg_person, password=None):

        from cpovc_registry.models import RegPerson
        if not username:
            raise ValueError('The given username must be set')

        now = datetime.now()
        user = self.model(username=username,
                          reg_person=RegPerson.objects.get(pk=int(reg_person)),
                          password=password,
                          is_staff=False,
                          is_active=True,
                          is_superuser=False,
                          role='Admin',
                          date_joined=now,
                          timestamp_created=now,
                          timestamp_updated=now,
                          )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, reg_person, password=None):
        user = self.create_user(username=username,
                                reg_person=reg_person,
                                password=password
                                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class AppUser(AbstractBaseUser, PermissionsMixin):
    reg_person = models.OneToOneField('cpovc_registry.RegPerson', null=False)
    role = models.CharField(max_length=20, unique=False, default='Public')
    username = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)
    password_changed_timestamp = models.DateTimeField(null=True)

    objects = CPOVCUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['reg_person']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'

    def _get_users_data(self):
        _reg_users_data = AppUser.objects.all()
        return _reg_users_data

    def get_full_name(self):
        """
        TO DO - Get this from persons table but for now just use
        Workforce ID
        """
        return self.username

    def get_short_name(self):
        """
        Return Workforce ID if exists or not
        """
        return self.username

    def get_username(self):
        """
        Return National ID if exists else Workforce ID
        """
        if self.username:
            return self.username
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
    # from cpovc_registry.models import RegPersonsGeo, RegOrgUnit
    user = models.ForeignKey(AppUser)
    group = models.ForeignKey(CPOVCRole)
    org_unit = models.ForeignKey('cpovc_registry.RegOrgUnit', null=True)
    area = models.ForeignKey('cpovc_registry.RegPersonsGeo', null=True)
    timestamp_modified = models.DateTimeField(default=timezone.now)
    void = models.BooleanField(default=False)

    class Meta:
        db_table = 'auth_user_groups_geo_org'
