from rest_framework.serializers import ModelSerializer

from cpovc_registry.serializers import RegPersonInlineSerializer

from .models import OVCRegistration


class OVCRegistrationInlineSerializer(ModelSerializer):
    person = RegPersonInlineSerializer()
    class Meta:
        model = OVCRegistration
        fields = '__all__'


