import json 

from django.http import JsonResponse
from django_filters import rest_framework
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

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


class SetupListChildView(ListAPIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request, **kwargs):
        try:
            
            jsonServiceCategoriesData = []
            data = request.data.get('payload')                
            domain_id = data['domain_id']
            index = int(data['index'])

            if domain_id:
                if index == 1:
                    # Get services
                    servicecategory = SetupList.objects.get(
                        field_name='olmis_domain_id', item_id=domain_id)
                    service_sub_category = servicecategory.item_sub_category

                    if not service_sub_category:
                        jsonServiceCategoriesData.append({'item_sub_category': servicecategory.item_description,
                                                        'item_sub_category_id': servicecategory.item_id,
                                                        'status': 0})
                    else:
                        servicecategories = SetupList.objects.filter(
                            field_name=service_sub_category)
                        for servicecategory in servicecategories:
                            jsonServiceCategoriesData.append({'item_sub_category': servicecategory.item_description,
                                                            'item_sub_category_id': servicecategory.item_id,
                                                            'status': 1})

                if index == 2:
                    # Get assessments
                    assessmentcategory = SetupList.objects.get(
                        field_name='olmis_assessment_domain_id', item_id=domain_id)
                    assessment_sub_category = assessmentcategory.item_sub_category
                    print 'assessmentcategory.item_sub_category -- %s' % assessmentcategory.item_sub_category

                    if not assessment_sub_category:
                        jsonServiceCategoriesData.append({'item_sub_category': assessmentcategory.item_description,
                                                        'item_sub_category_id': str(assessmentcategory.item_id),
                                                        'status': 0})
                    else:
                        assessmentcategories = SetupList.objects.filter(
                            field_name=assessment_sub_category)
                        for assessmentcategory in assessmentcategories:
                            jsonServiceCategoriesData.append({'item_sub_category': assessmentcategory.item_description,
                                                            'item_sub_category_id': str(assessmentcategory.item_id),
                                                            'status': 1})
                if index == 3:
                    # Get fieldname
                    setuplist = SetupList.objects.filter(
                        item_id=domain_id, field_name__icontains='olmis')

                    for s in setuplist:
                        # Get assessments service status
                        assessmentstatuscategorys = SetupList.objects.filter(
                            field_name='' + s.item_sub_category + '')
                        if assessmentstatuscategorys:
                            for assessmentstatuscategory in assessmentstatuscategorys:
                                jsonServiceCategoriesData.append({'item_sub_category': assessmentstatuscategory.item_description,
                                                                'item_sub_category_id': str(assessmentstatuscategory.item_id),
                                                                'status': 1})
                if index == 4:
                    data_list = data['domain_id']
                    if data_list:
                        _data = json.loads(data_list)
                        _item_ids = []
                        for _data_ in _data:
                            _service = _data_['olmis_priority_service']

                            # . . . not comma separated
                            if ',' not in _service:
                                _item_ids.append(_service)
                            else:
                                _itemx = _service.split(",")
                                for _itemx_ in _itemx:
                                    _item_ids.append(_itemx_)
                        for _item_id in _item_ids:
                            setuplist = SetupList.objects.filter(
                                item_id=_item_id, field_name__icontains='olmis')
                            for s in setuplist:
                                jsonServiceCategoriesData.append({'item_sub_category': s.item_description,
                                                                'item_sub_category_id': str(s.item_id),
                                                                'status': 1})
                return JsonResponse(jsonServiceCategoriesData, content_type='application/json',safe=False)
        except Exception, e:
            print 'Error >>  %s' % str(e)
            raise e
        return JsonResponse(jsonServiceCategoriesData, content_type='application/json',safe=False)