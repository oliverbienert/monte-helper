SELECT
  e.email_id email_id,
  e.email    email,
  ae.note    note
FROM people a
  INNER JOIN adults_emailaddresses ae ON a.people_id = ae.adult_id
  INNER JOIN emailaddresses e ON ae.email_id = e.email_id
WHERE a.people_id = ?