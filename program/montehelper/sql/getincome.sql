SELECT
  i.income        income,
  i.incometype_id incometype_id,
  l.description   description
FROM income i
  INNER JOIN l_incometypes l ON i.incometype_id = l.incometype_id
WHERE adult_id = ?