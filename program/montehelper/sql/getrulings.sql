select r.ruling_id, l.description, r.startdate, r.enddate
from rulings r 
inner join l_rulings l on r.ruling_id = l.ruling_id
where child_id = ?