select c.people_id child_id, c.name, c.firstname, b.birthdate, calcyear(birthdate) yearcalculated, 
 ly.description yc_description, ry.year_id
from people c
inner join birthdate b on c.people_id = b.child_id
left join l_year ly on yearcalculated = ly.year_id
left join (
	select ry.child_id, ry.year_id
	from realyear ry
) ry on c.people_id = ry.child_id
where c.people_type = 'child'