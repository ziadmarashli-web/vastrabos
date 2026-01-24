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
# 1A) Dölj toppraden (Share/GitHub/meny) i hosting-miljöer
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
# 1B) Enkel styling
# ----------------------------
st.markdown(
    """
    <style>
    .app-title { font-size: 64px !important; color: #1E3A8A; font-weight: 900; text-align: center; margin: 0; padding: 0; }
    .app-subtitle { font-size: 18px !important; color: #4B5563; text-align: center; margin-bottom: 18px; }
    .divider-line { border-bottom: 2px solid #eee; margin: 0 0 18px 0; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="app-title">Söka bostad i Västra Götaland</div>', unsafe_allow_html=True)
st.markdown('<div class="app-subtitle">Enheten för mottagande och integration i Lerums kommun</div>', unsafe_allow_html=True)
st.markdown('<div class="divider-line"></div>', unsafe_allow_html=True)

# ----------------------------
# 2) Robust hjälpfunktioner
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
    """Google-sökning för hyresvärdar i vald kommun."""
    q = urllib.parse.quote_plus(f"hyresvärdar {kommun} bostad")
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

# ----------------------------
# 3) Konstanter
# ----------------------------
BOPLATS_FILTER_URL = "https://boplats.se/filtrera?listtype=imagelist&types=1hand"
BOPLATS_KOMMUNER = {
    "Göteborg","Ale","Alingsås","Borås","Herrljunga","Härryda","Kungsbacka","Kungälv",
    "Lerum","Mölndal","Partille","Skara","Stenungsund","Strömstad","Trollhättan","Uddevalla","Öckerö"
}

FOERBO_INFO_URL = "https://www.foerbo.se/"
FOERBO_LEDIG_URL = "https://minasidor.foerbo.se/market/residential"

QASA_INFO_TEXT = (
    "Qasa är en seriös tjänst.\n\n"
    "Använd gärna Qasa, men följ alltid säkerhetsråden:\n\n"
    "• Betala inte pengar innan du har sett bostaden och fått tydligt avtal.\n"
    "• Håll kommunikationen i plattformen när det går.\n"
    "• Var försiktig om någon vill flytta kontakten till WhatsApp/privat direkt."
)

# ----------------------------
# 4) Data: kommuner
#    - hyresvardar: lista av (namn, url, kategori) där kategori = "Kommunal" eller "Privat"
#    - time är valfri (restid), kan fyllas på senare
# ----------------------------
kommuner = {
    "Göteborg": {
        "lat": 57.70, "lon": 11.97, "dist": "0 km", "time": "0 min",
        "hyresvardar": [
            ("Bostadsbolaget", "https://bostadsbolaget.se/", "Kommunal"),
            ("Poseidon", "https://poseidon.goteborg.se/", "Kommunal"),
            ("Familjebostäder", "https://familjebostader.se/", "Kommunal"),
        ],
    },
    "Mölndal": {
        "lat": 57.65, "lon": 12.01, "dist": "10 km", "time": "15–25 min",
        "hyresvardar": [
            ("Mölndalsbostäder", "https://www.molndalsbostader.se/", "Kommunal"),
            ("Wallenstam", "https://www.wallenstam.se/", "Privat"),
        ],
    },
    "Partille": {
        "lat": 57.74, "lon": 12.10, "dist": "10 km", "time": "15–25 min",
        "hyresvardar": [
            ("Partillebo", "https://www.partillebo.se/", "Kommunal"),
        ],
    },
    "Lerum": {
        "lat": 57.77, "lon": 12.27, "dist": "20 km", "time": "ca 20–30 min",
        "hyresvardar": [
            ("Förbo (info)", FOERBO_INFO_URL, "Kommunal"),
            ("Förbo – Lediga bostäder (Mina sidor)", FOERBO_LEDIG_URL, "Kommunal"),
        ],
    },
    "Härryda": {
        "lat": 57.66, "lon": 12.12, "dist": "20 km", "time": "ca 20–40 min",
        "hyresvardar": [
            ("Förbo (info)", FOERBO_INFO_URL, "Kommunal"),
            ("Förbo – Lediga bostäder (Mina sidor)", FOERBO_LEDIG_URL, "Kommunal"),
        ],
    },
    "Borås": {
        "lat": 57.72, "lon": 12.94, "dist": "65 km", "time": "ca 55–70 min",
        "hyresvardar": [
            ("Bostäder i Borås", "https://www.bostaderiboras.se/", "Kommunal"),
            ("Willhem", "https://www.willhem.se/", "Privat"),
        ],
    },

    # --- Resterande (minst 1 hyresvärd per kommun) ---
    "Ale": {"lat": 57.92, "lon": 12.08, "dist": "25 km", "hyresvardar": [("Alebyggen", "https://www.alebyggen.se/", "Kommunal")]},
    "Alingsås": {"lat": 57.93, "lon": 12.53, "dist": "45 km", "hyresvardar": [("Alingsåshem", "https://www.alingsashem.se/", "Kommunal")]},
    "Bengtsfors": {"lat": 59.03, "lon": 12.22, "dist": "175 km", "hyresvardar": [("Bengtsforshus", "https://bengtsforshus.se/", "Kommunal")]},
    "Bollebygd": {"lat": 57.66, "lon": 12.57, "dist": "40 km", "hyresvardar": [("Bollebo", "https://www.bollebo.se/", "Kommunal")]},
    "Dals-Ed": {"lat": 58.91, "lon": 11.92, "dist": "165 km", "hyresvardar": [("Edshus", "https://www.edshus.se/", "Kommunal")]},
    "Essunga": {"lat": 58.17, "lon": 12.71, "dist": "85 km", "hyresvardar": [("Essungabostäder", "https://www.essungabostader.se/", "Kommunal")]},
    "Falköping": {"lat": 58.17, "lon": 13.55, "dist": "115 km", "hyresvardar": [("Falköpings Hyresbostäder", "https://www.hyresbostader.se/", "Kommunal")]},
    "Färgelanda": {"lat": 58.57, "lon": 11.99, "dist": "110 km", "hyresvardar": [("Valbohem", "https://www.valbohem.se/", "Kommunal")]},
    "Grästorp": {"lat": 58.33, "lon": 12.68, "dist": "100 km", "hyresvardar": [("Grästorps fastigheter AB", "https://www.grastorp.se/bygga-bo-och-miljo/bo-och-bygga/grastorps-fastigheter-ab.html", "Kommunal")]},
    "Gullspång": {"lat": 58.98, "lon": 14.12, "dist": "210 km", "hyresvardar": [("Gullspångsbostäder", "https://www.gullspangsbostader.se/", "Kommunal")]},
    "Götene": {"lat": 58.52, "lon": 13.49, "dist": "150 km", "hyresvardar": [("Götenebostäder", "https://www.gotenebostader.se/", "Kommunal")]},
    "Herrljunga": {"lat": 58.07, "lon": 13.02, "dist": "85 km", "hyresvardar": [("Herrljungabostäder", "https://www.herbo.se/", "Kommunal")]},
    "Hjo": {"lat": 58.30, "lon": 14.28, "dist": "160 km", "hyresvardar": [("Guldkroksbostäder", "https://www.hjo.se/guldkroksbostader", "Kommunal")]},
    "Karlsborg": {"lat": 58.53, "lon": 14.50, "dist": "200 km", "hyresvardar": [("Karlsborgsbostäder", "https://www.karlsborgsbostader.se/", "Kommunal")]},
    "Kungälv": {"lat": 57.87, "lon": 11.98, "dist": "20 km", "hyresvardar": [("Kungälvsbostäder", "https://www.kungalvsbostader.se/", "Kommunal")]},
    "Lidköping": {"lat": 58.50, "lon": 13.15, "dist": "130 km", "hyresvardar": [("AB Bostäder i Lidköping", "https://www.bostaderlidkoping.se/", "Kommunal")]},
    "Lilla Edet": {"lat": 58.13, "lon": 12.12, "dist": "55 km", "hyresvardar": [("EdetHus", "https://edethus.se/", "Kommunal")]},
    "Lysekil": {"lat": 58.27, "lon": 11.43, "dist": "110 km", "hyresvardar": [("LysekilsBostäder", "https://www.lysekilsbostader.se/", "Kommunal")]},
    "Mariestad": {"lat": 58.70, "lon": 13.82, "dist": "175 km", "hyresvardar": [("Mariehus", "https://www.mariehus.se/", "Kommunal")]},
    "Mark": {"lat": 57.51, "lon": 12.69, "dist": "60 km", "hyresvardar": [("Marks Bostads AB", "https://www.marksbostadsab.se/", "Kommunal")]},
    "Mellerud": {"lat": 58.70, "lon": 12.45, "dist": "125 km", "hyresvardar": [("Melleruds Bostäder", "https://www.mellerudsbostader.se/", "Kommunal")]},
    "Munkedal": {"lat": 58.47, "lon": 11.68, "dist": "110 km", "hyresvardar": [("Munkbo", "https://www.munkbo.se/", "Kommunal")]},
    "Orust": {"lat": 58.21, "lon": 11.70, "dist": "80 km", "hyresvardar": [("Orustbostäder", "https://www.orustbostader.se/", "Kommunal")]},
    "Skara": {"lat": 58.38, "lon": 13.43, "dist": "130 km", "hyresvardar": [("Centrumbostäder", "https://www.centrumbostader.se/", "Kommunal")]},
    "Skövde": {"lat": 58.39, "lon": 13.85, "dist": "150 km", "hyresvardar": [("Skövdebostäder", "https://www.skovdebostader.se/", "Kommunal")]},
    "Sotenäs": {"lat": 58.35, "lon": 11.28, "dist": "130 km", "hyresvardar": [("Sotenäsbostäder", "https://www.sotenasbostader.se/", "Kommunal")]},
    "Stenungsund": {"lat": 58.07, "lon": 11.81, "dist": "50 km", "hyresvardar": [("Stenungsundshem", "https://www.stenungsundshem.se/", "Kommunal")]},
    "Strömstad": {"lat": 58.93, "lon": 11.17, "dist": "165 km", "hyresvardar": [("Strömstadsbyggen", "https://www.stromstadsbyggen.se/", "Kommunal")]},
    "Svenljunga": {"lat": 57.49, "lon": 13.11, "dist": "95 km", "hyresvardar": [("Svenljunga Bostäder", "https://www.svenljungabostader.se/", "Kommunal")]},
    "Tanum": {"lat": 58.72, "lon": 11.32, "dist": "140 km", "hyresvardar": [("Tanums Bostäder", "https://www.tanumsbostader.se/", "Kommunal")]},
    "Tibro": {"lat": 58.41, "lon": 14.16, "dist": "170 km", "hyresvardar": [("Tibrobyggen", "https://www.tibrobyggen.se/", "Kommunal")]},
    "Tidaholm": {"lat": 58.18, "lon": 13.95, "dist": "160 km", "hyresvardar": [("Tidaholms Bostads AB", "https://www.tidaholmsbostadsab.se/", "Kommunal")]},
    "Tjörn": {"lat": 58.00, "lon": 11.63, "dist": "65 km", "hyresvardar": [("TBAB", "https://www.tjorn.se/webbplatser/tbab", "Kommunal")]},
    "Tranemo": {"lat": 57.48, "lon": 13.35, "dist": "100 km", "hyresvardar": [("Tranemobostäder", "https://www.tranemobostader.se/", "Kommunal")]},
    "Trollhättan": {"lat": 58.28, "lon": 12.28, "dist": "75 km", "hyresvardar": [("Eidar", "https://eidar.se/", "Kommunal")]},
    "Töreboda": {"lat": 58.70, "lon": 14.12, "dist": "185 km", "hyresvardar": [("Törebodabostäder", "https://www.torebodabostader.se/", "Kommunal")]},
    "Uddevalla": {"lat": 58.35, "lon": 11.93, "dist": "90 km", "hyresvardar": [("Uddevallahem", "https://www.uddevallahem.se/", "Kommunal")]},
    "Ulricehamn": {"lat": 57.79, "lon": 13.41, "dist": "100 km", "hyresvardar": [("Stubo", "https://www.stubo.se/", "Kommunal")]},
    "Vara": {"lat": 58.26, "lon": 12.95, "dist": "100 km", "hyresvardar": [("Vara Bostäder", "https://www.varabostader.se/", "Kommunal")]},
    "Vårgårda": {"lat": 58.03, "lon": 12.80, "dist": "65 km", "hyresvardar": [("Vårgårda Bostäder", "https://www.vargardabostader.se/", "Kommunal")]},
    "Vänersborg": {"lat": 58.37, "lon": 12.32, "dist": "85 km", "hyresvardar": [("Vänersborgsbostäder", "https://www.vanersborgsbostader.se/", "Kommunal")]},
    "Åmål": {"lat": 59.05, "lon": 12.70, "dist": "175 km", "hyresvardar": [("ÅKAB", "https://akab.amal.se/", "Kommunal")]},
    "Öckerö": {"lat": 57.71, "lon": 11.64, "dist": "25 km", "hyresvardar": [("Öckerö Fastigheter", "https://www.ockerofastigheter.se/", "Kommunal")]},
}

# ----------------------------
# 5) Kommunväljare med SÖKFUNKTION + Rensa
# ----------------------------
if "city_selector" not in st.session_state:
    st.session_state["city_selector"] = ""

search_text = st.text_input("Sök kommun (skriv några bokstäver):", value="")

def reset_city():
    st.session_state["city_selector"] = ""

col_sel, col_btn = st.columns([4, 1])

all_kommuner = sorted(list(kommuner.keys()))
if search_text.strip():
    filtered = [k for k in all_kommuner if search_text.lower() in k.lower()]
else:
    filtered = all_kommuner

with col_sel:
    options = [""] + filtered
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

    # ---------- Hyresvärdar ----------
    with st.container(border=True):
        st.subheader(f"🏢 {selected_city} – Hyresvärdar")
        st.write("Här är hyresvärdar i kommunen:")

        grupper = {"Kommunal": [], "Privat": [], "Övrigt": []}
        for item in d.get("hyresvardar", []):
            if len(item) == 3:
                name, url, cat = item
                cat = cat if cat in ("Kommunal", "Privat") else "Övrigt"
            else:
                name, url = item[0], item[1]
                cat = "Övrigt"
            grupper[cat].append((name, url))

        if grupper["Kommunal"]:
            st.markdown("**Kommunal**")
            for name, url in grupper["Kommunal"]:
                st.markdown(f"🔗 **[{name}]({url})**")

        if grupper["Privat"]:
            st.markdown("**Privat**")
            for name, url in grupper["Privat"]:
                st.markdown(f"🔗 **[{name}]({url})**")

        if grupper["Övrigt"]:
            st.markdown("**Övrigt**")
            for name, url in grupper["Övrigt"]:
                st.markdown(f"🔗 **[{name}]({url})**")

        # AUTOMATISK Google-knapp om listan är liten (≤ 1)
        if len(d.get("hyresvardar", [])) <= 1:
            st.divider()
            st.caption("Hittar du inte fler hyresvärdar?")
            link_btn(f"🔎 Sök hyresvärdar i {selected_city} på Google", google_hyresvardar_url(selected_city))

    # ---------- Portaler ----------
    with st.container(border=True):
        st.subheader("🔎 Sök lediga annonser")
        c1, c2, c3 = st.columns(3)

        with c1:
            link_btn("HomeQ (kommun)", homeq_kommun_url(selected_city))

        with c2:
            if selected_city in BOPLATS_KOMMUNER:
                link_btn("Boplats (välj kommun i filter)", BOPLATS_FILTER_URL)
            else:
                st.caption("Boplats: ej i deras kommun-lista")

        with c3:
            link_btn("Qasa (kommun)", qasa_kommun_url(selected_city))

        with st.expander("Säkerhetstips (Qasa och privata annonser)", expanded=False):
            st.info(QASA_INFO_TEXT)

        st.caption(f"Sökningarna ovan är satta på **{kommun_namn}** (HomeQ/Qasa).")

    # ---------- Pendling & Karta ----------
    with st.container(border=True):
        st.subheader("📍 Pendling & Karta")
        st.write(f"Avstånd till Göteborg C: **{d.get('dist', '—')}**")
        if d.get("time"):
            st.write(f"Restid (cirka): **{d['time']}**")

        with st.expander("Visa karta", expanded=False):
            map_df = pd.DataFrame({"lat": [d["lat"]], "lon": [d["lon"]]})
            map_safe(map_df, zoom=9)

        link_btn("Visa vägbeskrivning på Google Maps 🗺️", google_maps_station_url(selected_city))

else:
    st.info("Välj en kommun för att se hyresvärdar, portal-länkar och pendlingsinformation.")

st.markdown("---")
st.caption("© 2026 Västrabo | Enheten för mottagande och integration i Lerums kommun")
