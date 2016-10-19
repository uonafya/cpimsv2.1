"""Admin backend for editing this aggregate data."""
from django.contrib import admin

from .models import OVCAggregate


class OVCAggregateAdmin(admin.ModelAdmin):
    """Aggregate data admin."""

    search_fields = ['indicator_name', 'gender']
    list_display = ['id', 'indicator_name', 'indicator_count', 'age',
                    'reporting_period', 'cbo', 'subcounty', 'county']
    # readonly_fields = ['id']
    list_filter = ['indicator_name', 'project_year', 'reporting_period',
                   'gender', 'subcounty', 'county', 'cbo']


admin.site.register(OVCAggregate, OVCAggregateAdmin)
