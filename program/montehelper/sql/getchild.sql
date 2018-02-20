SELECT DISTINCT
  c.people_id         child_id,
  c.name              name,
  c.firstname         firstname,
  b.birthdate         birthdate,
  ry.year_id          year,
  cb.benefit          benefit,
  calcyear(birthdate) yearcalculated,
  ly.description      yc_description,
  j.date              joindate,
  s.date              separationdate
FROM people c
  INNER JOIN birthdate b ON c.people_id = b.child_id
  LEFT JOIN l_year ly ON yearcalculated = ly.year_id
  LEFT JOIN (
              SELECT
                r.child_id,
                r.year_id,
                l.description
              FROM realyear r
                INNER JOIN l_year l ON r.year_id = l.year_id
            ) ry ON c.people_id = ry.child_id
  LEFT JOIN childbenefit cb ON c.people_id = cb.child_id
  LEFT JOIN joindates j ON (c.people_id = j.people_id AND j.type_id = 'school')
  LEFT JOIN separationdates s ON (c.people_id = s.people_id AND s.type_id = 'school')
WHERE c.people_id = ?