select ac.adult_id, a.name, a.firstname, ac.relation_id, l.description, ac.flags
from adults_children ac 
inner join people a on ac.adult_id = a.people_id
inner join l_relations l on ac.relation_id = l.relation_id
where ac.child_id = ?