SELECT
  ac.adult_id     adult_id,
  a.name          name,
  a.firstname     firstname,
  ac.relation_id  relation_id,
  i.income        income,
  i.incometype_id incometype_id,
  h.size          size,
  ac.flags        flags
FROM adults_children ac
  INNER JOIN people a ON ac.adult_id = a.people_id
  INNER JOIN income i ON a.people_id = i.adult_id
  LEFT JOIN householdsize h ON a.people_id = h.adult_id
WHERE child_id = (
  SELECT child_id
  FROM adults_children
  WHERE adult_id = ?
)
      AND ac.flags IN (1, 3)