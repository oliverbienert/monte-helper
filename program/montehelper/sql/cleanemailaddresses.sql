delete from emailaddresses
where email_id not in (
        select email_id
        from adults_emailaddresses
        where email_id is not null
)