SELECT DISTINCT
  a.name      name,
  a.firstname firstname,
  ad.street   street,
  ad.number   number,
  ad.postcode postcode,
  ad.city     city
FROM people a
  LEFT JOIN adults_addresses aa ON a.people_id = aa.adult_id
  LEFT JOIN addresses ad ON aa.address_id = ad.address_id
WHERE a.people_id = ?