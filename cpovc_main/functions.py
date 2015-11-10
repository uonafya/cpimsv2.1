# -*- coding: utf-8 -*-
# Common method for getting related list for dropdowns... e.t.c
import datetime
import itertools
import collections
import jellyfish
from .models import SetupList, SetupGeography
from django.core.exceptions import FieldError
from django.db.models import Q
from cpovc_registry.models import (
    RegPerson, RegPersonsGeo, RegPersonsOrgUnits, RegOrgUnit,
    RegOrgUnitGeography, RegPersonsTypes)


def get_general_list(field_name=[]):
    '''
    Get list general filtered by field_name
    '''
    try:
        queryset = SetupList.objects.filter(
            is_void=False, field_name=field_name).order_by('the_order')

        # To do -...............
        # queryset = queryset.filter(field_name='sex_id')
    except Exception, e:
        error = 'Error getting whole list - %s' % (str(e))
        print error
        return None
    else:
        return queryset


def get_list(field_name=[], default_txt=False):
    my_list = ()
    try:
        final_list = get_dict(field_name, default_txt)
        if final_list:
            my_list = final_list.items()
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return my_list
    else:
        return my_list


def get_dict(field_name=[], default_txt=False):
    '''
    Push the item_id and item_description into a tuple
    Instead of sorting after, ordered dict works since query
    results are already ordered from db
    '''
    initial_list = {'': default_txt} if default_txt else {}
    all_list = collections.OrderedDict(initial_list)
    try:
        my_list = get_general_list(field_name)
        if my_list:
            for a_list in my_list:
                all_list[a_list.item_id] = a_list.item_description
        else:
            all_list = ()
    except Exception, e:
        error = 'Error getting list - %s' % (str(e))
        print error
        return ()
    else:
        return all_list


def tokenize_search_string(search_string):
    if not search_string:
        return []
    return search_string.split()


def as_of_date_filter(queryset, as_of_date=None, include_died=True):
    """
    as_of_date: A date or not specified. If not specified, we assume we want
    current data (date delinked is null). If specified, when looking at
    date_delinked, date_of_death e.t.c we regard them as still linked, still
    alive e.t.c if the date delinked or date_of_death occurs after this
    parameter date.
    This function takes in any queryset and tries to use the as_of_date filter
    to carry out the above rule.
    By default we need to exclude the died, but if we have include died we have
    #show all the died. If we do not have include died BUT we have
    #as of date, we get all whose date of death came after the as_of_death.
    """
    if include_died:
        # do nothing - We have not filtered on dead or alive so everyone is
        # currently included
        pass
    else:
        # now basically DO NOT include died so we remove the died...unless the
        # as_of_date is provided then we only remove those whose date of
        # death is gt than
        if as_of_date:
            queryset = queryset.exclude(date_of_death__lt=as_of_date)
        else:
            queryset = queryset.exclude(date_of_death__isnull=False)

    if not as_of_date:
        try:
            queryset = queryset.filter(date_delinked__isnull=True)
        except FieldError:
            pass
    if as_of_date:
        try:
            queryset = queryset.exclude(date_delinked__lt=as_of_date)
        except FieldError:
            try:
                queryset = queryset.exclude(date_of_death__lt=as_of_date)
            except FieldError:
                pass

    return queryset


def order_by_relevence(wrapped_function):
    def _wrapper(*args, **kwargs):
        results = wrapped_function(*args, **kwargs)
        # we order the results by relevance
        search_string = kwargs['search_string']
        field_names = kwargs['field_names']
        diff_distances = []
        for result in results:
            # match against the concentenated fields
            field_values = [getattr(result, fname) for fname in field_names]
            field_values = itertools.ifilter(None, field_values)
            field_string = " ".join(field_values)
            # access the field names dynamically.
            diff_distance = jellyfish.jaro_distance(
                unicode(field_string.upper()),
                unicode(search_string.upper())
            )
            diff_distances.append((result, diff_distance),)
        sorted_distances = sorted(diff_distances, key=lambda x: -x[1])
        # Now return the actual sorted results not the tuples
        return [sorted_distance[0] for sorted_distance in sorted_distances]
    return _wrapper


