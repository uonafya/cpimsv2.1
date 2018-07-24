from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework

from .serializers import  SetupListInlineSerializer
from .models import SetupList

class SetupListView(ListAPIView):
    permission_classes=[IsAuthenticated,]
    model = SetupList
    serializer_class = SetupListInlineSerializer
    queryset = SetupList.objects.all()
    # filter_backends = (rest_framework.DjangoFilterBackend, )

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = SetupList.objects.all()

        id = self.request.query_params.get('id', None)                    
        if id is not None:
            queryset = queryset.filter(id=id)

        item_id = self.request.query_params.get('item_id', None)                    
        if item_id is not None:
            queryset = queryset.filter(item_id=item_id)

        item_description = self.request.query_params.get('item_description', None)                    
        if item_description is not None:
            queryset = queryset.filter(item_description=item_description)
        
        item_description_short = self.request.query_params.get('item_description_short', None)                    
        if item_description_short is not None:
            queryset = queryset.filter(item_description_short=item_description_short)

        item_category = self.request.query_params.get('item_category', None)                    
        if item_category is not None:
            queryset = queryset.filter(item_category=item_category)

        item_sub_category = self.request.query_params.get('item_sub_category', None)                    
        if item_sub_category is not None:
            queryset = queryset.filter(item_sub_category=item_sub_category)
        
        the_order = self.request.query_params.get('the_order', None)                    
        if the_order is not None:
            queryset = queryset.filter(the_order=the_order)
        
        user_configurable = self.request.query_params.get('user_configurable', None)                    
        if user_configurable is not None:
            queryset = queryset.filter(user_configurable=user_configurable)
        
        sms_keyword = self.request.query_params.get('sms_keyword', None)                    
        if sms_keyword is not None:
            queryset = queryset.filter(sms_keyword=sms_keyword)
        
        is_void = self.request.query_params.get('is_void', None)                    
        if is_void is not None:
            queryset = queryset.filter(is_void=is_void)
        
        field_name = self.request.query_params.get('field_name', None)                    
        if field_name is not None:
            queryset = queryset.filter(field_name=field_name)

        timestamp_modified = self.request.query_params.get('timestamp_modified', None)                    
        if timestamp_modified is not None:
            queryset = queryset.filter(timestamp_modified=timestamp_modified)        


        return queryset