QUERIES = {}
# Reports
REPORTS = {}
# Reports listings
REPORTS[1] = 'registration'
REPORTS[2] = 'registration'
REPORTS[3] = 'registration'

# Registration List
QUERIES['registration'] = '''
select reg_org_unit.org_unit_name AS CBO,
reg_person.first_name, reg_person.surname,
reg_person.other_names, reg_person.date_of_birth, registration_date,
date_part('year', age(reg_person.date_of_birth)) AS age,
date_part('year', age(ovc_registration.registration_date,
reg_person.date_of_birth)) AS age_at_reg,
child_cbo_id as OVCID,
list_geo.area_name as ward,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN 'BCERT' ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN 'NCPWD' ELSE NULL END AS NCPWDNumber,
CASE
WHEN hiv_status = 'HSTP' THEN 'POSITIVE'
WHEN hiv_status = 'HSTN' THEN 'NEGATIVE'
ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
concat(chw.first_name,' ',chw.surname,' ',chw.other_names) as CHW,
concat(cgs.first_name,' ',cgs.surname,' ',cgs.other_names) as parent_names,
CASE is_active WHEN 'True' THEN 'ACTIVE' ELSE 'EXITED' END AS Exit_status,
CASE is_active WHEN 'False' THEN exit_date ELSE NULL END AS Exit_date
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_person chw on child_chv_id=chw.id
left outer join reg_person cgs on caretaker_id=cgs.id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
left outer join reg_persons_geo on ovc_registration.person_id=reg_persons_geo.person_id
left outer join list_geo on list_geo.area_id=reg_persons_geo.area_id
where child_cbo_id in (%s);'''

# PEPFAR
QUERIES['pepfar'] = '''
select
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward,
date_part('year', age(reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_services.service_provided
WHEN 'HC1S' THEN 'Health' %s
ELSE 'Unknown'
END AS Domain
from ovc_care_services
INNER JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
INNER JOIN reg_person ON ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON ovc_care_events.person_id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
WHERE ovc_care_services.is_void = False and ovc_care_events.event_type_id='FSAM'
and ovc_care_events.date_of_event between '%s' and '%s'
%s
GROUP BY ovc_care_services.service_provided, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
list_geo.area_name;'''

# DATIM
QUERIES['datim'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward,
date_part('year', age(reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_registration.hiv_status
WHEN 'HSTP' THEN '2a. (i) OVC_HIVSTAT: HIV+'
WHEN 'HSTN' THEN '2b. OVC_HIVSTAT: HIV-'
ELSE '2c. OVC_HIVSTAT: HIV Status NOT Known'
END AS Domain
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
WHERE ovc_registration.is_active = True
%s
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name;'''

# DATIM - Served
# '1. OVC_Serv' as domain
QUERIES['datim_1'] = '''
select 
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward,
date_part('year', age(reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
'1. OVC_Serv' as Domain
from ovc_care_services
INNER JOIN ovc_care_events ON ovc_care_events.event=ovc_care_services.event_id
INNER JOIN reg_person ON ovc_care_events.person_id=reg_person.id
LEFT OUTER JOIN ovc_registration ON ovc_care_events.person_id=ovc_registration.person_id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
WHERE ovc_care_services.is_void = False and ovc_care_events.event_type_id='FSAM'
and ovc_care_events.date_of_event between '%s' and '%s'
%s
GROUP BY reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
list_geo.area_name;'''

# DATIM ART
QUERIES['datim_2'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
reg_org_unit.org_unit_name AS CBO,
list_geo.area_name as ward,
date_part('year', age(reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
WHEN 'ARPR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
WHERE ovc_registration.is_active = True AND ovc_registration.hiv_status = 'HSTP'
%s
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name, ovc_care_health.art_status;'''

# KPI
QUERIES['kpi'] = '''
select
cast(count(distinct ovc_registration.person_id) as integer) as OVCCount,
ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name,
reg_persons_geo.area_id,
list_geo.area_name,
date_part('year', age(reg_person.date_of_birth)) AS age,
CASE
WHEN date_part('year', age(reg_person.date_of_birth)) < 1 THEN 'a.[<1yrs]'
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 1 AND 4 THEN 'b.[1-4yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 5 AND 9 THEN 'c.[5-9yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 10 AND 14 THEN 'd.[10-14yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 15 AND 17 THEN 'e.[15-17yrs]' 
WHEN  date_part('year', age(reg_person.date_of_birth)) BETWEEN 18 AND 24 THEN 'f.[18-24yrs]'
ELSE 'g.[25+yrs]' END AS AgeRange,
CASE reg_person.sex_id WHEN 'SMAL' THEN 'Female' ELSE 'Male' END AS Gender,
CASE ovc_care_health.art_status
WHEN 'ARAR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
WHEN 'ARPR' THEN '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
WHERE ovc_registration.is_active = True AND ovc_registration.hiv_status = 'HSTP'
%s
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name, ovc_care_health.art_status;'''
