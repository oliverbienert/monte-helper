select distinct c.people_id child_id, c.name, c.firstname, b.birthdate,
 ry.year_id year, cb.benefit, calcyear(birthdate) yearcalculated, ly.description yc_description,
 j.date joindate, s.date separationdate
from people c
inner join birthdate b on c.people_id = b.child_id
left join l_year ly on yearcalculated = ly.year_id
left join (
    select r.child_id, r.year_id, l.description
    from realyear r
    inner join l_year l on r.year_id = l.year_id
) ry on c.people_id = ry.child_id
left join childbenefit cb on c.people_id = cb.child_id
left join joindates j on (c.people_id = j.people_id and j.type_id = 'school')
left join separationdates s on (c.people_id = s.people_id and s.type_id = 'school')
where c.people_id = ?