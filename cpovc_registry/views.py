from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from cpovc_auth.forms import RegistrationForm
from cpovc_main.functions import get_list_of_org_units, get_dict
from .forms import FormRegistry, FormRegistryNew, FormContact
from .models import RegOrgUnit, RegOrgUnitContact
from .functions import org_id_generator, save_contacts, save_external_ids


def home(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            if form.is_valid():
                search_string = form.cleaned_data['org_unit_name']
                org_type = form.cleaned_data['org_type']
                org_closed = form.cleaned_data['org_closed']
                print org_closed
                closed_org = True if org_closed == 'True' else False
                unit_type = [org_type] if org_type else []
                results = get_list_of_org_units(search_string=search_string,
                                                include_closed=closed_org,
                                                in_org_unit_types=unit_type,
                                                number_of_results=50)
                message = "Search for %s returned %d results" % (search_string,
                                                                 len(results))
                return render(request,
                              'registry/index.html', {'form': form,
                                                      'results': results,
                                                      'message': message})
            else:
                print 'Not Good %s' % (form.errors)
        form = FormRegistry()
        return render(request, 'registry/index.html', {'form': form})
    except Exception, e:
        raise e


def register_new(request):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            cform = FormContact(data=request.POST)
            # org_unit_type = form.cleaned_data['org_unit_type']
            # org_unit_name = form.cleaned_data['org_unit_name']
            org_unit_type = request.POST.get('org_unit_type')
            org_unit_name = request.POST.get('org_unit_name')
            reg_date = request.POST.get('reg_date')
            sub_county = request.POST.getlist('sub_county')
            parent_org_unit = request.POST.get('parent_org_unit')
            org_reg_type = request.POST.get('org_reg_type')
            legal_reg_number = request.POST.get('legal_reg_number')
            print sub_county
            org_new = RegOrgUnit(org_unit_id_vis='NXXXXXX',
                                 org_unit_name=org_unit_name,
                                 org_unit_type_id=org_unit_type,
                                 date_operational=reg_date,
                                 parent_org_unit_id=parent_org_unit,
                                 is_void=False)
            org_new.save()
            org_unit_id = org_new.pk
            org_unit_id_vis = org_id_generator(org_unit_id)
            org_new.org_unit_id_vis = org_unit_id_vis
            org_new.save(update_fields=["org_unit_id_vis"])
            msg = 'Organisation Unit (%s) save success.' % (org_unit_name)
            messages.add_message(request, messages.INFO, msg)
            # Save external ids
            save_external_ids(org_reg_type, legal_reg_number, org_unit_id)
            # Save geo units
            # Save contacts
            if cform.is_valid():
                for (form_id, form_value) in cform.extra_contacts():
                    if form_value:
                        print form_id, form_value, org_unit_id
                        save_contacts(form_id, form_value, org_unit_id)
            # Perform audit trail
            return HttpResponseRedirect(reverse(home))
        form = FormRegistryNew()
        cform = FormContact()
        return render(request, 'registry/new.html', {'form': form,
                                                     'cform': cform})
    except Exception, e:
        raise e


def register_edit(request, org_id):
    '''
    Some default page for the home page / Dashboard
    '''
    try:
        if request.method == 'POST':
            form = FormRegistry(data=request.POST)
            cform = FormContact(data=request.POST)
            # org_unit_type = form.cleaned_data['org_unit_type']
            # org_unit_name = form.cleaned_data['org_unit_name']
            '''
            org_unit_type = request.POST.get('org_unit_type')
            org_unit_name = request.POST.get('org_unit_name')
            reg_date = request.POST.get('reg_date')
            org_new = RegOrgUnit(org_unit_id_vis='NXXXXXX',
                                 org_unit_name=org_unit_name,
                                 org_unit_type_id=org_unit_type,
                                 date_operational=reg_date,
                                 is_void=False)
            org_new.save()
            org_unit_id = org_new.pk
            org_unit_id_vis = org_id_generator(org_unit_id)
            org_new.org_unit_id_vis = org_unit_id_vis
            org_new.save(update_fields=["org_unit_id_vis"])
            msg = 'Organisation Unit (%s) save success.' % (org_unit_name)
            messages.add_message(request, messages.INFO, msg)
            # results = {'message': msg, 'value': org_unit_type}
            # return JsonResponse(results, content_type='application/json')
            if cform.is_valid():
                for (form_id, form_value) in cform.extra_contacts():
                    if form_value:
                        print form_id, form_value, org_unit_id
                        save_contacts(form_id, form_value, org_unit_id)
            '''
            return HttpResponseRedirect(reverse(home))
        # f = ContactForm(request.POST, initial=data)
        # f.has_changed()
        units = RegOrgUnit.objects.get(pk=org_id)
        name = units.org_unit_name
        unit_type = units.org_unit_type_id
        date_op = units.date_operational
        data = {'org_unit_name': name, 'org_unit_type': unit_type,
                'reg_date': date_op, 'sub_county': ['TNRS', 'TNCB', 'TNCW']}
        form = FormRegistryNew(data)
        cform = FormContact()
        return render(request, 'registry/edit.html', {'form': form,
                                                      'cform': cform})
    except Exception, e:
        raise e


def register_details(request, org_id):
    '''
    Some default page for the home page / Dashboard
    vals - All possible list_general used on this page
    '''
    try:
        # All my filters
        vals = get_dict('contact_detail_type_id')
        vals['TNCD'] = 'Test'

        org_unit = RegOrgUnit.objects.get(pk=org_id)
        org_contact = RegOrgUnitContact.objects.filter(org_unit_id=org_id)
        org_unit.contacts = org_contact
        return render(request, 'registry/details.html',
                      {'org_details': org_unit, 'vals': vals})
    except Exception, e:
        # raise e
        error = 'Org unit view error - %s' % (str(e))
        print error
        form = FormRegistry()
        msg = 'Organisation Unit does not exist - %s' % (str(e))
        messages.add_message(request, messages.INFO, msg)
        return render(request, 'registry/index.html', {'form': form})


def register(request):
    '''
    Some default page for the home page / Dashboard
    '''
    form = RegistrationForm()

    return render(request, 'register.html', {'form': form},)