def search_core_ids(regpersons_queryset, search_string, as_of_date=None):
    """takes a queryset of regpersons and a search string - returns a filtered
    queryset with filters acted upon core_ids"""
    core_id_fields = ['national_id', 'birth_reg_id', 'workforce_id',
                      'beneficiary_id']

    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        for field in core_id_fields:
            q_filter |= Q(**{"%s__icontains" % field: search_string})
    results = regpersons_queryset.filter(q_filter)

    results = as_of_date_filter(results, as_of_date=None)
    # redundant just for documentation
    return results


@order_by_relevence
def direct_field_search(queryset, field_names, search_string, as_of_date=None):
    """Takes a queryset and a list of field names that the search string can act
    on."""
    # Split the string in case of first name, surname e.t.c
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        for field in field_names:
            q_filter |= Q(**{"%s__icontains" % field: search_string})
    results = queryset.filter(q_filter)

    # results = as_of_date_filter(results, as_of_date=None)
    # redundant just for documentation
    # filter already applied on regpersons
    return results


def search_geo_tags(regpersons_queryset, search_string, as_of_date=None):
    # geographical areas
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        q_filter |= Q(**{"area_name__icontains": search_string})
    areas_matched = SetupGeography.objects.filter(q_filter)
    area_param = areas_matched.values_list("area_id")
    persons_geo = RegPersonsGeo.objects.filter(area_id__in=area_param)
    # persons_geo = as_of_date_filter(persons_geo, as_of_date=None)
    persons_param = persons_geo.values_list("person__id")
    matches = regpersons_queryset.filter(id__in=persons_param)

    return matches


def search_parent_orgs(regpersons_queryset, search_string, as_of_date=None):
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    query_param = "parent_org_unit__org_unit_name__icontains"
    for search_string in search_strings:
        q_filter |= Q(**{query_param: search_string})
    parent_org_unit_matches = RegPersonsOrgUnits.objects.filter(q_filter)
    # parent_org_unit_matches = as_of_date_filter(parent_org_unit_matches,
    #                                                as_of_date=None)
    p_param = parent_org_unit_matches.values_list("person__id")
    parent_org_unit_match_persons = regpersons_queryset.filter(id__in=p_param)

    return parent_org_unit_match_persons


def filter_age(regpersons_queryset, age=None, as_of_date=None):
    # convert the age to a timedelta
    age_datetime = datetime.timedelta(365 * int(age))
    if as_of_date:
        required_year_of_birth = as_of_date - age_datetime
    else:
        required_year_of_birth = datetime.datetime.today() - age_datetime

    one_year_time_delta = datetime.timedelta(days=365)
    results = regpersons_queryset.filter(
        date_of_birth__range=[required_year_of_birth - one_year_time_delta,
                              required_year_of_birth + one_year_time_delta])

    return results


def person_type_filter(regpersons_queryset, passed_in_persons_types):
    """in_person_types: list of person types we want to search in (tbvc, tbgr,
       twvl, twne, twge), if not specified, search in all person types. if
       as_of_date provided, look at records where (date_delinked is null or
       date_delinked > as_of_date)
    """
    person_types = RegPersonsTypes.objects.filter(
        person_type_id__in=passed_in_persons_types)
    regpersons_queryset = regpersons_queryset.filter(
        id__in=person_types.values('person'))
    return regpersons_queryset


def rank_results(results_dict, required_fields, rank_order):
    """First pick out the required fields from the results dict."""
    # Choose the required items
    # Rank them and ensure no duplicates
    ranked_results = []
    for field in rank_order:
        if field in required_fields:
            try:
                field_results = results_dict[field]
                for person in field_results:
                    if person not in ranked_results:
                        ranked_results.append(person)
            except KeyError:
                pass
    return ranked_results


