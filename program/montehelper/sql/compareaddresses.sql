select address_id
from addresses
where street = ? collate caseinsensitive
and number = ? collate caseinsensitive
and postcode = ? collate caseinsensitive
and city = ? collate caseinsensitive