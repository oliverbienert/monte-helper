select i.income, i.incometype_id, l.description
from income i
inner join l_incometypes l on i.incometype_id = l.incometype_id
where adult_id = ?