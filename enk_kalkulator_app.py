import json
from datetime import datetime
from pathlib import Path

import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(page_title="Haga Digital ENK-kalkulator", page_icon="💼", layout="wide")

LOGO_PATH = Path("assets/logo2.png")
ANNUAL_COSTS_PATH = Path("assets/annual_costs.json")

PALETTE = {
    "bg": "#F7F8FB",
    "card": "rgba(255,255,255,0.88)",
    "card_border": "rgba(17,24,39,0.06)",
    "text": "#111827",
    "muted": "#667085",
    "blue": "#7AA2FF",
    "mint": "#74D9B6",
    "peach": "#FFB58A",
    "lavender": "#B49CFF",
    "yellow": "#F4C95D",
}

st.markdown(
    """
    <style>
    .stApp {
        background: #F7F8FB;
        color: #111827;
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1380px;
    }
    .hero {
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(17,24,39,0.06);
        border-radius: 24px;
        padding: 22px 24px;
        box-shadow: 0 10px 30px rgba(17,24,39,0.05);
        margin-top: 42px;
        margin-bottom: 14px;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        color: #667085;
        font-size: 1rem;
        line-height: 1.5;
    }
    .section-title {
        font-size: 1.08rem;
        font-weight: 650;
        letter-spacing: -0.02em;
        margin: 0.15rem 0 0.85rem 0;
    }
    .metric-card {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(17,24,39,0.08);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 8px 24px rgba(17,24,39,0.06);
        min-height: 116px;
        margin-bottom: 8px;
    }
    .metric-label {
        color: #667085;
        font-size: 0.92rem;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #111827;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        line-height: 1.05;
    }
    .metric-note {
        margin-top: 10px;
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 0.78rem;
        color: #111827;
        background: #F2F4F7;
        border: 1px solid rgba(17,24,39,0.05);
    }
    .card {
        background: rgba(255,255,255,0.96);
        border: 1px solid rgba(17,24,39,0.08);
        border-radius: 24px;
        padding: 18px 20px;
        box-shadow: 0 8px 24px rgba(17,24,39,0.06);
        margin-bottom: 14px;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 650;
        margin-bottom: 0.2rem;
    }
    .card-subtitle {
        color: #667085;
        font-size: 0.9rem;
        margin-bottom: 0.8rem;
        line-height: 1.45;
    }
    .legend-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 8px;
        margin-bottom: 10px;
    }
    .legend-pill {
        padding: 7px 11px;
        border-radius: 999px;
        font-size: 0.82rem;
        color: #111827;
        background: #F2F4F7;
        border: 1px solid rgba(17,24,39,0.05);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: transparent;
        border: none;
        padding: 0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 12px;
        padding-left: 14px;
        padding-right: 14px;
        color: #667085;
        background: rgba(255,255,255,0.7);
        border: 1px solid rgba(17,24,39,0.06);
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #111827 !important;
        box-shadow: 0 4px 14px rgba(17,24,39,0.05);
    }
    div[data-testid="stSidebar"] > div:first-child {
        background: #FFFFFF;
        border-right: 1px solid rgba(17,24,39,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def nok(value: float) -> str:
    return f"{value:,.0f} kr".replace(",", " ")


def metric_card(label: str, value: str, note: str = ""):
    note_html = f'<div class="metric-note">{note}</div>' if note else ""
    st.markdown(
        f"""
        <div style=\"background: rgba(255,255,255,0.96); border: 1px solid rgba(17,24,39,0.08); border-radius: 22px; padding: 18px; box-shadow: 0 8px 24px rgba(17,24,39,0.06); min-height: 116px; margin-bottom: 8px;\">
            <div style=\"color: #667085; font-size: 0.92rem; margin-bottom: 10px;\">{label}</div>
            <div style=\"color: #111827; font-size: 2rem; font-weight: 700; letter-spacing: -0.04em; line-height: 1.05;\">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_start(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div style=\"background: rgba(255,255,255,0.96); border: 1px solid rgba(17,24,39,0.08); border-radius: 24px; padding: 18px 20px; box-shadow: 0 8px 24px rgba(17,24,39,0.06); margin-bottom: 14px;\">
            <div style=\"font-size: 1rem; font-weight: 650; margin-bottom: 0.2rem;\">{title}</div>
            <div style=\"color: #667085; font-size: 0.9rem; margin-bottom: 0.8rem; line-height: 1.45;\">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def card_end():
    st.markdown("</div>", unsafe_allow_html=True)


DEFAULTS = {
    "mva_rate": 25.0,
    "skatt_rate": 35.0,
    "aarlige_programvarekostnader": 2500.0,
    "fiken_maned": 209.0,
    "fiken_prosjekt_maned": 59.0,
    "fiken_skattemelding_aar": 1290.0,
}


def init_state():
    if "annual_costs" not in st.session_state:
        st.session_state.annual_costs = load_annual_costs()
    if "project_expenses" not in st.session_state:
        st.session_state.project_expenses = [{"id": 1, "name": "Prosjektkostnad 1", "amount": 0.0}]
    if "saved_projects" not in st.session_state:
        st.session_state.saved_projects = []
    if "prosjektpris" not in st.session_state:
        st.session_state.prosjektpris = 0.0
    if "prosjektkostnader" not in st.session_state:
        st.session_state.prosjektkostnader = 0.0
    if "editing_saved_project_index" not in st.session_state:
        st.session_state.editing_saved_project_index = None


def add_annual_cost():
    next_id = max((item["id"] for item in st.session_state.annual_costs), default=0) + 1
    st.session_state.annual_costs.append({"id": next_id, "name": f"Årlig kostnad {next_id}", "amount": 0.0})
    save_annual_costs(st.session_state.annual_costs)


def remove_annual_cost(item_id: int):
    st.session_state.annual_costs = [item for item in st.session_state.annual_costs if item["id"] != item_id]
    save_annual_costs(st.session_state.annual_costs)


def load_annual_costs() -> list[dict]:
    if not ANNUAL_COSTS_PATH.exists():
        return []

    try:
        with ANNUAL_COSTS_PATH.open("r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    if not isinstance(raw_data, list):
        return []

    cleaned: list[dict] = []
    next_id = 1
    for item in raw_data:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        amount = max(0.0, float(item.get("amount", 0.0)))
        if not name:
            continue
        cleaned.append({"id": next_id, "name": name, "amount": amount})
        next_id += 1
    return cleaned


def save_annual_costs(items: list[dict]):
    ANNUAL_COSTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = [{"name": str(item.get("name", "")).strip(), "amount": max(0.0, float(item.get("amount", 0.0)))} for item in items]
    with ANNUAL_COSTS_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def add_project_expense():
    next_id = max((item["id"] for item in st.session_state.project_expenses), default=0) + 1
    st.session_state.project_expenses.append({"id": next_id, "name": f"Prosjektkostnad {next_id}", "amount": 0.0})


def remove_project_expense(item_id: int):
    st.session_state.project_expenses = [item for item in st.session_state.project_expenses if item["id"] != item_id]


def total_from_items(items: list[dict]) -> float:
    return sum(max(0.0, float(item.get("amount", 0.0))) for item in items)


def beregn_prosjekt(
    prosjektpris_eks_mva: float,
    aarlige_kostnader: float,
    prosjektspesifikke_kostnader: float,
    skatt_rate: float,
    mva_rate: float,
    mva_pliktig: bool,
):
    mva_belop = prosjektpris_eks_mva * (mva_rate / 100) if mva_pliktig else 0.0
    faktura_inkl_mva = prosjektpris_eks_mva + mva_belop
    totale_kostnader = aarlige_kostnader + prosjektspesifikke_kostnader
    resultat_for_skatt = prosjektpris_eks_mva - totale_kostnader
    estimert_skatt = max(0.0, resultat_for_skatt) * (skatt_rate / 100)
    netto_etter_skatt = resultat_for_skatt - estimert_skatt
    anbefalt_avsetning = estimert_skatt + mva_belop

    return {
        "prosjektpris_eks_mva": prosjektpris_eks_mva,
        "mva_belop": mva_belop,
        "faktura_inkl_mva": faktura_inkl_mva,
        "totale_kostnader": totale_kostnader,
        "resultat_for_skatt": resultat_for_skatt,
        "estimert_skatt": estimert_skatt,
        "netto_etter_skatt": netto_etter_skatt,
        "anbefalt_avsetning": anbefalt_avsetning,
        "tooltips": {
            "faktura_inkl_mva": f"Prosjektpris eks. mva ({nok(prosjektpris_eks_mva)}) + MVA ({nok(mva_belop)})",
            "mva_belop": f"Prosjektpris eks. mva ({nok(prosjektpris_eks_mva)}) × {mva_rate:.0f}% = {nok(mva_belop)}",
            "totale_kostnader": f"Årlige kostnader ({nok(aarlige_kostnader)}) + prosjektkostnader ({nok(prosjektspesifikke_kostnader)}) = {nok(totale_kostnader)}",
            "resultat_for_skatt": f"Prosjektpris eks. mva ({nok(prosjektpris_eks_mva)}) - totale kostnader ({nok(totale_kostnader)}) = {nok(resultat_for_skatt)}",
            "estimert_skatt": f"Maks(0, resultat før skatt {nok(resultat_for_skatt)}) × {skatt_rate:.0f}% = {nok(estimert_skatt)}",
            "netto_etter_skatt": f"Resultat før skatt ({nok(resultat_for_skatt)}) - estimert skatt ({nok(estimert_skatt)}) = {nok(netto_etter_skatt)}",
            "anbefalt_avsetning": f"Estimert skatt ({nok(estimert_skatt)}) + MVA ({nok(mva_belop)}) = {nok(anbefalt_avsetning)}",
        },
    }


def beregn_timepris(
    timepris_eks_mva: float,
    antall_timer: float,
    aarlige_kostnader: float,
    prosjektspesifikke_kostnader: float,
    skatt_rate: float,
    mva_rate: float,
    mva_pliktig: bool,
):
    prosjektpris_eks_mva = timepris_eks_mva * antall_timer
    return beregn_prosjekt(
        prosjektpris_eks_mva=prosjektpris_eks_mva,
        aarlige_kostnader=aarlige_kostnader,
        prosjektspesifikke_kostnader=prosjektspesifikke_kostnader,
        skatt_rate=skatt_rate,
        mva_rate=mva_rate,
        mva_pliktig=mva_pliktig,
    )


def vis_resultater(resultat: dict, overskrift: str):
    st.subheader(overskrift)
    tips = resultat["tooltips"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faktura inkl. mva", nok(resultat["faktura_inkl_mva"]), help=tips["faktura_inkl_mva"])
    c2.metric("MVA å sette av", nok(resultat["mva_belop"]), help=tips["mva_belop"])
    c3.metric("Resultat før skatt", nok(resultat["resultat_for_skatt"]), help=tips["resultat_for_skatt"])
    c4.metric("Mulig privatuttak etter skatt", nok(resultat["netto_etter_skatt"]), help=tips["netto_etter_skatt"])

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Prosjektpris eks. mva", nok(resultat["prosjektpris_eks_mva"]), help="Beløpet du fakturerer før MVA.")
    d2.metric("Totale kostnader", nok(resultat["totale_kostnader"]), help=tips["totale_kostnader"])
    d3.metric("Estimert skatt", nok(resultat["estimert_skatt"]), help=tips["estimert_skatt"])
    d4.metric("Sett av nå", nok(resultat["anbefalt_avsetning"]), help=tips["anbefalt_avsetning"])

    with st.expander("Se utregninger"):
        st.write(f"- Faktura inkl. mva: {tips['faktura_inkl_mva']}")
        st.write(f"- MVA å sette av: {tips['mva_belop']}")
        st.write(f"- Totale kostnader: {tips['totale_kostnader']}")
        st.write(f"- Resultat før skatt: {tips['resultat_for_skatt']}")
        st.write(f"- Estimert skatt: {tips['estimert_skatt']}")
        st.write(f"- Mulig privatuttak etter skatt: {tips['netto_etter_skatt']}")
        st.write(f"- Sett av nå: {tips['anbefalt_avsetning']}")

    if resultat["resultat_for_skatt"] < 0:
        st.warning("Dette prosjektet går i minus med disse forutsetningene.")
    else:
        st.info("I ENK tar du ikke ut lønn eller utbytte. Beløpet vist som mulig privatuttak etter skatt er det du i praksis kan ta ut privat, gitt disse forutsetningene.")


def save_project(name: str, mode: str, result: dict, extra: dict):
    st.session_state.saved_projects.append(
        {
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "name": name,
            "mode": mode,
            "result": result,
            "extra": extra,
        }
    )


def delete_saved_project(index: int):
    if 0 <= index < len(st.session_state.saved_projects):
        st.session_state.saved_projects.pop(index)


def series_bar(data: list[dict], key: str):
    chart = [
        {
            "chart": {
                "height": 340,
                "layout": {
                    "background": {"type": "solid", "color": "rgba(255,255,255,0)"},
                    "textColor": PALETTE["muted"],
                },
                "rightPriceScale": {"visible": True, "borderVisible": False},
                "leftPriceScale": {"visible": False},
                "timeScale": {"visible": True, "borderVisible": False},
                "crosshair": {"mode": 0},
                "grid": {
                    "vertLines": {"visible": False},
                    "horzLines": {"visible": True, "color": "rgba(17,24,39,0.06)"},
                },
            },
            "series": [
                {
                    "type": "Histogram",
                    "priceFormat": {"type": "price", "precision": 0, "minMove": 1},
                    "data": data,
                }
            ],
        }
    ]
    renderLightweightCharts(chart, key=key)


def series_compare(income_data: list[dict], withdrawal_data: list[dict], key: str):
    chart = [
        {
            "chart": {
                "height": 380,
                "layout": {
                    "background": {"type": "solid", "color": "rgba(255,255,255,0)"},
                    "textColor": PALETTE["muted"],
                },
                "rightPriceScale": {"visible": True, "borderVisible": False},
                "leftPriceScale": {"visible": False},
                "timeScale": {"visible": True, "borderVisible": False},
                "crosshair": {"mode": 1},
                "grid": {
                    "vertLines": {"visible": False},
                    "horzLines": {"visible": True, "color": "rgba(17,24,39,0.06)"},
                },
            },
            "series": [
                {
                    "type": "Area",
                    "data": income_data,
                    "lineColor": PALETTE["blue"],
                    "topColor": "rgba(122,162,255,0.28)",
                    "bottomColor": "rgba(122,162,255,0.04)",
                    "priceFormat": {"type": "price", "precision": 0, "minMove": 1},
                    "title": "Inntekt eks. mva",
                },
                {
                    "type": "Line",
                    "data": withdrawal_data,
                    "lineColor": PALETTE["mint"],
                    "priceFormat": {"type": "price", "precision": 0, "minMove": 1},
                    "title": "Mulig privatuttak",
                },
            ],
        }
    ]
    renderLightweightCharts(chart, key=key)


init_state()

if LOGO_PATH.exists():
    with st.sidebar:
        st.image(str(LOGO_PATH), use_container_width=True)

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">ENK-kalkulator</div>
        <div class="hero-subtitle">En oversiktlig økonomi-app for enkeltpersonforetak. Se inntekt, kostnader, skatt, MVA og mulig privatuttak i et dashboard som er enklere å forstå enn et regneark.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# st.caption("Installer grafpakken med: pip install streamlit-lightweight-charts")

tab0, tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Prosjektkalkulator", "Timepriskalkulator", "Lagrede prosjekter", "Forklaringer"])

with st.sidebar:
    st.header("Standardforutsetninger")
    skatt_rate = st.slider("Estimert skatt / avsetning (%)", 0.0, 60.0, DEFAULTS["skatt_rate"], 1.0)
    mva_rate = st.slider("MVA-sats (%)", 0.0, 25.0, DEFAULTS["mva_rate"], 1.0)
    mva_pliktig = st.toggle("MVA-pliktig prosjekt", value=True)

    st.markdown("### Årlige faste kostnader")
    st.button("+ Legg til årlig kostnad", on_click=add_annual_cost, use_container_width=True)
    if not st.session_state.annual_costs:
        st.caption("Ingen faste kostnader lagt inn ennå.")

    updated_annual_costs = []
    for item in st.session_state.annual_costs:
        a1, a2, a3 = st.columns([1.5, 1, 0.25])
        name = a1.text_input("Navn", value=item["name"], key=f"annual_name_{item['id']}", label_visibility="collapsed")
        amount = a2.number_input("Beløp", min_value=0.0, value=float(item["amount"]), step=100.0, key=f"annual_amount_{item['id']}", label_visibility="collapsed")
        if a3.button("−", key=f"remove_annual_{item['id']}"):
            remove_annual_cost(item["id"])
            st.rerun()
        updated_annual_costs.append({"id": item["id"], "name": name, "amount": amount})
    st.session_state.annual_costs = updated_annual_costs
    save_annual_costs(st.session_state.annual_costs)
    totale_aarlige_kostnader = total_from_items(st.session_state.annual_costs)
    st.write(f"Totale årlige faste kostnader: **{nok(totale_aarlige_kostnader)}**")

with tab0:
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)

    if not st.session_state.saved_projects:
        st.info("Ingen lagrede prosjekter ennå. Lagre et prosjekt for å få en samlet oversikt her.")
    else:
        total_inntekt = sum(float(p["result"]["prosjektpris_eks_mva"]) for p in st.session_state.saved_projects)
        total_mva = sum(float(p["result"]["mva_belop"]) for p in st.session_state.saved_projects)
        total_kostnader = sum(float(p["result"]["totale_kostnader"]) for p in st.session_state.saved_projects)
        total_skatt = sum(float(p["result"]["estimert_skatt"]) for p in st.session_state.saved_projects)
        total_privatuttak = sum(float(p["result"]["netto_etter_skatt"]) for p in st.session_state.saved_projects)
        total_avsetning = sum(float(p["result"]["anbefalt_avsetning"]) for p in st.session_state.saved_projects)
        antall_prosjekter = len(st.session_state.saved_projects)

        st.write("Her ser du kun totalsummen av alle lagrede prosjekter.")

        top1, top2, top3 = st.columns(3)
        with top1:
            metric_card("Antall lagrede prosjekter", str(antall_prosjekter), "Alle prosjekter som er lagret i appen")
        with top2:
            metric_card("Total inntekt eks. mva", nok(total_inntekt), "Summen av prosjektpris eks. mva")
        with top3:
            metric_card("Mulig privatuttak totalt", nok(total_privatuttak), "Det du i praksis kan ta ut privat")

        bottom1, bottom2, bottom3 = st.columns(3)
        with bottom1:
            metric_card("Totale kostnader", nok(total_kostnader), "Årlige + prosjektspesifikke kostnader")
        with bottom2:
            metric_card("Total skatt", nok(total_skatt), "Estimert skatt på samlet overskudd")
        with bottom3:
            metric_card("Total MVA å sette av", nok(total_mva), "MVA som skal viderebetales")

        card_start(
            "Samlet oppsummering",
            "En enkel totaloversikt over økonomien på tvers av alle lagrede prosjekter.",
        )
        s1, s2 = st.columns(2)
        with s1:
            st.metric("Total anbefalt avsetning", nok(total_avsetning))
        with s2:
            st.metric("Gjennomsnittlig mulig privatuttak per prosjekt", nok(total_privatuttak / antall_prosjekter if antall_prosjekter > 0 else 0.0))
        card_end()

with tab1:
    st.markdown('<div class="section-title">Prosjektkalkulator</div>', unsafe_allow_html=True)
    st.write("Legg inn valgfri prosjektpris og eventuelle prosjektspesifikke kostnader.")

    p1, p2, p3 = st.columns([1, 1, 1])
    if p1.button("Sett 30 000 kr"):
        st.session_state["prosjektpris"] = 30000.0
    if p2.button("Sett 50 000 kr"):
        st.session_state["prosjektpris"] = 50000.0
    if p3.button("Nullstill"):
        st.session_state["prosjektpris"] = 0.0
        st.session_state.project_expenses = [{"id": 1, "name": "Prosjektkostnad 1", "amount": 0.0}]

    prosjektpris = st.number_input("Prosjektpris eks. mva", min_value=0.0, step=1000.0, key="prosjektpris")

    st.markdown("### Prosjektspesifikke kostnader")
    st.button("+ Legg til prosjektutgift", on_click=add_project_expense)
    updated_project_expenses = []
    for item in st.session_state.project_expenses:
        p1, p2, p3 = st.columns([1.5, 1, 0.25])
        name = p1.text_input("Navn prosjektutgift", value=item["name"], key=f"project_name_{item['id']}", label_visibility="collapsed")
        amount = p2.number_input("Beløp prosjektutgift", min_value=0.0, value=float(item["amount"]), step=100.0, key=f"project_amount_{item['id']}", label_visibility="collapsed")
        if p3.button("−", key=f"remove_project_{item['id']}"):
            remove_project_expense(item["id"])
            st.rerun()
        updated_project_expenses.append({"id": item["id"], "name": name, "amount": amount})
    st.session_state.project_expenses = updated_project_expenses
    prosjektspesifikke_kostnader = total_from_items(st.session_state.project_expenses)
    st.caption(f"Sum prosjektutgifter: {nok(prosjektspesifikke_kostnader)}")

    resultat = beregn_prosjekt(
        prosjektpris_eks_mva=prosjektpris,
        aarlige_kostnader=totale_aarlige_kostnader,
        prosjektspesifikke_kostnader=prosjektspesifikke_kostnader,
        skatt_rate=skatt_rate,
        mva_rate=mva_rate,
        mva_pliktig=mva_pliktig,
    )

    vis_resultater(resultat, "Resultat for prosjekt")

    save_name = st.text_input("Navn på prosjekt", value="Fastprisprosjekt")
    if st.button("Lagre prosjekt"):
        save_project(
            name=save_name,
            mode="Prosjektkalkulator",
            result=resultat,
            extra={
                "prosjektpris": prosjektpris,
                "annual_costs": st.session_state.annual_costs,
                "project_expenses": st.session_state.project_expenses,
            },
        )
        st.success("Prosjekt lagret.")

with tab2:
    st.markdown('<div class="section-title">Timepriskalkulator</div>', unsafe_allow_html=True)
    st.write("Sett timepris og antall timer for å se hva prosjektet faktisk gir deg.")

    t1, t2 = st.columns(2)
    timepris = t1.number_input("Timepris eks. mva", min_value=0.0, value=1200.0, step=100.0)
    antall_timer = t2.number_input("Antall timer", min_value=0.0, value=40.0, step=1.0)
    prosjektspesifikke_kostnader_time = st.number_input(
        "Totale prosjektkostnader for dette timeprosjektet",
        min_value=0.0,
        value=0.0,
        step=100.0,
    )

    resultat_time = beregn_timepris(
        timepris_eks_mva=timepris,
        antall_timer=antall_timer,
        aarlige_kostnader=totale_aarlige_kostnader,
        prosjektspesifikke_kostnader=prosjektspesifikke_kostnader_time,
        skatt_rate=skatt_rate,
        mva_rate=mva_rate,
        mva_pliktig=mva_pliktig,
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Omsetning eks. mva", nok(timepris * antall_timer))
    c2.metric("Mulig privatuttak per time", nok((resultat_time["netto_etter_skatt"] / antall_timer) if antall_timer > 0 else 0.0))
    c3.metric("Anbefalt avsetning", nok(resultat_time["anbefalt_avsetning"]))

    vis_resultater(resultat_time, "Resultat for timebasert prosjekt")

    save_name_time = st.text_input("Navn på timeprosjekt", value="Timebasert prosjekt")
    if st.button("Lagre timeprosjekt"):
        save_project(
            name=save_name_time,
            mode="Timepriskalkulator",
            result=resultat_time,
            extra={
                "timepris": timepris,
                "antall_timer": antall_timer,
                "prosjektkostnader": prosjektspesifikke_kostnader_time,
                "annual_costs": st.session_state.annual_costs,
            },
        )
        st.success("Timeprosjekt lagret.")

with tab3:
    st.markdown('<div class="section-title">Lagrede prosjekter</div>', unsafe_allow_html=True)

    if not st.session_state.saved_projects:
        st.info("Ingen prosjekter lagret ennå.")
    else:
        st.caption("Prosjektene vises som en enkel liste. Trykk Endre for å oppdatere navn/type, eller Slett for å fjerne prosjektet.")

        for i, project in enumerate(st.session_state.saved_projects):
            with st.container(border=True):
                st.markdown(f"**{i+1}. {project['name']}**")
                st.caption(f"{project['mode']} • Lagret: {project['saved_at']}")

                a1, a2, a3 = st.columns(3)
                a1.metric("Inntekt eks. mva", nok(project["result"]["prosjektpris_eks_mva"]))
                a2.metric("Sett av til skatt + MVA", nok(project["result"]["anbefalt_avsetning"]))
                a3.metric("Mulig privatuttak", nok(project["result"]["netto_etter_skatt"]))

                b1, b2 = st.columns([1, 1])
                if b1.button("Endre", key=f"edit_project_{i}", use_container_width=True):
                    st.session_state.editing_saved_project_index = i
                if b2.button("Slett", key=f"delete_project_{i}", use_container_width=True):
                    delete_saved_project(i)
                    if st.session_state.editing_saved_project_index == i:
                        st.session_state.editing_saved_project_index = None
                    st.success("Prosjekt slettet.")
                    st.rerun()

                if st.session_state.editing_saved_project_index == i:
                    st.markdown("### Rediger prosjekt")
                    edited_name = st.text_input("Prosjektnavn", value=project["name"], key=f"edit_name_{i}")
                    edited_mode = st.selectbox(
                        "Type",
                        options=["Prosjektkalkulator", "Timepriskalkulator"],
                        index=0 if project["mode"] == "Prosjektkalkulator" else 1,
                        key=f"edit_mode_{i}",
                    )

                    c1, c2 = st.columns(2)
                    if c1.button("Lagre endringer", key=f"update_project_{i}", use_container_width=True):
                        updated = dict(project)
                        updated["name"] = edited_name
                        updated["mode"] = edited_mode
                        updated["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.session_state.saved_projects[i] = updated
                        st.session_state.editing_saved_project_index = None
                        st.success("Prosjekt oppdatert.")
                        st.rerun()
                    if c2.button("Avbryt", key=f"cancel_update_project_{i}", use_container_width=True):
                        st.session_state.editing_saved_project_index = None
                        st.rerun()

        export_payload = json.dumps(st.session_state.saved_projects, ensure_ascii=False, indent=2)
        st.download_button(
            "Last ned lagrede prosjekter som JSON",
            data=export_payload,
            file_name="lagrede_prosjekter.json",
            mime="application/json",
        )

        uploaded_json = st.file_uploader("Last inn lagrede prosjekter fra JSON", type=["json"])
        if uploaded_json is not None:
            try:
                loaded = json.load(uploaded_json)
                if isinstance(loaded, list):
                    st.session_state.saved_projects = loaded
                    st.success("Prosjekter lastet inn.")
                    st.rerun()
                else:
                    st.error("JSON-filen må inneholde en liste med prosjekter.")
            except Exception as exc:
                st.error(f"Kunne ikke lese JSON-fil: {exc}")

with tab4:
    st.markdown('<div class="section-title">Forklaringer</div>', unsafe_allow_html=True)
    st.markdown(
        """
### Dette betyr tallene
- **Prosjektpris eks. mva**: det du faktisk tar betalt for jobben din.
- **Faktura inkl. mva**: beløpet kunden betaler hvis du er MVA-pliktig.
- **MVA å sette av**: dette er ikke dine penger, men skal betales videre.
- **Totale kostnader**: årlige faste kostnader + prosjektspesifikke kostnader.
- **Resultat før skatt**: overskudd før estimert skatt.
- **Estimert skatt**: enkel avsetning basert på prosentsatsen du velger.
- **Mulig privatuttak etter skatt**: omtrent hva du sitter igjen med og kan ta ut privat.

### Viktig å huske i ENK
- Du tar ikke ut vanlig lønn fra et ENK.
- Pengene du tar ut kalles **privatuttak**.
- Skatten avhenger av total inntekt, fradrag og personlige forhold.
- Denne appen er derfor en **praktisk kalkulator**, ikke en full skatteberegning.

### Typiske ting å sette av penger til
- MVA
- Forskuddsskatt
- Fiken / regnskap
- Programvare og abonnementer
- Reise, utstyr eller andre prosjektkostnader
        """
    )
