create table if not exists "version" (
    "prog" text primary key not null,
    "build" integer not null
);