def get_list_of_persons(search_string,
                        search_string_look_in=["names", "core_ids",
                                               "parent_orgs", "geo_tags"],
                        age=None, has_beneficiary_id=False,
                        has_workforce_id=False, as_of_date=None,
                        in_person_types=[], number_of_results=5,
                        include_died=True, sex=None, include_void=False,
                        ):
    """
    search_string: The text the user has entered in the control. Used for
    searching among the following:
        Names

        NRC
        Birth Certificate
        Workforce ID
        Beneficiary ID
        Geographical tags

        Names of parent org units of the person
    search search_string_look_in: What field search looks in, One or more of:
        Core IDs
        Names
        Parent Org Units
    age: Match against people with +-1 year of specific age. If not specified
    do not use. If as of date provided, calculate age as of that date
        else calculate age on current date.
    sex: SMAL or SFEM - If not specified, do not filter by sex
    has_beneficiary_id: True or False or not specified - Whether we want the
    to search among persons with beneficiary ids, persons without
        beneficiary_ids or all persons regardless of whether or not they have
        the beneficiary_id
    has_work_force_id: True or False or not specified. Whether to search among
    persons with workforce ids, persons without workforce ids, or all
        persons regardless of whether or not they have a workforce id
    as_of_date: A date or not specified. If not specified, we assume we want
    current data (date delinked is null). If specified, when looking at
        date_delinked, date_of_death e.t.c we regard them as still linked,
        still alive e.t.c if the date delinked or date_of_death occurs after
        this parameter date.
    in_person_types: List of person types we want to search in (TBVC, TBGR,
        TWVL, TWNE, TWGE), if not specified, search in all person types. If
        as_of_date provided, look at records where (date_delinked is null or
        date_delinked > as_of_date)
    include_void: True or False. If unspecified we assume fals. Whether to
    include records where tbl_reg_persons.void = true or not

    include_died: True or false. If unspecified we assume true. Whether to
    include persons who have died or not. Note if as_of_date provided and
    include_ died is false, look at records where (date_of_death is null)

    number_of_results: Limit to number of results to be returned. If not
    specified, assume unlimited.

    All the other filters come after that.
    """
    regpersons_queryset = as_of_date_filter(RegPerson.objects.all(),
                                            as_of_date, include_died)
    if age:
        regpersons_queryset = filter_age(regpersons_queryset, age, as_of_date)
    if in_person_types:
        regpersons_queryset = person_type_filter(regpersons_queryset,
                                                 in_person_types)
    regpersons_queryset = regpersons_queryset.filter(is_void=include_void)
    if sex:
        regpersons_queryset = regpersons_queryset.filter(sex_id__iexact=sex)
    if has_beneficiary_id:
        regpersons_queryset = regpersons_queryset.filter(
            beneficiary_id__isnull=False)
    if has_workforce_id:
        regpersons_queryset = regpersons_queryset.filter(
            workforce_id__isnull=False)

    field_names = ['first_name', 'other_names', 'surname']
    name_results = direct_field_search(regpersons_queryset,
                                       field_names=field_names,
                                       search_string=search_string)

    core_id_results = search_core_ids(regpersons_queryset,
                                      search_string=search_string)
    geo_tag_results = search_geo_tags(regpersons_queryset, search_string)
    parent_orgs_results = search_parent_orgs(regpersons_queryset,
                                             search_string)
    results_dict = {
        "names": name_results,
        "core_ids": core_id_results,
        "geo_tags": geo_tag_results,
        "parent_orgs": parent_orgs_results,
    }
    rank_order = ['names', 'core_ids', 'geo_tags', 'parent_orgs']
    ranked_results = rank_results(results_dict, search_string_look_in,
                                  rank_order)
    return ranked_results[:number_of_results]


