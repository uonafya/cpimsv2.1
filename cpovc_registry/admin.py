"""Admin backend for editing some admin details."""
from django.contrib import admin

from .models import (RegPerson, RegOrgUnit, RegOrgUnitsAuditTrail,
                     RegPersonsAuditTrail)


from cpovc_auth.models import AppUser


class PersonInline(admin.StackedInline):
    model = AppUser
    exclude = ('password', )


class RegPersonAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['first_name', 'surname', 'other_names']
    list_display = ['id', 'first_name', 'surname', 'date_of_birth',
                    'age', 'sex_id', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'sex_id']

    inlines = (PersonInline, )


admin.site.register(RegPerson, RegPersonAdmin)


class RegOrgUnitAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['org_unit_name', 'org_unit_id_vis']
    list_display = ['id', 'org_unit_id_vis', 'org_unit_name',
                    'parent_org_unit_id', 'is_void']
    # readonly_fields = ['id']
    list_filter = ['is_void', 'org_unit_type_id']


admin.site.register(RegOrgUnit, RegOrgUnitAdmin)


class OrgUnitAuditAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['org_unit_id']
    list_display = ['transaction_id', 'transaction_type_id', 'ip_address',
                    'app_user_id', 'timestamp_modified']
    # readonly_fields = ['id']
    list_filter = ['transaction_type_id', 'app_user_id']

admin.site.register(RegOrgUnitsAuditTrail, OrgUnitAuditAdmin)


class PersonsAuditAdmin(admin.ModelAdmin):
    """Register persons admin."""

    search_fields = ['person_id']
    list_display = ['transaction_id', 'transaction_type_id', 'ip_address',
                    'app_user_id', 'timestamp_modified']
    # readonly_fields = ['id']
    list_filter = ['transaction_type_id', 'app_user_id']

admin.site.register(RegPersonsAuditTrail, PersonsAuditAdmin)
