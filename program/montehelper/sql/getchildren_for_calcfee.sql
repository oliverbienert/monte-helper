select ac.child_id, c.name, c.firstname, b.birthdate, cb.benefit, calcyear(b.birthdate) yearcalculated,
 ry.year_id, length(r1.ruling_id)>0 exdt
from adults_children ac
inner join people c on ac.child_id = c.people_id
inner join birthdate b on c.people_id = b.child_id
left join realyear ry on ac.child_id = ry.child_id
left join childbenefit cb on ac.child_id = cb.child_id
left join (
	select child_id, ruling_id
	from rulings
	where ruling_id = 'extendeddaytime'
	and date(startdate) < date(?) 
	and date(enddate) > date(?)
) r1 on c.people_id = r1.child_id
where ac.child_id in (
        select child_id
        from adults_children
        where adult_id = ?
)
and flags in (1, 3)
group by ac.child_id, c.name, c.firstname, b.birthdate, cb.benefit, yearcalculated, ry.year_id 
order by b.birthdate