delete from fonnumbers
where fonnumber_id not in (
        select fonnumber_id
        from adults_fonnumbers
        where fonnumber_id is not null
)