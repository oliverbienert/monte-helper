SELECT DISTINCT
  a.people_id   adult_id,
  a.name        name,
  a.firstname   firstname,
  ad.address_id address_id,
  ad.street     street,
  ad.number     number,
  ad.postcode   postcode,
  ad.city       city,
  h.size        householdsize
FROM people a
  LEFT JOIN adults_addresses aa ON a.people_id = aa.adult_id
  LEFT JOIN addresses ad ON aa.address_id = ad.address_id
  LEFT JOIN householdsize h ON a.people_id = h.adult_id
WHERE a.people_id = ?