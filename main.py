import re
import urllib.parse
import streamlit as st
import pandas as pd

# ----------------------------
# 1) Sidinställningar
# ----------------------------
st.set_page_config(
    page_title="Söka bostad i Västra Götaland",
    page_icon="🏠",
    layout="centered"
)

# ----------------------------
# 1A) DÖLJ TOPPRADEN (Share/GitHub/meny)
# ----------------------------
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
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# 1B) Design
# ----------------------------
st.markdown(
    """
    <style>
    .app-title { font-size: 70px !important; color: #1E3A8A; font-weight: 900; text-align: center; margin: 0; padding: 0; }
    .app-subtitle { font-size: 20px !important; color: #4B5563; text-align: center; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 15px; }
    .card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .section-header { color: #1E3A8A; font-size: 24px; font-weight: bold; margin-bottom: 15px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="app-title">Söka bostad i Västra Götaland</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Enheten för mottagande och integration i Lerums kommun</p>',
    unsafe_allow_html=True
)

# ----------------------------
# 2) Hjälpfunktioner
# ----------------------------
def link_btn(label: str, url: str) -> None:
    """Robust länkknapp: använder st.link_button om möjligt, annars markdown."""
    try:
        st.link_button(label, url)
    except Exception:
        st.markdown(f"👉 [{label}]({url})")

def map_safe(df: pd.DataFrame, zoom: int = 9) -> None:
    try:
        st.map(df, zoom=zoom)
    except TypeError:
        st.map(df)

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

# ----------------------------
# 3) Konstanter
# ----------------------------
BOPLATS_FILTER_URL = "https://boplats.se/filtrera?listtype=imagelist&types=1hand"
BOPLATS_KOMMUNER = {
    "Göteborg","Ale","Alingsås","Borås","Herrljunga","Härryda","Kungsbacka","Kungälv",
    "Lerum","Mölndal","Partille","Skara","Stenungsund","Strömstad","Trollhättan","Uddevalla","Öckerö"
}

# Förbo – stabila länkar
FOERBO_INFO_URL = "https://www.foerbo.se/"
FOERBO_LEDIG_URL = "https://minasidor.foerbo.se/market/residential"

# Qasa-text (som du bad om)
QASA_INFO_TEXT = [
    "Qasa är en seriös tjänst.",
    "Använd gärna Qasa, men följ alltid säkerhetsråden:",
    "• Betala inte pengar innan du har sett bostaden och fått tydligt avtal.",
    "• Håll kommunikationen i plattformen när det går.",
    "• Var försiktig om någon vill flytta kontakten till WhatsApp/privat direkt."
]

# ----------------------------
# 4) Kommun-databas
#    NYTT: hyresvardar = lista av (namn, url)
#    Kommuner utan hyresvardar-lista fungerar ändå via bolag/web.
# ----------------------------
kommuner = {
    "Göteborg": {
        "bolag": "Bostadsbolaget",
        "web": "https://bostadsbolaget.se",
        "hyresvardar": [
            ("Bostadsbolaget", "https://bostadsbolaget.se/"),
            ("Poseidon", "https://poseidon.goteborg.se/"),
            ("Familjebostäder", "https://familjebostader.se/"),
        ],
        "lat": 57.70, "lon": 11.97, "dist": "0 km"
    },
    "Mölndal": {
        "bolag": "Mölndalsbostäder",
        "web": "https://www.molndalsbostader.se",
        "hyresvardar": [
            ("Mölndalsbostäder", "https://www.molndalsbostader.se/"),
            ("Wallenstam", "https://www.wallenstam.se/"),
        ],
        "lat": 57.65, "lon": 12.01, "dist": "10 km"
    },
    "Partille": {
        "bolag": "Partillebo",
        "web": "https://www.partillebo.se",
        "hyresvardar": [
            ("Partillebo", "https://www.partillebo.se/"),
        ],
        "lat": 57.74, "lon": 12.10, "dist": "10 km"
    },
    "Lerum": {
        "bolag": "Förbo",
        "web": FOERBO_INFO_URL,
        "hyresvardar": [
            ("Förbo (info)", FOERBO_INFO_URL),
            ("Förbo – Lediga bostäder (Mina sidor)", FOERBO_LEDIG_URL),
        ],
        "lat": 57.77, "lon": 12.27, "dist": "20 km"
    },
    "Härryda": {
        "bolag": "Förbo",
        "web": FOERBO_INFO_URL,
        "hyresvardar": [
            ("Förbo (info)", FOERBO_INFO_URL),
            ("Förbo – Lediga bostäder (Mina sidor)", FOERBO_LEDIG_URL),
        ],
        "lat": 57.66, "lon": 12.12, "dist": "20 km"
    },
    "Kungälv": {
        "bolag": "Kungälvsbostäder",
        "web": "https://www.kungalvsbostader.se",
        "hyresvardar": [
            ("Kungälvsbostäder", "https://www.kungalvsbostader.se/"),
            ("Förbo – Lediga bostäder (Mina sidor)", FOERBO_LEDIG_URL),
        ],
        "lat": 57.87, "lon": 11.98, "dist": "20 km"
    },
    "Borås": {
        "bolag": "Bostäder i Borås",
        "web": "https://www.bostaderiboras.se/",
        "hyresvardar": [
            ("Bostäder i Borås", "https://www.bostaderiboras.se/"),
            ("Willhem", "https://www.willhem.se/"),
        ],
        "lat": 57.72, "lon": 12.94, "dist": "65 km"
    },

    # --- resten av dina kommuner (minst en hyresvärd) ---
    "Ale": {"bolag": "Alebyggen", "web": "https://www.alebyggen.se", "hyresvardar": [("Alebyggen", "https://www.alebyggen.se/")], "lat": 57.92, "lon": 12.08, "dist": "25 km"},
    "Alingsås": {"bolag": "Alingsåshem", "web": "https://www.alingsashem.se", "hyresvardar": [("Alingsåshem", "https://www.alingsashem.se/")], "lat": 57.93, "lon": 12.53, "dist": "45 km"},
    "Bengtsfors": {"bolag": "Bengtsforshus", "web": "https://bengtsforshus.se/", "hyresvardar": [("Bengtsforshus", "https://bengtsforshus.se/")], "lat": 59.03, "lon": 12.22, "dist": "175 km"},
    "Bollebygd": {"bolag": "Bollebo", "web": "https://www.bollebo.se/", "hyresvardar": [("Bollebo", "https://www.bollebo.se/")], "lat": 57.66, "lon": 12.57, "dist": "40 km"},
    "Dals-Ed": {"bolag": "Edshus", "web": "https://www.edshus.se", "hyresvardar": [("Edshus", "https://www.edshus.se/")], "lat": 58.91, "lon": 11.92, "dist": "165 km"},
    "Essunga": {"bolag": "Essungabostäder", "web": "https://www.essungabostader.se", "hyresvardar": [("Essungabostäder", "https://www.essungabostader.se/")], "lat": 58.17, "lon": 12.71, "dist": "85 km"},
    "Falköping": {"bolag": "Falköpings Hyresbostäder", "web": "https://www.hyresbostader.se", "hyresvardar": [("Falköpings Hyresbostäder", "https://www.hyresbostader.se/")], "lat": 58.17, "lon": 13.55, "dist": "115 km"},
    "Färgelanda": {"bolag": "Valbohem", "web": "https://www.valbohem.se", "hyresvardar": [("Valbohem", "https://www.valbohem.se/")], "lat": 58.57, "lon": 11.99, "dist": "110 km"},
    "Grästorp": {"bolag": "Grästorps fastigheter AB", "web": "https://www.grastorp.se/bygga-bo-och-miljo/bo-och-bygga/grastorps-fastigheter-ab.html",
                 "hyresvardar": [("Grästorps fastigheter AB", "https://www.grastorp.se/bygga-bo-och-miljo/bo-och-bygga/grastorps-fastigheter-ab.html")],
                 "lat": 58.33, "lon": 12.68, "dist": "100 km"},
    "Gullspång": {"bolag": "Gullspångsbostäder", "web": "https://www.gullspangsbostader.se", "hyresvardar": [("Gullspångsbostäder", "https://www.gullspangsbostader.se/")], "lat": 58.98, "lon": 14.12, "dist": "210 km"},
    "Götene": {"bolag": "Götenebostäder", "web": "https://www.gotenebostader.se", "hyresvardar": [("Götenebostäder", "https://www.gotenebostader.se/")], "lat": 58.52, "lon": 13.49, "dist": "150 km"},
    "Herrljunga": {"bolag": "Herrljungabostäder", "web": "https://www.herbo.se", "hyresvardar": [("Herrljungabostäder", "https://www.herbo.se/")], "lat": 58.07, "lon": 13.02, "dist": "85 km"},
    "Hjo": {"bolag": "Guldkroksbostäder", "web": "https://www.hjo.se/guldkroksbostader", "hyresvardar": [("Guldkroksbostäder", "https://www.hjo.se/guldkroksbostader")], "lat": 58.30, "lon": 14.28, "dist": "160 km"},
    "Karlsborg": {"bolag": "Karlsborgsbostäder", "web": "https://www.karlsborgsbostader.se", "hyresvardar": [("Karlsborgsbostäder", "https://www.karlsborgsbostader.se/")], "lat": 58.53, "lon": 14.50, "dist": "200 km"},
    "Lidköping": {"bolag": "AB Bostäder i Lidköping", "web": "https://www.bostaderlidkoping.se", "hyresvardar": [("AB Bostäder i Lidköping", "https://www.bostaderlidkoping.se/")], "lat": 58.50, "lon": 13.15, "dist": "130 km"},
    "Lilla Edet": {"bolag": "EdetHus", "web": "https://edethus.se/", "hyresvardar": [("EdetHus", "https://edethus.se/")], "lat": 58.13, "lon": 12.12, "dist": "55 km"},
    "Lysekil": {"bolag": "LysekilsBostäder", "web": "https://www.lysekilsbostader.se", "hyresvardar": [("LysekilsBostäder", "https://www.lysekilsbostader.se/")], "lat": 58.27, "lon": 11.43, "dist": "110 km"},
    "Mariestad": {"bolag": "Mariehus", "web": "https://www.mariehus.se", "hyresvardar": [("Mariehus", "https://www.mariehus.se/")], "lat": 58.70, "lon": 13.82, "dist": "175 km"},
    "Mark": {"bolag": "Marks Bostads AB", "web": "https://www.marksbostadsab.se", "hyresvardar": [("Marks Bostads AB", "https://www.marksbostadsab.se/")], "lat": 57.51, "lon": 12.69, "dist": "60 km"},
    "Mellerud": {"bolag": "Melleruds Bostäder", "web": "https://www.mellerudsbostader.se", "hyresvardar": [("Melleruds Bostäder", "https://www.mellerudsbostader.se/")], "lat": 58.70, "lon": 12.45, "dist": "125 km"},
    "Munkedal": {"bolag": "Munkbo", "web": "https://www.munkbo.se", "hyresvardar": [("Munkbo", "https://www.munkbo.se/")], "lat": 58.47, "lon": 11.68, "dist": "110 km"},
    "Orust": {"bolag": "Orustbostäder", "web": "https://www.orustbostader.se", "hyresvardar": [("Orustbostäder", "https://www.orustbostader.se/")], "lat": 58.21, "lon": 11.70, "dist": "80 km"},
    "Skara": {"bolag": "Centrumbostäder", "web": "https://www.centrumbostader.se", "hyresvardar": [("Centrumbostäder", "https://www.centrumbostader.se/")], "lat": 58.38, "lon": 13.43, "dist": "130 km"},
    "Skövde": {"bolag": "Skövdebostäder", "web": "https://www.skovdebostader.se", "hyresvardar": [("Skövdebostäder", "https://www.skovdebostader.se/")], "lat": 58.39, "lon": 13.85, "dist": "150 km"},
    "Sotenäs": {"bolag": "Sotenäsbostäder", "web": "https://www.sotenasbostader.se", "hyresvardar": [("Sotenäsbostäder", "https://www.sotenasbostader.se/")], "lat": 58.35, "lon": 11.28, "dist": "130 km"},
    "Stenungsund": {"bolag": "Stenungsundshem", "web": "https://www.stenungsundshem.se", "hyresvardar": [("Stenungsundshem", "https://www.stenungsundshem.se/")], "lat": 58.07, "lon": 11.81, "dist": "50 km"},
    "Strömstad": {"bolag": "Strömstadsbyggen", "web": "https://www.stromstadsbyggen.se", "hyresvardar": [("Strömstadsbyggen", "https://www.stromstadsbyggen.se/")], "lat": 58.93, "lon": 11.17, "dist": "165 km"},
    "Svenljunga": {"bolag": "Svenljunga Bostäder", "web": "https://www.svenljungabostader.se", "hyresvardar": [("Svenljunga Bostäder", "https://www.svenljungabostader.se/")], "lat": 57.49, "lon": 13.11, "dist": "95 km"},
    "Tanum": {"bolag": "Tanums Bostäder", "web": "https://www.tanumsbostader.se", "hyresvardar": [("Tanums Bostäder", "https://www.tanumsbostader.se/")], "lat": 58.72, "lon": 11.32, "dist": "140 km"},
    "Tibro": {"bolag": "Tibrobyggen", "web": "https://www.tibrobyggen.se", "hyresvardar": [("Tibrobyggen", "https://www.tibrobyggen.se/")], "lat": 58.41, "lon": 14.16, "dist": "170 km"},
    "Tidaholm": {"bolag": "Tidaholms Bostads AB", "web": "https://www.tidaholmsbostadsab.se", "hyresvardar": [("Tidaholms Bostads AB", "https://www.tidaholmsbostadsab.se/")], "lat": 58.18, "lon": 13.95, "dist": "160 km"},
    "Tjörn": {"bolag": "Tjörns Bostads AB (TBAB)", "web": "https://www.tjorn.se/webbplatser/tbab", "hyresvardar": [("TBAB", "https://www.tjorn.se/webbplatser/tbab")], "lat": 58.00, "lon": 11.63, "dist": "65 km"},
    "Tranemo": {"bolag": "Tranemobostäder", "web": "https://www.tranemobostader.se", "hyresvardar": [("Tranemobostäder", "https://www.tranemobostader.se/")], "lat": 57.48, "lon": 13.35, "dist": "100 km"},
    "Trollhättan": {"bolag": "Eidar", "web": "https://eidar.se", "hyresvardar": [("Eidar", "https://eidar.se/")], "lat": 58.28, "lon": 12.28, "dist": "75 km"},
    "Töreboda": {"bolag": "Törebodabostäder", "web": "https://www.torebodabostader.se", "hyresvardar": [("Törebodabostäder", "https://www.torebodabostader.se/")], "lat": 58.70, "lon": 14.12, "dist": "185 km"},
    "Uddevalla": {"bolag": "Uddevallahem", "web": "https://www.uddevallahem.se", "hyresvardar": [("Uddevallahem", "https://www.uddevallahem.se/")], "lat": 58.35, "lon": 11.93, "dist": "90 km"},
    "Ulricehamn": {"bolag": "Stubo", "web": "https://www.stubo.se", "hyresvardar": [("Stubo", "https://www.stubo.se/")], "lat": 57.79, "lon": 13.41, "dist": "100 km"},
    "Vara": {"bolag": "Vara Bostäder", "web": "https://www.varabostader.se", "hyresvardar": [("Vara Bostäder", "https://www.varabostader.se/")], "lat": 58.26, "lon": 12.95, "dist": "100 km"},
    "Vårgårda": {"bolag": "Vårgårda Bostäder", "web": "https://www.vargardabostader.se", "hyresvardar": [("Vårgårda Bostäder", "https://www.vargardabostader.se/")], "lat": 58.03, "lon": 12.80, "dist": "65 km"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "web": "https://www.vanersborgsbostader.se", "hyresvardar": [("Vänersborgsbostäder", "https://www.vanersborgsbostader.se/")], "lat": 58.37, "lon": 12.32, "dist": "85 km"},
    "Åmål": {"bolag": "Åmåls Kommunfastigheter (ÅKAB)", "web": "https://akab.amal.se/", "hyresvardar": [("ÅKAB", "https://akab.amal.se/")], "lat": 59.05, "lon": 12.70, "dist": "175 km"},
    "Öckerö": {"bolag": "Öckerö Fastigheter", "web": "https://www.ockerofastigheter.se/", "hyresvardar": [("Öckerö Fastigheter", "https://www.ockerofastigheter.se/")], "lat": 57.71, "lon": 11.64, "dist": "25 km"},
}

# ----------------------------
# 5) Session state + Rensa
# ----------------------------
if "city_selector" not in st.session_state:
    st.session_state["city_selector"] = ""

def reset_city():
    st.session_state["city_selector"] = ""

col_sel, col_btn = st.columns([4, 1])

with col_sel:
    options = [""] + sorted(list(kommuner.keys()))
    selected_city = st.selectbox(
        "Välj kommun:",
        options,
        key="city_selector",
        format_func=lambda x: "— Välj kommun —" if x == "" else x
    )

with col_btn:
    st.write(" ")
    st.write(" ")
    st.button("Rensa 🔄", on_click=reset_city)

# ----------------------------
# 6) UI: Resultat
# ----------------------------
if selected_city:
    d = kommuner[selected_city]
    kommun_namn = official_kommun_name(selected_city)

    # --- Bostadskort / Hyresvärdar ---
    st.markdown(
        f'<div class="card"><div class="section-header">🏢 {selected_city} - Hyresvärdar</div>',
        unsafe_allow_html=True
    )

    hyresvardar = d.get("hyresvardar", [])

    # Fallback: om någon kommun bara har bolag/web
    if not hyresvardar and d.get("bolag") and d.get("web"):
        hyresvardar = [(d["bolag"], d["web"])]

    st.write("Här är hyresvärdar i kommunen:")
    for name, url in hyresvardar:
        st.markdown(f"🔗 **[{name}]({url})**")

    st.markdown("</div>", unsafe_allow_html=True)

    # --- Portaler ---
    st.markdown(
        f'<div class="card"><div class="section-header">🔎 Sök lediga annonser</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        link_btn("HomeQ (kommun)", homeq_kommun_url(selected_city))

    with c2:
        if selected_city in BOPLATS_KOMMUNER:
            link_btn("Boplats (välj kommun i filter)", BOPLATS_FILTER_URL)
        else:
            st.markdown("**Boplats**: ej i deras kommun-lista")

    with c3:
        link_btn("Qasa (kommun)", qasa_kommun_url(selected_city))

    # Qasa-info (som du bad om)
    st.info("\n\n".join(QASA_INFO_TEXT))

    st.caption(f"Sökningarna ovan är satta på **{kommun_namn}** (HomeQ/Qasa).")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Karta & läge ---
    st.markdown(
        f'<div class="card"><div class="section-header">📍 Karta & Läge</div>',
        unsafe_allow_html=True
    )
    st.write(f"Avstånd till Göteborg C: **{d['dist']}**")

    map_df = pd.DataFrame({"lat": [d["lat"]], "lon": [d["lon"]]})
    map_safe(map_df, zoom=9)

    link_btn("Visa vägbeskrivning på Google Maps 🗺️", google_maps_station_url(selected_city))
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Välj en kommun för att se hyresvärdar, portal-länkar och pendlingsinformation.")

# Sidfot
st.markdown("---")
st.caption("© 2026 Västrabo | Enheten för mottagande och integration i Lerums kommun")
