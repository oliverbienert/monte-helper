select e.email_id, e.email, ae.note
from people as a
inner join adults_emailaddresses as ae on a.people_id = ae.adult_id
inner join emailaddresses as e on ae.email_id = e.email_id
where a.people_id = ?