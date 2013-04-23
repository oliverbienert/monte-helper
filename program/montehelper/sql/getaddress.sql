select distinct a.name, a.firstname, ad.street, ad.number, ad.postcode, ad.city
from people as a
left join adults_addresses as aa on a.people_id = aa.adult_id
left join addresses as ad on aa.address_id = ad.address_id
where a.people_id = ?