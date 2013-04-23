select ac.adult_id, a.name, a.firstname, ac.relation_id, i.income, i.incometype_id, h.size, ac.flags
from adults_children ac
inner join people a on ac.adult_id = a.people_id
inner join income i on a.people_id = i.adult_id
left join householdsize h on a.people_id = h.adult_id
where child_id = (
        select child_id
        from adults_children
        where adult_id = ?
)
and ac.flags in (1, 3)