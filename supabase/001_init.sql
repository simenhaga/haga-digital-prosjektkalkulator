-- Supabase schema for Haga Digital ENK-kalkulator (single fixed user_id)

create extension if not exists "pgcrypto";

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table if not exists public.annual_costs (
  id bigserial primary key,
  user_id uuid not null,
  name text not null check (char_length(trim(name)) > 0),
  amount numeric(12,2) not null default 0 check (amount >= 0),
  sort_order integer not null default 1,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists annual_costs_user_id_idx
  on public.annual_costs (user_id);

create unique index if not exists annual_costs_user_sort_order_uidx
  on public.annual_costs (user_id, sort_order);

drop trigger if exists trg_annual_costs_updated_at on public.annual_costs;
create trigger trg_annual_costs_updated_at
before update on public.annual_costs
for each row execute function public.set_updated_at();

create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  name text not null check (char_length(trim(name)) > 0),
  mode text not null check (mode in ('Prosjektkalkulator', 'Timepriskalkulator')),
  saved_at timestamptz not null default now(),
  result_json jsonb not null default '{}'::jsonb,
  extra_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists projects_user_id_saved_at_idx
  on public.projects (user_id, saved_at desc);

drop trigger if exists trg_projects_updated_at on public.projects;
create trigger trg_projects_updated_at
before update on public.projects
for each row execute function public.set_updated_at();
