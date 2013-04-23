create table "registrationdate" (
    "people_id" int primary key not null references people(people_id) on delete cascade,
    "date" TEXT not null
);