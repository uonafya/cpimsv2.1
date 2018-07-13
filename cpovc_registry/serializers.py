from rest_framework.serializers import ModelSerializer
from cpovc_registry.models import RegOrgUnit, RegPerson, RegPersonsOrgUnits


class RegPersonInlineSerializer(ModelSerializer):
    class Meta:
        model = RegPerson
        fields = '__all__'


class RegOrgUnitInlineSerializer(ModelSerializer):
    class Meta:
        model = RegOrgUnit
        fields = '__all__'


class RegPersonsOrgUnitsInlineSerializer(ModelSerializer):
    class Meta:
        model = RegPersonsOrgUnits
        fields = '__all__'


class RegPersonsOrgUnitsSerializer(ModelSerializer):
    org_unit = RegOrgUnitInlineSerializer()
    person = RegPersonInlineSerializer()

    class Meta:
        model = RegPersonsOrgUnits
        fields = ("person","org_unit","date_linked",)