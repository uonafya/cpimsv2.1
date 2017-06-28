QUERIES = {}
# Registration
QUERIES['registration'] = '''
select reg_org_unit.org_unit_name, reg_person.first_name, reg_person.surname,
reg_person.other_names, reg_person.date_of_birth, registration_date,
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
CASE has_bcert WHEN 'True' THEN 'HAS BIRTHCERT' ELSE 'NO BIRTHCERT' END AS BirthCert,
CASE has_bcert WHEN 'True' THEN 'BCERT' ELSE NULL END AS BCertNumber,
CASE is_disabled WHEN 'True' THEN 'HAS DISABILITY' ELSE 'NO DISABILITY' END AS OVCDisability,
CASE is_Disabled WHEN 'True' THEN 'NCPWD' ELSE NULL END AS NCPWDNumber,
CASE hiv_status WHEN 'HSTP' THEN 'POSITIVE' ELSE 'NOT KNOWN' END AS OVCHIVstatus,
CASE hiv_status WHEN 'HSTP' THEN 'ART' ELSE NULL END AS ARTStatus,
reg_person.date_of_birth
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
where child_cbo_id in (%s);'''


# PEPFAR
QUERIES['pepfar'] = '''
select ovc_care_services.service_provided,
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
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
and child_cbo_id in (%s)
GROUP BY ovc_care_services.service_provided, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
list_geo.area_name;'''

# DATIM
QUERIES['datim'] = '''
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
AND ovc_registration.child_cbo_id in (%s)
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name;'''

# DATIM - Served
# '1. OVC_Serv' as domain
QUERIES['datim_1'] = '''
select 
cast(count(distinct ovc_care_events.person_id) as integer) as OVCCount,
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
and child_cbo_id in (%s)
GROUP BY reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
list_geo.area_name;'''

# DATIM ART
QUERIES['datim_2'] = '''
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
ELSE '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
END AS Domain
from ovc_registration
INNER JOIN reg_person ON ovc_registration.person_id=reg_person.id
LEFT OUTER JOIN reg_org_unit ON reg_org_unit.id=ovc_registration.child_cbo_id
LEFT OUTER JOIN reg_persons_geo ON reg_persons_geo.person_id=ovc_registration.person_id
LEFT OUTER JOIN list_geo ON list_geo.area_id=reg_persons_geo.area_id
LEFT OUTER JOIN ovc_care_health ON ovc_care_health.person_id=ovc_registration.person_id
WHERE ovc_registration.is_active = True AND ovc_registration.hiv_status = 'HSTP'
AND ovc_registration.child_cbo_id in (%s)
GROUP BY ovc_registration.person_id, reg_person.date_of_birth,
reg_person.sex_id, ovc_registration.child_cbo_id,
reg_org_unit.org_unit_name, reg_persons_geo.area_id,
ovc_registration.hiv_status, list_geo.area_name, ovc_care_health.art_status;'''

'''

CASE ovc_care_health.art_status
WHEN ovc_care_health.art_status IS NULL THEN '2a. (iii) OVC_HIVSTAT: HIV+ NOT on ARV Treatment'
ELSE '2a. (ii) OVC_HIVSTAT: HIV+ on ARV Treatment'
END AS Domain
'''
