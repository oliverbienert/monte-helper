-- noinspection SqlResolve
SELECT
  ac.child_id              child_id,
  c.name                   name,
  c.firstname              firstname,
  b.birthdate              birthdate,
  cb.benefit               benefit,
  calcyear(b.birthdate)    yearcalculated,
  ry.year_id               year_id,
  length(r1.ruling_id) > 0 exdt
FROM adults_children ac
  INNER JOIN people c ON ac.child_id = c.people_id
  INNER JOIN birthdate b ON c.people_id = b.child_id
  LEFT JOIN realyear ry ON ac.child_id = ry.child_id
  LEFT JOIN childbenefit cb ON ac.child_id = cb.child_id
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
  WHERE adult_id = ?
)
      AND flags IN (1, 3)
GROUP BY ac.child_id, c.name, c.firstname, b.birthdate, cb.benefit, yearcalculated, ry.year_id
ORDER BY b.birthdate