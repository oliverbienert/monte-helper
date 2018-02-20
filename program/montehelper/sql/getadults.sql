SELECT DISTINCT
  a.people_id        adult_id,
  a.name             name,
  a.firstname        firstname,
  f.number           number,
  f.fonnumbertype_id fonnumbertype_id,
  f.description      description
FROM people a
  LEFT OUTER JOIN (
                    SELECT
                      af.adult_id,
                      af.fonnumber_id,
                      fn.number,
                      af.fonnumbertype_id,
                      l.description
                    FROM adults_fonnumbers af
                      INNER JOIN fonnumbers fn ON af.fonnumber_id = fn.fonnumber_id
                      LEFT JOIN l_fonnumbertypes l ON af.fonnumbertype_id = l.fonnumbertype_id
                  ) f ON a.people_id = f.adult_id
WHERE people_type = 'adult'