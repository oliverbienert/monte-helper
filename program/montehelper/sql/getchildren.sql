SELECT
  c.people_id         child_id,
  c.name              name,
  c.firstname         firstname,
  b.birthdate         birthdate,
  calcyear(birthdate) yearcalculated,
  ly.description      yc_description,
  ry.year_id          year_id
FROM people c
  INNER JOIN birthdate b ON c.people_id = b.child_id
  LEFT JOIN l_year ly ON yearcalculated = ly.year_id
  LEFT JOIN (
              SELECT
                ry.child_id,
                ry.year_id
              FROM realyear ry
            ) ry ON c.people_id = ry.child_id
WHERE c.people_type = 'child'