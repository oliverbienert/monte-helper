SELECT
  af.fonnumber_id     fonnumber_id,
  fn.number           number,
  af.fonnumbertype_id fonnumbertype_id,
  l.description       description
FROM adults_fonnumbers af
  INNER JOIN fonnumbers fn ON af.fonnumber_id = fn.fonnumber_id
  LEFT JOIN l_fonnumbertypes l ON af.fonnumbertype_id = l.fonnumbertype_id
WHERE af.adult_id = ?