def search_geo_org_tags(queryset, search_string, as_of_date=None):
    # geographical areas
    search_strings = tokenize_search_string(search_string)
    q_filter = Q()
    for search_string in search_strings:
        q_filter |= Q(**{"area_name__icontains": search_string})
    areas_matched = SetupGeography.objects.filter(q_filter)
    a_param = areas_matched.values_list("area_id")
    reg_org_units_geo = RegOrgUnitGeography.objects.filter(area_id__in=a_param)
    # reg_org_units_geo = as_of_date_filter(reg_org_units_geo, as_of_date=None)
    geo_param = reg_org_units_geo.values_list("org_unit__id")
    matches = queryset.filter(id__in=geo_param)

    return matches


def org_unit_type_filter(queryset, passed_in_org_types):
    for passed_in_org_type in passed_in_org_types:
        queryset = queryset.filter(org_unit_type_id=passed_in_org_type)
    return queryset


def include_closed_filter(queryset, as_of_date=None, include_closed=True):
    """include_closed: True or false. If unspecified, we assume true.
        whether to include org units which have closed or not. Not if
        as_of_date provided and include_closed is false, look at records
        where (date_closed is null or date_closed > as_of_date)"""
    if include_closed:
        pass
    else:
        if as_of_date:
            queryset = queryset.exclude(date_closed__lt=as_of_date)
        else:
            queryset = queryset.exclude(date_closed__isnull=False)
    '''
    if not as_of_date and not include_closed:
        try:
            queryset = queryset.filter(date_closed__isnull=False)
        except FieldError:
            pass
    '''
    if as_of_date:
        try:
            queryset = queryset.exclude(date_closed__lt=as_of_date)
        except FieldError:
            try:
                queryset = queryset.exclude(date_closed__lt=as_of_date)
            except FieldError:
                pass
    return queryset


def get_list_of_org_units(search_string, as_of_date=None, in_org_unit_types=[],
                          include_closed=True, include_void=False,
                          number_of_results=5,
                          search_string_look_in=['names', 'geo_tags']):
    """
    search_string: The text the user has entered in the control. Used for
    searching among the following:
        org_unit_name
        org_unit_id
        geographical_tags

    search_string_look_in: What field search looks in, One or more of:
        Names, org_id

    as_of_date: A date or not specified. If not specified, we assume we want
    current data (date delinked is null). If specified, when looking at
    date_delinked, date_of_death e.t.c we regard them as still linked, still
    alive e.t.c if the date delinked or date_of_death occurs after this
    parameter date.

    in_org_unit_types: List of org unit types we want to search in.
        If not specified, assume we want to search in all org unit
        types. Note if as_of_date is provided, look at records where
        (date_delinked is null or date_delinked > as_of_date)

    include_closed: True or false. If unspecified, we assume true.
        whether to include org units which have closed or not. Not if
        as_of_date provided and include_closed is false, look at records
        where (date_closed is null or date_closed > as_of_date)

    include_void: True or False. If unspecified we assume false. Whether to
    include records where tbl_reg_persons.void = true or not

    number_of_results: Limit to number of results to be returned. If not
    specified, assume unlimited.
    """
    queryset = include_closed_filter(RegOrgUnit.objects.all(), as_of_date,
                                     include_closed)
    if in_org_unit_types:
        queryset = org_unit_type_filter(queryset, in_org_unit_types)

    queryset = queryset.filter(is_void=include_void)
    # queryset = include_closed_filter(queryset, as_of_date, include_closed)

    field_names = ["org_unit_id_vis", "org_unit_name"]
    name_results = direct_field_search(queryset, field_names=field_names,
                                       search_string=search_string)

    geo_tag_results = search_geo_org_tags(queryset, search_string)

    results_dict = {
        "names": name_results,
        "geo_tags": geo_tag_results,
    }
    rank_order = ['names', 'geo_tags']
    ranked_results = rank_results(results_dict, search_string_look_in,
                                  rank_order)
    return ranked_results[:number_of_results]
