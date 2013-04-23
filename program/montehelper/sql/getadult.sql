select distinct a.people_id adult_id, a.name, a.firstname, ad.address_id, ad.street, ad.number, ad.postcode, ad.city, h.size householdsize
from people a
left join adults_addresses aa on a.people_id = aa.adult_id
left join addresses ad on aa.address_id = ad.address_id
left join householdsize h on a.people_id = h.adult_id
where a.people_id = ?