delete from addresses
where address_id not in (
        select address_id
        from adults_addresses
        where address_id is not null
)