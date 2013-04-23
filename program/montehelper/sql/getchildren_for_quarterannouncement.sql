select ac.child_id, c.name, c.firstname, b.birthdate, (a.street || " " || a.number) address, a.postcode,
city, l.district, calcyear(b.birthdate) yearcalculated, ry.year_id, length(r1.ruling_id)>0 exdt
from adults_children ac
inner join people c on ac.child_id = c.people_id
inner join people cp on ac.adult_id = cp.people_id
inner join adults_addresses aa on cp.people_id = aa.adult_id
inner join addresses a on aa.address_id = a.address_id
inner join birthdate b on c.people_id = b.child_id
left join l_postcode_district l on a.postcode = l.postcode
left join realyear ry on ac.child_id = ry.child_id
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
)
and flags in (2, 3)