import re
import urllib.parse
from contextlib import contextmanager

import streamlit as st
import pandas as pd

# =========================================================
# Västrabo – Sök bostad i Västra Götaland
# =========================================================

st.set_page_config(page_title="Söka bostad i Västra Götland", page_icon="🏠", layout="centered")

# Dölj toppraden (Share/GitHub/meny)
st.markdown(
    """
    <style>
    header { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    div[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .block-container { padding-top: 2rem !important; }

    .app-title { font-size: 56px !important; color: #1E3A8A; font-weight: 900; text-align: center; margin: 0; padding: 0; }
    .app-subtitle { font-size: 18px !important; color: #4B5563; text-align: center; margin-bottom: 18px; }
    .divider-line { border-bottom: 2px solid #eee; margin: 0 0 18px 0; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-title">Söka bostad i Västra Götland</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Enheten för Mottagande och Integration</div>', unsafe_allow_html=True)
st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# ----------------------------
# Robust hjälpfunktioner
# ----------------------------
def link_btn(label: str, url: str) -> None:
    """Robust länkknapp: använder st.link_button om möjligt, annars markdown-länk."""
    try:
        st.link_button(label, url, use_container_width=True)
    except Exception:
        st.markdown(f"👉 [{label}]({url})")

def map_safe(df: pd.DataFrame, zoom: int = 9) -> None:
    """Robust karta: zoom om det stöds av din Streamlit-version."""
    try:
        st.map(df, zoom=zoom)
    except TypeError:
        st.map(df)

def google_hyresvardar_url(kommun: str) -> str:
    q = urllib.parse.quote_plus(f"privata hyresvärdar {kommun} bostad")
    return f"https://www.google.com/search?q={q}"

VOWELS = set("aeiouyåäö")

def slugify_sv(text: str) -> str:
    s = text.strip().lower()
    s = (
        s.replace("å", "a")
         .replace("ä", "a")
         .replace("ö", "o")
         .replace("é", "e")
    )
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def genitive_s_if_needed(kommun: str) -> str:
    k = kommun.strip()
    if not k:
        return ""
    last = k[-1].lower()
    if last in VOWELS or last == "s":
        return ""
    return "s"

def official_kommun_name(kommun: str) -> str:
    return f"{kommun}{genitive_s_if_needed(kommun)} kommun"

def homeq_kommun_url(kommun: str) -> str:
    slug = slugify_sv(kommun) + genitive_s_if_needed(kommun)
    return f"https://www.homeq.se/lediga-lagenheter/{slug}-kommun"

def qasa_kommun_url(kommun: str) -> str:
    area = f"{kommun}{genitive_s_if_needed(kommun)}_kommun~~se"
    return "https://qasa.com/se/sv/find-home?searchAreas=" + urllib.parse.quote(area)

def google_maps_station_url(kommun: str) -> str:
    dest = urllib.parse.quote_plus(f"{kommun} Station")
    return f"https://www.google.com/maps/dir/?api=1&destination={dest}"

@contextmanager
def card():
    """Container med border om Streamlit-versionen stödjer det."""
    try:
        with st.container(border=True):
            yield
    except TypeError:
        with st.container():
            yield

# ----------------------------
# Konstanter
# ----------------------------
BOPLATS_FILTER_URL = "https://boplats.se/filtrera?listtype=imagelist&types=1hand"
BOPLATS_KOMMUNER = {
    "Göteborg","Ale","Alingsås","Borås","Herrljunga","Härryda","Kungälv",
    "Lerum","Mölndal","Partille","Skara","Stenungsund","Strömstad","Trollhättan","Uddevalla","Öckerö"
}

QASA_INFO_TEXT = (
    "Qasa är en seriös tjänst.\n\n"
    "Använd gärna Qasa, men följ alltid säkerhetsråden:\n\n"
    "• Betala inte pengar innan du har sett bostaden och fått tydligt avtal.\n"
    "• Håll kommunikationen i plattformen när det går.\n"
    "• Var försiktig om någon vill flytta kontakten till WhatsApp/privat direkt."
)

# ----------------------------
# Data: alla 49 kommuner
# ----------------------------
kommuner = {'Ale': {'dist': '25 km',
         'hyresvardar': [('Alebyggen', 'https://www.alebyggen.se', 'Kommunal')],
         'lat': 57.92,
         'lon': 12.08,
         'time': 'ca 20 min (pendeltåg)'},
 'Alingsås': {'dist': '45 km',
              'hyresvardar': [('Alingsåshem', 'https://www.alingsashem.se', 'Kommunal'),
                              ('Fabs', 'https://www.fabs.se', 'Privat')],
              'lat': 57.93,
              'lon': 12.53,
              'time': 'ca 25 min (pendeltåg)'},
 'Bengtsfors': {'dist': '175 km',
                'hyresvardar': [('Bengtsforsbostäder', 'https://www.bengtsforsbostader.se', 'Kommunal')],
                'lat': 59.03,
                'lon': 12.22},
 'Bollebygd': {'dist': '40 km',
               'hyresvardar': [('Bollebygds Hyresbostäder', 'https://www.bollebygdsbostader.se', 'Kommunal')],
               'lat': 57.66,
               'lon': 12.57},
 'Borås': {'dist': '65 km',
           'hyresvardar': [('AB Bostäder i Borås', 'https://www.bostader.boras.se', 'Kommunal'),
                           ('Willhem', 'https://www.willhem.se', 'Privat')],
           'lat': 57.72,
           'lon': 12.94,
           'time': 'ca 55–70 min (buss/tåg)'},
 'Dals-Ed': {'dist': '165 km',
             'hyresvardar': [('Edshus', 'https://www.edshus.se', 'Kommunal')],
             'lat': 58.91,
             'lon': 11.92},
 'Essunga': {'dist': '85 km',
             'hyresvardar': [('Essungabostäder', 'https://www.essungabostader.se', 'Kommunal')],
             'lat': 58.17,
             'lon': 12.71},
 'Falköping': {'dist': '115 km',
               'hyresvardar': [('Falköpings Hyresbostäder',
                                'https://www.falkopingshyresbostader.se',
                                'Kommunal')],
               'lat': 58.17,
               'lon': 13.55},
 'Färgelanda': {'dist': '110 km',
                'hyresvardar': [('Valbohem', 'https://www.valbohem.se', 'Kommunal')],
                'lat': 58.57,
                'lon': 11.99},
 'Grästorp': {'dist': '100 km',
              'hyresvardar': [('Grästorps Bostäder', 'https://www.grastorpsbostader.se', 'Kommunal')],
              'lat': 58.33,
              'lon': 12.68},
 'Gullspång': {'dist': '210 km',
               'hyresvardar': [('Gullspångsbostäder', 'https://www.gullspangsbostader.se', 'Kommunal')],
               'lat': 58.98,
               'lon': 14.12},
 'Götene': {'dist': '150 km',
            'hyresvardar': [('GöteneBostäder', 'https://www.gotenebostader.se', 'Kommunal')],
            'lat': 58.52,
            'lon': 13.49},
 'Göteborg': {'dist': '0 km',
              'hyresvardar': [('Bostadsbolaget', 'https://bostadsbolaget.se', 'Kommunal'),
                              ('Poseidon', 'https://poseidon.goteborg.se', 'Kommunal'),
                              ('Familjebostäder', 'https://familjebostader.se', 'Kommunal'),
                              ('Wallenstam', 'https://www.wallenstam.se', 'Privat')],
              'lat': 57.7,
              'lon': 11.97,
              'time': '0 min'},
 'Herrljunga': {'dist': '85 km',
                'hyresvardar': [('Herrljungabostäder', 'https://www.herrljungabostader.se', 'Kommunal')],
                'lat': 58.07,
                'lon': 13.02,
                'time': 'ca 50 min (tåg)'},
 'Hjo': {'dist': '160 km',
         'hyresvardar': [('Guldkroksbostäder', 'https://www.hjo.se/guldkroksbostader', 'Kommunal')],
         'lat': 58.3,
         'lon': 14.28},
 'Härryda': {'dist': '20 km',
             'hyresvardar': [('Förbo (info)', 'https://xn--frbo-5qa.se/', 'Kommunal'),
                             ('Förbo – Lediga bostäder (Mina sidor)',
                              'https://minasidor.foerbo.se/market/residential',
                              'Kommunal')],
             'lat': 57.66,
             'lon': 12.12,
             'time': 'ca 20–40 min'},
 'Karlsborg': {'dist': '200 km',
               'hyresvardar': [('Karlsborgsbostäder', 'https://www.karlsborgsbostader.se', 'Kommunal')],
               'lat': 58.53,
               'lon': 14.5},
 'Kungälv': {'dist': '20 km',
             'hyresvardar': [('Kungälvsbostäder', 'https://www.kungalvsbostader.se', 'Kommunal'),
                             ('Förbo – Lediga bostäder (Mina sidor)',
                              'https://minasidor.foerbo.se/market/residential',
                              'Kommunal')],
             'lat': 57.87,
             'lon': 11.98,
             'time': 'ca 25 min (buss)'},
 'Lerum': {'dist': '20 km',
           'hyresvardar': [('Förbo (info)', 'https://xn--frbo-5qa.se/', 'Kommunal'),
                           ('Förbo – Lediga bostäder (Mina sidor)',
                            'https://minasidor.foerbo.se/market/residential',
                            'Kommunal')],
           'lat': 57.77,
           'lon': 12.27,
           'time': 'ca 20 min (pendeltåg)'},
 'Lidköping': {'dist': '130 km',
               'hyresvardar': [('AB Bostäder i Lidköping', 'https://www.bostaderlidkoping.se', 'Kommunal')],
               'lat': 58.5,
               'lon': 13.15},
 'Lilla Edet': {'dist': '55 km',
                'hyresvardar': [('Lilla Edet Bostads AB', 'https://www.lebo.se', 'Kommunal')],
                'lat': 58.13,
                'lon': 12.12},
 'Lysekil': {'dist': '110 km',
             'hyresvardar': [('LysekilsBostäder', 'https://www.lysekilsbostader.se', 'Kommunal')],
             'lat': 58.27,
             'lon': 11.43},
 'Mariestad': {'dist': '175 km',
               'hyresvardar': [('Mariehus', 'https://www.mariehus.se', 'Kommunal')],
               'lat': 58.7,
               'lon': 13.82},
 'Mark': {'dist': '60 km',
          'hyresvardar': [('Marks Bostads AB', 'https://www.marksbostadsab.se', 'Kommunal')],
          'lat': 57.51,
          'lon': 12.69},
 'Mellerud': {'dist': '125 km',
              'hyresvardar': [('Melleruds Bostäder', 'https://www.mellerudsbostader.se', 'Kommunal')],
              'lat': 58.7,
              'lon': 12.45},
 'Munkedal': {'dist': '110 km',
              'hyresvardar': [('Munkedals Bostäder', 'https://www.munkedalsbostader.se', 'Kommunal')],
              'lat': 58.47,
              'lon': 11.68},
 'Mölndal': {'dist': '10 km',
             'hyresvardar': [('Mölndalsbostäder', 'https://www.molndalsbostader.se', 'Kommunal'),
                             ('Wallenstam', 'https://www.wallenstam.se', 'Privat')],
             'lat': 57.65,
             'lon': 12.01,
             'time': 'ca 10–20 min'},
 'Orust': {'dist': '80 km',
           'hyresvardar': [('Orustbostäder', 'https://www.orustbostader.se', 'Kommunal')],
           'lat': 58.21,
           'lon': 11.7},
 'Partille': {'dist': '10 km',
              'hyresvardar': [('Partillebo', 'https://www.partillebo.se', 'Kommunal')],
              'lat': 57.74,
              'lon': 12.1,
              'time': 'ca 15–25 min'},
 'Skara': {'dist': '130 km',
           'hyresvardar': [('Centrumbostäder', 'https://www.centrumbostader.se', 'Kommunal'),
                           ('Cantab', 'https://cantab.nu', 'Privat'),
                           ('Filip Söderqvist', 'https://filipsoderqvist.se', 'Privat')],
           'lat': 58.38,
           'lon': 13.43},
 'Skövde': {'dist': '150 km',
            'hyresvardar': [('Skövdebostäder', 'https://www.skovdebostader.se', 'Kommunal')],
            'lat': 58.39,
            'lon': 13.85},
 'Sotenäs': {'dist': '130 km',
             'hyresvardar': [('Sotenäsbostäder', 'https://www.sotenasbostader.se', 'Kommunal')],
             'lat': 58.35,
             'lon': 11.28},
 'Stenungsund': {'dist': '50 km',
                 'hyresvardar': [('Stenungsundshem', 'https://www.stenungsundshem.se', 'Kommunal')],
                 'lat': 58.07,
                 'lon': 11.81,
                 'time': 'ca 40 min (tåg/buss)'},
 'Strömstad': {'dist': '165 km',
               'hyresvardar': [('Strömstadsbyggen', 'https://www.stromstadsbyggen.se', 'Kommunal')],
               'lat': 58.93,
               'lon': 11.17},
 'Svenljunga': {'dist': '95 km',
                'hyresvardar': [('Svenljunga Bostäder', 'https://www.svenljungabostader.se', 'Kommunal')],
                'lat': 57.49,
                'lon': 13.11},
 'Tanum': {'dist': '140 km',
           'hyresvardar': [('Tanums Bostäder', 'https://www.tanumsbostader.se', 'Kommunal')],
           'lat': 58.72,
           'lon': 11.32},
 'Tibro': {'dist': '170 km',
           'hyresvardar': [('Tibrobyggen', 'https://www.tibrobyggen.se', 'Kommunal')],
           'lat': 58.41,
           'lon': 14.16},
 'Tidaholm': {'dist': '160 km',
              'hyresvardar': [('Tidaholms Bostads AB', 'https://www.tidaholmsbostadsab.se', 'Kommunal')],
              'lat': 58.18,
              'lon': 13.95},
 'Tjörn': {'dist': '65 km',
           'hyresvardar': [('Tjörns Bostads AB', 'https://www.tjornsbostad.se', 'Kommunal')],
           'lat': 58.0,
           'lon': 11.63},
 'Tranemo': {'dist': '100 km',
             'hyresvardar': [('Tranemobostäder', 'https://www.tranemobostader.se', 'Kommunal')],
             'lat': 57.48,
             'lon': 13.35},
 'Trollhättan': {'dist': '75 km',
                 'hyresvardar': [('Eidar', 'https://www.eidar.se', 'Kommunal')],
                 'lat': 58.28,
                 'lon': 12.28,
                 'time': 'ca 40 min (tåg)'},
 'Töreboda': {'dist': '185 km',
              'hyresvardar': [('Törebodabostäder', 'https://www.torebodabostader.se', 'Kommunal')],
              'lat': 58.7,
              'lon': 14.12},
 'Uddevalla': {'dist': '90 km',
               'hyresvardar': [('Uddevallahem', 'https://www.uddevallahem.se', 'Kommunal')],
               'lat': 58.35,
               'lon': 11.93,
               'time': 'ca 55 min (tåg)'},
 'Ulricehamn': {'dist': '100 km',
                'hyresvardar': [('Stubo', 'https://www.stubo.se', 'Kommunal')],
                'lat': 57.79,
                'lon': 13.41},
 'Vara': {'dist': '100 km',
          'hyresvardar': [('Vara Bostäder', 'https://www.varabostader.se', 'Kommunal')],
          'lat': 58.26,
          'lon': 12.95},
 'Vårgårda': {'dist': '65 km',
              'hyresvardar': [('Vårgårda Bostäder', 'https://www.vargardabostader.se', 'Kommunal')],
              'lat': 58.03,
              'lon': 12.8},
 'Vänersborg': {'dist': '85 km',
                'hyresvardar': [('Vänersborgsbostäder', 'https://www.vanersborgsbostader.se', 'Kommunal')],
                'lat': 58.37,
                'lon': 12.32,
                'time': 'ca 50 min (tåg)'},
 'Åmål': {'dist': '175 km',
          'hyresvardar': [('Åmåls Kommunfastigheter', 'https://www.amalskommunfastigheter.se', 'Kommunal')],
          'lat': 59.05,
          'lon': 12.7},
 'Öckerö': {'dist': '25 km',
            'hyresvardar': [('Öckerö Bostads AB', 'https://www.ockerobostad.se', 'Kommunal')],
            'lat': 57.71,
            'lon': 11.64,
            'time': 'ca 50 min (buss + färja)'}}

# ----------------------------
# “Så gör du” + “Vad du behöver”
# ----------------------------
with card():
    st.subheader("✅ Så gör du")
    st.markdown(
        "1. Välj en kommun i listan.\n"
        "2. Klicka på länkarna (hyresvärdar + portaler).\n"
        "3. Registrera konto (om det behövs) och gör intresseanmälan.\n"
        "4. Följ upp regelbundet – många bostäder ligger ute kort tid."
    )

    st.subheader("📄 Vad du behöver (oftast)")
    st.markdown(
        "• E-post och mobilnummer\n"
        "• BankID (om du har)\n"
        "• Personnummer/samordningsnummer (om du har)\n"
        "• Inkomstuppgifter (lön, etablering, bidrag)\n"
        "• Referenser och dokument (om hyresvärden ber om det)"
    )

st.divider()

# ----------------------------
# Välj kommun + Rensa
# ----------------------------
if "city_selector" not in st.session_state:
    st.session_state["city_selector"] = ""

def reset_city():
    st.session_state["city_selector"] = ""
    st.rerun()

col_sel, col_btn = st.columns([4, 1], vertical_alignment="bottom")

with col_sel:
    options = [""] + sorted(list(kommuner.keys()))
    selected_city = st.selectbox(
        "Välj kommun:",
        options,
        key="city_selector",
        format_func=lambda x: "— Välj kommun —" if x == "" else x
    )

with col_btn:
    st.button("Rensa 🔄", on_click=reset_city, use_container_width=True)

# ----------------------------
# Resultat
# ----------------------------
if selected_city:
    d = kommuner[selected_city]
    kommun_namn = official_kommun_name(selected_city)

    # Hyresvärdar
    with card():
        st.subheader(f"🏢 {selected_city} – Hyresvärdar")

        hyres = d.get("hyresvardar", []) or []
        kommunala = [(n, u) for (n, u, cat) in hyres if cat == "Kommunal"]
        privata = [(n, u) for (n, u, cat) in hyres if cat == "Privat"]

        if kommunala:
            st.markdown("**Kommunala:**")
            for name, url in kommunala:
                st.markdown(f"• **[{name}]({url})**")

        if privata:
            st.markdown("**Privata (exempel):**")
            for name, url in privata:
                st.markdown(f"• **[{name}]({url})**")

        # Google-knapp som täcker luckor om privata saknas
        if not privata:
            st.info("Tips: Om listan inte är komplett ännu kan du söka fler privata hyresvärdar via Google.")
            link_btn("Sök privata hyresvärdar på Google ↗️", google_hyresvardar_url(selected_city))

    # Sökportaler
    with card():
        st.subheader("🔎 Sök lediga annonser")

        c1, c2, c3 = st.columns(3)
        with c1:
            link_btn("HomeQ (kommun) ↗️", homeq_kommun_url(selected_city))

        with c2:
            if selected_city in BOPLATS_KOMMUNER:
                link_btn("Boplats (välj kommun i filter) ↗️", BOPLATS_FILTER_URL)
            else:
                st.caption("Boplats: ej i deras kommun-lista")

        with c3:
            link_btn("Qasa (kommun) ↗️", qasa_kommun_url(selected_city))

        st.caption(f"Sökningarna ovan är satta på **{kommun_namn}** (HomeQ/Qasa).")

        with st.expander("Qasa – säkerhetsråd"):
            st.write(QASA_INFO_TEXT)

    # Karta & läge
    with card():
        st.subheader("📍 Karta & läge")
        st.write(f"Avstånd till Göteborg C: **{d.get('dist', '—')}**")
        if d.get("time"):
            st.write(f"Restid (ungefär): **{d['time']}**")

        map_df = pd.DataFrame({"lat": [d["lat"]], "lon": [d["lon"]]})
        map_safe(map_df, zoom=9)

        link_btn("Visa vägbeskrivning på Google Maps 🗺️", google_maps_station_url(selected_city))

else:
    st.info("Välj en kommun för att se hyresvärdar, portal-länkar och karta.")

st.divider()
st.caption("© 2026 Västrabo | Enheten för mottagande och integration i Lerums kommun")



