SELECT
  ac.adult_id    adult_id,
  a.name         name,
  a.firstname    firstname,
  ac.relation_id relation_id,
  l.description  description,
  ac.flags       flags
FROM adults_children ac
  INNER JOIN people a ON ac.adult_id = a.people_id
  INNER JOIN l_relations l ON ac.relation_id = l.relation_id
WHERE ac.child_id = ?