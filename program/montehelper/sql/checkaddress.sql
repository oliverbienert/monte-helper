SELECT
  a.address_id address_id,
  street,
  number,
  postcode,
  city
FROM adults_addresses aa
  INNER JOIN addresses a ON aa.address_id = a.address_id
                            AND adult_id = ?