import streamlit as st
import pandas as pd
import urllib.parse as up
import re

# 1) Konfiguration
st.set_page_config(page_title="Västrabo", page_icon="🏠", layout="centered")

# Hjälpfunktion: säkra länkar även om Streamlit-versionen saknar link_button
def link(container, label: str, url: str):
    if hasattr(container, "link_button"):
        container.link_button(label, url)
    else:
        container.markdown(f"[{label}]({url})")

# Hjälpfunktioner för URL:er
def url_q(text: str) -> str:
    # URL-encodar å/ä/ö, mellanslag m.m.
    return up.quote(text, safe="")

def qasa_slug(city: str) -> str:
    # Gör en stabil "slug" för Qasa: å/ä/ö -> a/a/o, mellanslag -> bindestreck
    s = city.strip().lower()
    s = s.replace("å", "a").replace("ä", "a").replace("ö", "o")
    s = s.replace(" ", "-")
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s

# Anpassad CSS
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

# 2) Rubrik
st.markdown('<p class="app-title">Västrabo</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Enheten för mottagande och integration i Lerums kommun</p>',
    unsafe_allow_html=True
)

# 3) Databas: 49 kommuner i Västra Götaland
kommuner = {
    "Ale": {"bolag": "Alebyggen", "web": "https://www.alebyggen.se", "lat": 57.92, "lon": 12.08, "dist": "25 km"},
    "Alingsås": {"bolag": "Alingsåshem", "web": "https://www.alingsashem.se", "lat": 57.93, "lon": 12.53, "dist": "45 km"},
    "Bengtsfors": {"bolag": "Bengtsforsbostäder", "web": "https://www.bengtsforsbostader.se", "lat": 59.03, "lon": 12.22, "dist": "175 km"},
    "Bollebygd": {"bolag": "Bollebygds Hyresbostäder", "web": "https://www.bollebygdsbostader.se", "lat": 57.66, "lon": 12.57, "dist": "40 km"},
    "Borås": {"bolag": "AB Bostäder i Borås", "web": "https://www.bostader.boras.se", "lat": 57.72, "lon": 12.94, "dist": "65 km"},
    "Dals-Ed": {"bolag": "Edshus", "web": "https://www.edshus.se", "lat": 58.91, "lon": 11.92, "dist": "165 km"},
    "Essunga": {"bolag": "Essungabostäder", "web": "https://www.essungabostader.se", "lat": 58.17, "lon": 12.71, "dist": "85 km"},
    "Falköping": {"bolag": "Falköpings Hyresbostäder", "web": "https://www.falkopingshyresbostader.se", "lat": 58.17, "lon": 13.55, "dist": "115 km"},
    "Färgelanda": {"bolag": "Valbohem", "web": "https://www.valbohem.se", "lat": 58.57, "lon": 11.99, "dist": "110 km"},
    "Grästorp": {"bolag": "Grästorps Bostäder", "web": "https://www.grastorpsbostader.se", "lat": 58.33, "lon": 12.68, "dist": "100 km"},
    "Gullspång": {"bolag": "Gullspångsbostäder", "web": "https://www.gullspangsbostader.se", "lat": 58.98, "lon": 14.12, "dist": "210 km"},
    "Götene": {"bolag": "GöteneBostäder", "web": "https://www.gotenebostader.se", "lat": 58.52, "lon": 13.49, "dist": "150 km"},
    "Göteborg": {"bolag": "Bostadsbolaget", "web": "https://bostadsbolaget.se", "lat": 57.70, "lon": 11.97, "dist": "0 km"},
    "Herrljunga": {"bolag": "Herrljungabostäder", "web": "https://www.herrljungabostader.se", "lat": 58.07, "lon": 13.02, "dist": "85 km"},
    "Hjo": {"bolag": "Guldkroksbostäder", "web": "https://www.hjo.se/guldkroksbostader", "lat": 58.30, "lon": 14.28, "dist": "160 km"},
    "Härryda": {"bolag": "Förbo", "web": "https://www.foerbo.se", "lat": 57.66, "lon": 12.12, "dist": "20 km"},
    "Karlsborg": {"bolag": "Karlsborgsbostäder", "web": "https://www.karlsborgsbostader.se", "lat": 58.53, "lon": 14.50, "dist": "200 km"},
    "Kungälv": {"bolag": "Kungälvsbostäder", "web": "https://www.kungalvsbostader.se", "lat": 57.87, "lon": 11.98, "dist": "20 km"},
    "Lerum": {"bolag": "Förbo", "web": "https://www.foerbo.se", "lat": 57.77, "lon": 12.27, "dist": "20 km"},
    "Lidköping": {"bolag": "AB Bostäder i Lidköping", "web": "https://www.bostaderlidkoping.se", "lat": 58.50, "lon": 13.15, "dist": "130 km"},
    "Lilla Edet": {"bolag": "Lilla Edet Bostads AB", "web": "https://www.lebo.se", "lat": 58.13, "lon": 12.12, "dist": "55 km"},
    "Lysekil": {"bolag": "LysekilsBostäder", "web": "https://www.lysekilsbostader.se", "lat": 58.27, "lon": 11.43, "dist": "110 km"},
    "Mariestad": {"bolag": "Mariehus", "web": "https://www.mariehus.se", "lat": 58.70, "lon": 13.82, "dist": "175 km"},
    "Mark": {"bolag": "Marks Bostads AB", "web": "https://www.marksbostadsab.se", "lat": 57.51, "lon": 12.69, "dist": "60 km"},
    "Mellerud": {"bolag": "Melleruds Bostäder", "web": "https://www.mellerudsbostader.se", "lat": 58.70, "lon": 12.45, "dist": "125 km"},
    "Munkedal": {"bolag": "Munkedals Bostäder", "web": "https://www.munkedalsbostader.se", "lat": 58.47, "lon": 11.68, "dist": "110 km"},
    "Mölndal": {"bolag": "Mölndalsbostäder", "web": "https://www.molndalsbostader.se", "lat": 57.65, "lon": 12.01, "dist": "10 km"},
    "Orust": {"bolag": "Orustbostäder", "web": "https://www.orustbostader.se", "lat": 58.21, "lon": 11.70, "dist": "80 km"},
    "Partille": {"bolag": "Partillebo", "web": "https://www.partillebo.se", "lat": 57.74, "lon": 12.10, "dist": "10 km"},
    "Skara": {"bolag": "Centrumbostäder", "web": "https://www.centrumbostader.se", "lat": 58.38, "lon": 13.43, "dist": "130 km"},
    "Skövde": {"bolag": "Skövdebostäder", "web": "https://www.skovdebostader.se", "lat": 58.39, "lon": 13.85, "dist": "150 km"},
    "Sotenäs": {"bolag": "Sotenäsbostäder", "web": "https://www.sotenasbostader.se", "lat": 58.35, "lon": 11.28, "dist": "130 km"},
    "Stenungsund": {"bolag": "Stenungsundshem", "web": "https://www.stenungsundshem.se", "lat": 58.07, "lon": 11.81, "dist": "50 km"},
    "Strömstad": {"bolag": "Strömstadsbyggen", "web": "https://www.stromstadsbyggen.se", "lat": 58.93, "lon": 11.17, "dist": "165 km"},
    "Svenljunga": {"bolag": "Svenljunga Bostäder", "web": "https://www.svenljungabostader.se", "lat": 57.49, "lon": 13.11, "dist": "95 km"},
    "Tanum": {"bolag": "Tanums Bostäder", "web": "https://www.tanumsbostader.se", "lat": 58.72, "lon": 11.32, "dist": "140 km"},
    "Tibro": {"bolag": "Tibrobyggen", "web": "https://www.tibrobyggen.se", "lat": 58.41, "lon": 14.16, "dist": "170 km"},
    "Tidaholm": {"bolag": "Tidaholms Bostads AB", "web": "https://www.tidaholmsbostad.se", "lat": 58.18, "lon": 13.95, "dist": "160 km"},
    "Tjörn": {"bolag": "Tjörns Bostads AB", "web": "https://www.tjornsbostad.se", "lat": 58.00, "lon": 11.63, "dist": "65 km"},
    "Tranemo": {"bolag": "Tranemobostäder", "web": "https://www.tranemobostader.se", "lat": 57.48, "lon": 13.35, "dist": "100 km"},
    "Trollhättan": {"bolag": "Eidar", "web": "https://www.eidar.se", "lat": 58.28, "lon": 12.28, "dist": "75 km"},
    "Töreboda": {"bolag": "Törebodabostäder", "web": "https://www.torebodabostader.se", "lat": 58.70, "lon": 14.12, "dist": "185 km"},
    "Uddevalla": {"bolag": "Uddevallahem", "web": "https://www.uddevallahem.se", "lat": 58.35, "lon": 11.93, "dist": "90 km"},
    "Ulricehamn": {"bolag": "Stubo", "web": "https://www.stubo.se", "lat": 57.79, "lon": 13.41, "dist": "100 km"},
    "Vara": {"bolag": "Varabostäder", "web": "https://www.varabostader.se", "lat": 58.26, "lon": 12.95, "dist": "100 km"},
    "Vårgårda": {"bolag": "Vårgårda Bostäder", "web": "https://www.vargardabostader.se", "lat": 58.03, "lon": 12.80, "dist": "65 km"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "web": "https://www.vanersborgsbostader.se", "lat": 58.37, "lon": 12.32, "dist": "85 km"},
    "Åmål": {"bolag": "Åmåls Kommunfastigheter", "web": "https://www.amalskommunfastigheter.se", "lat": 59.05, "lon": 12.70, "dist": "175 km"},
    "Öckerö": {"bolag": "Öckerö Bostads AB", "web": "https://www.ockerobostad.se", "lat": 57.71, "lon": 11.64, "dist": "25 km"}
}

