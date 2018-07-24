from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import  SetupListInlineSerializer
from .models import SetupList

class SetupListView(ListAPIView):
    permission_classes=[IsAuthenticated,]
    model = SetupList
    serializer_class = SetupListInlineSerializer
    queryset = SetupList.objects.all()