# haga-digital-prosjektkalkulator
Prosjektkalkulator for enkeltpersonsforetak - Haga Digital

## Supabase-oppsett (managed Postgres)

Appen har na valgfri Supabase-lagring med fallback til lokal fil/session.

### 1) Opprett Supabase-prosjekt

Hent disse verdiene fra Supabase:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Lag i tillegg en fast bruker-id (UUID) for forste versjon:
- `APP_USER_ID`

### 2) Kjor database-schema

Kjor SQL fra [supabase/001_init.sql](supabase/001_init.sql) i Supabase SQL Editor.

### 3) Sett secrets lokalt

Opprett `.streamlit/secrets.toml` med:

```toml
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "YOUR_SERVICE_ROLE_KEY"
APP_USER_ID = "00000000-0000-0000-0000-000000000001"
USE_SUPABASE = "true"
```

### 4) Installer avhengigheter

```bash
pip install streamlit streamlit-lightweight-charts supabase fpdf2
```

### 5) Kjor appen

```bash
streamlit run enk_kalkulator_app.py
```

## Kontrollert overgang

- Når `USE_SUPABASE = "true"`: appen leser/skriver årlige kostnader og lagrede prosjekter i Supabase.
- Når `USE_SUPABASE = "false"`: appen bruker lokal fallback (dagens adferd).
