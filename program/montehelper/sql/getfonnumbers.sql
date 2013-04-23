select af.fonnumber_id, fn.number, af.fonnumbertype_id, l.description
from adults_fonnumbers af
inner join fonnumbers fn on af.fonnumber_id = fn.fonnumber_id
left join l_fonnumbertypes l on af.fonnumbertype_id = l.fonnumbertype_id
where af.adult_id = ?