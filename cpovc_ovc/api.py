from django.http import JsonResponse

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


from cpovc_registry.models import RegOrgUnit

from .models import OVCRegistration
from .serializers import OVCRegistrationInlineSerializer

class RegOrgUnitOVCRegistrationsView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    model = OVCRegistration
    serializer_class = OVCRegistrationInlineSerializer

    def get_queryset(self):
        #get ovc registrations related to the orgunit provided
        found_orgunit = RegOrgUnit.objects.get(id=self.kwargs["orgunit"])
        
        if found_orgunit:
            return OVCRegistration.objects.filter(child_cbo=found_orgunit) 
        