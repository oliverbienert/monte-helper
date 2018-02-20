SELECT
  r.ruling_id   ruling_id,
  l.description description,
  r.startdate   startdate,
  r.enddate     enddate
FROM rulings r
  INNER JOIN l_rulings l ON r.ruling_id = l.ruling_id
WHERE child_id = ?