QUERIES = {}
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
hiv_status
from ovc_registration
left outer join reg_person on person_id=reg_person.id
left outer join reg_org_unit on child_cbo_id=reg_org_unit.id
where child_cbo_id in (%s);'''