# 4) Sök + Rensa (robust utan index=None)
if "city_selector" not in st.session_state:
    st.session_state.city_selector = ""

col_sel, col_btn = st.columns([4, 1])

with col_sel:
    options = [""] + sorted(kommuner.keys())
    selected_city = st.selectbox("Välj kommun:", options, key="city_selector")

with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("Rensa 🔄"):
        st.session_state.city_selector = ""
        st.rerun()

# 5) Resultat
if selected_city:
    d = kommuner[selected_city]

    # Bostadskort
    st.markdown(
        f'<div class="card"><div class="section-header">🏢 {selected_city} - Bostad</div>',
        unsafe_allow_html=True
    )
    st.write(f"Kommunalt bostadsbolag: **{d['bolag']}**")
    link(st, f"Besök {d['bolag']} officiella hemsida ↗️", d["web"])

    st.write("---")
    st.write("**Sök lediga annonser direkt på portalerna:**")

    c1, c2, c3 = st.columns(3)

    city_param = url_q(selected_city)
    link(c1, "HomeQ", f"https://www.homeq.se/search?q={city_param}")
    link(c2, "Boplats", f"https://nya.boplats.se/sok?searchgridquery={city_param}")

    q_slug = qasa_slug(selected_city)
    link(c3, "Qasa", f"https://qasa.se/p2/sv/find-home/sweden/{q_slug}-kommun")

    st.markdown("</div>", unsafe_allow_html=True)

    # Karta & Pendling
    st.markdown(
        '<div class="card"><div class="section-header">📍 Karta & Läge</div>',
        unsafe_allow_html=True
    )
    st.write(f"Avstånd till Göteborg C: **{d['dist']}**")

    map_df = pd.DataFrame({"lat": [d["lat"]], "lon": [d["lon"]]})
    st.map(map_df, zoom=9)

    dest = up.quote_plus(f"{selected_city} Station")
    link(st, "Visa vägbeskrivning på Google Maps 🗺️",
         f"https://www.google.com/maps/dir/?api=1&destination={dest}")

    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("Välj en kommun för att se hyresvärdar, lediga annonser och pendlingsinformation.")

# Sidfot
st.markdown("---")
st.caption("© 2026 Västrabo | Enheten för mottagande och integration i Lerums kommun")
