create table if not exists companies (
    id uuid primary key default gen_random_uuid(),

    name varchar(255) not null unique,

    website text,

    careers_url text,

    country varchar(100),

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_companies_name
on companies(name);