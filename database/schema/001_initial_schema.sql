-- ==========================================
-- CareerCopilot
-- Initial Schema V1
-- ==========================================

-- Enable UUID generation
create extension if not exists "pgcrypto";

-- ==========================================
-- Table: sources
-- Stores job sources (RemoteOK, Lever, etc.)
-- ==========================================

create table if not exists sources (
    id uuid primary key default gen_random_uuid(),

    name varchar(100) not null unique,

    source_type varchar(50) not null,

    active boolean not null default true,

    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

-- ==========================================
-- Indexes
-- ==========================================

create index if not exists idx_sources_name
on sources(name);

-- ==========================================
-- Seed data
-- ==========================================

insert into sources (name, source_type)
values
('RemoteOK', 'API'),
('Remotive', 'API'),
('Greenhouse', 'ATS'),
('Lever', 'ATS'),
('Ashby', 'ATS'),
('France Travail', 'API')
on conflict (name) do nothing;
