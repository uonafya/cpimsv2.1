from rest_framework.serializers import ModelSerializer

from .models import SetupList

class SetupListInlineSerializer(ModelSerializer):
    class Meta:
        model = SetupList
        fields = '__all__'