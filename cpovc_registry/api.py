from rest_framework.generics import ListAPIView
from django.http import JsonResponse
from cpovc_registry.models import RegPersonsOrgUnits
from rest_framework.permissions import IsAuthenticated

from cpovc_registry.serializers import RegPersonsOrgUnitsSerializer, RegPerson

class RegPersonsOrgUnitsView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    model = RegPersonsOrgUnits    
    serializer_class = RegPersonsOrgUnitsSerializer


    def get_queryset(self):
        #get regperson associated with account
        user = self.request.user.reg_person
        return RegPersonsOrgUnits.objects.filter(person=user)

