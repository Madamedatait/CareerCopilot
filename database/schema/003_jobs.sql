create table if not exists jobs (
    id uuid primary key default gen_random_uuid(),

    company_id uuid not null references companies(id),

    source_id uuid not null references sources(id),

    title varchar(255) not null,

    location varchar(255),

    country varchar(100),

    remote_type varchar(50),

    employment_type varchar(50),

    salary_min integer,

    salary_max integer,

    salary_currency varchar(10),

    job_url text not null,

    description text,

    posted_at timestamptz,

    collected_at timestamptz not null default now(),

    status varchar(50) default 'active',

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_jobs_company
on jobs(company_id);

create index if not exists idx_jobs_source
on jobs(source_id);

create index if not exists idx_jobs_country
on jobs(country);

create index if not exists idx_jobs_remote
on jobs(remote_type);
