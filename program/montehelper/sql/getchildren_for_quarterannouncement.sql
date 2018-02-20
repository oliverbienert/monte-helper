SELECT
  ac.child_id                   child_id,
  c.name                        name,
  c.firstname                   firstname,
  b.birthdate                   birthdate,
  (a.street || ' ' || a.number) address,
  a.postcode                    postcode,
  city,
  l.district                    district,
  calcyear(b.birthdate)         yearcalculated,
  ry.year_id                    year_id,
  length(r1.ruling_id) > 0      exdt
FROM adults_children ac
  INNER JOIN people c ON ac.child_id = c.people_id
  INNER JOIN people cp ON ac.adult_id = cp.people_id
  INNER JOIN adults_addresses aa ON cp.people_id = aa.adult_id
  INNER JOIN addresses a ON aa.address_id = a.address_id
  INNER JOIN birthdate b ON c.people_id = b.child_id
  LEFT JOIN l_postcode_district l ON a.postcode = l.postcode
  LEFT JOIN realyear ry ON ac.child_id = ry.child_id
  LEFT JOIN (
              SELECT
                child_id,
                ruling_id
              FROM rulings
              WHERE ruling_id = 'extendeddaytime'
                    AND date(startdate) < date(?)
                    AND date(enddate) > date(?)
            ) r1 ON c.people_id = r1.child_id
WHERE ac.child_id IN (
  SELECT child_id
  FROM adults_children
)
AND flags IN (2, 3)