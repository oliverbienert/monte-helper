select distinct a.people_id adult_id, a.name, a.firstname, f.number, f.fonnumbertype_id, f.description 
from people a
left outer join (
    select af.adult_id, af.fonnumber_id, fn.number, af.fonnumbertype_id, l.description
    from adults_fonnumbers af
    inner join fonnumbers fn on af.fonnumber_id = fn.fonnumber_id
    left join l_fonnumbertypes l on af.fonnumbertype_id = l.fonnumbertype_id
) f on a.people_id = f.adult_id
where people_type = 'adult'