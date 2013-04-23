select a.address_id, street, number, postcode, city
from adults_addresses aa
inner join addresses a on aa.address_id = a.address_id
and adult_id = ?