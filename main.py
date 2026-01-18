import streamlit as st

# Setup page
st.set_page_config(page_title="Västrabo", page_icon="🏠", layout="centered")

# Custom CSS for beauty and font size
st.markdown("""
    <style>
    .app-title { font-size: 60px !important; color: #1E3A8A; font-weight: 800; text-align: center; margin-bottom: 0px; }
    .app-subtitle { font-size: 20px !important; color: #4B5563; text-align: center; margin-bottom: 40px; }
    .card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e5e7eb; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); margin-bottom: 25px; }
    .section-header { color: #1E3A8A; font-size: 22px; font-weight: bold; border-bottom: 3px solid #f3f4f6; padding-bottom: 10px; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #f8fafc; border: 1px solid #e2e8f0; }
    .stButton>button:hover { border-color: #1E3A8A; color: #1E3A8A; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="app-title">Västrabo</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Enheten för mottagande och integration i Lerums kommun</p>', unsafe_allow_html=True)

# Database
kommuner = {
    "Ale": {"bolag": "Alebyggen", "web": "https://www.alebyggen.se", "dist": "25 km", "tid": "20 min"},
    "Alingsås": {"bolag": "Alingsåshem", "web": "https://www.alingsashem.se", "dist": "45 km", "tid": "40 min"},
    "Bengtsfors": {"bolag": "Bengtsforsbostäder", "web": "https://www.bengtsforsbostader.se", "dist": "175 km", "tid": "2h 30 min"},
    "Bollebygd": {"bolag": "Bollebygds Hyresbostäder", "web": "https://www.bollebygdsbostader.se", "dist": "40 km", "tid": "35 min"},
    "Borås": {"bolag": "AB Bostäder i Borås", "web": "https://www.bostader.boras.se", "dist": "65 km", "tid": "55 min"},
    "Dals-Ed": {"bolag": "Edshus", "web": "https://www.edshus.se", "dist": "165 km", "tid": "2h 15 min"},
    "Essunga": {"bolag": "Essungabostäder", "web": "https://www.essungabostader.se", "dist": "85 km", "tid": "1h 10 min"},
    "Falköping": {"bolag": "Falköpings Hyresbostäder", "web": "https://www.falkopingshyresbostader.se", "dist": "115 km", "tid": "1h 10 min"},
    "Färgelanda": {"bolag": "Valbohem", "web": "https://www.valbohem.se", "dist": "110 km", "tid": "1h 30 min"},
    "Grästorp": {"bolag": "Grästorps Bostäder", "web": "https://www.grastorpsbostader.se", "dist": "100 km", "tid": "1h 20 min"},
    "Gullspång": {"bolag": "Gullspångsbostäder", "web": "https://www.gullspangsbostader.se", "dist": "210 km", "tid": "2h 45 min"},
    "Götene": {"bolag": "GöteneBostäder", "web": "https://www.gotenebostader.se", "dist": "150 km", "tid": "1h 50 min"},
    "Göteborg": {"bolag": "Bostadsbolaget", "web": "https://bostadsbolaget.se", "dist": "0 km", "tid": "0 min"},
    "Herrljunga": {"bolag": "Herrljungabostäder", "web": "https://www.herrljungabostader.se", "dist": "85 km", "tid": "55 min"},
    "Hjo": {"bolag": "Guldkroksbostäder", "web": "https://www.hjo.se/guldkroksbostader", "dist": "160 km", "tid": "2h 10 min"},
    "Härryda": {"bolag": "Förbo", "web": "https://www.foerbo.se", "dist": "20 km", "tid": "20 min"},
    "Karlsborg": {"bolag": "Karlsborgsbostäder", "web": "https://www.karlsborgsbostader.se", "dist": "200 km", "tid": "2h 40 min"},
    "Kungälv": {"bolag": "Kungälvsbostäder", "web": "https://www.kungalvsbostader.se", "dist": "20 km", "tid": "25 min"},
    "Lerum": {"bolag": "Förbo", "web": "https://www.foerbo.se", "dist": "20 km", "tid": "20 min"},
    "Lidköping": {"bolag": "AB Bostäder i Lidköping", "web": "https://www.bostaderlidkoping.se", "dist": "130 km", "tid": "1h 45 min"},
    "Lilla Edet": {"bolag": "Lilla Edet Bostads AB", "web": "https://www.lebo.se", "dist": "55 km", "tid": "50 min"},
    "Lysekil": {"bolag": "LysekilsBostäder", "web": "https://www.lysekilsbostader.se", "dist": "110 km", "tid": "1h 35 min"},
    "Mariestad": {"bolag": "Mariehus", "web": "https://www.mariehus.se", "dist": "175 km", "tid": "2h"},
    "Mark": {"bolag": "Marks Bostads AB", "web": "https://www.marksbostadsab.se", "dist": "60 km", "tid": "55 min"},
    "Mellerud": {"bolag": "Melleruds Bostäder", "web": "https://www.mellerudsbostader.se", "dist": "125 km", "tid": "1h 30 min"},
    "Munkedal": {"bolag": "Munkedals Bostäder", "web": "https://www.munkedalsbostader.se", "dist": "110 km", "tid": "1h 20 min"},
    "Mölndal": {"bolag": "Mölndalsbostäder", "web": "https://www.molndalsbostader.se", "dist": "10 km", "tid": "15 min"},
    "Orust": {"bolag": "Orustbostäder", "web": "https://www.orustbostader.se", "dist": "80 km", "tid": "1h 10 min"},
    "Partille": {"bolag": "Partillebo", "web": "https://www.partillebo.se", "dist": "10 km", "tid": "10 min"},
    "Skara": {"bolag": "Centrumbostäder", "web": "https://www.centrumbostader.se", "dist": "130 km", "tid": "1h 40 min"},
    "Skövde": {"bolag": "Skövdebostäder", "web": "https://www.skovdebostader.se", "dist": "150 km", "tid": "1h"},
    "Sotenäs": {"bolag": "Sotenäsbostäder", "web": "https://www.sotenasbostader.se", "dist": "130 km", "tid": "1h 45 min"},
    "Stenungsund": {"bolag": "Stenungsundshem", "web": "https://www.stenungsundshem.se", "dist": "50 km", "tid": "45 min"},
    "Strömstad": {"bolag": "Strömstadsbyggen", "web": "https://www.stromstadsbyggen.se", "dist": "165 km", "tid": "2h"},
    "Svenljunga": {"bolag": "Svenljunga Bostäder", "web": "https://www.svenljungabostader.se", "dist": "95 km", "tid": "1h 15 min"},
    "Tanum": {"bolag": "Tanums Bostäder", "web": "https://www.tanumsbostader.se", "dist": "140 km", "tid": "1h 40 min"},
    "Tibro": {"bolag": "Tibrobyggen", "web": "https://www.tibrobyggen.se", "dist": "170 km", "tid": "2h 15 min"},
    "Tidaholm": {"bolag": "Tidaholms Bostads AB", "web": "https://www.tidaholmsbostad.se", "dist": "160 km", "tid": "2h"},
    "Tjörn": {"bolag": "Tjörns Bostads AB", "web": "https://www.tjornsbostad.se", "dist": "65 km", "tid": "1h"},
    "Tranemo": {"bolag": "Tranemobostäder", "web": "https://www.tranemobostader.se", "dist": "100 km", "tid": "1h 20 min"},
    "Trollhättan": {"bolag": "Eidar", "web": "https://www.eidar.se", "dist": "75 km", "tid": "40 min"},
    "Töreboda": {"bolag": "Törebodabostäder", "web": "https://www.torebodabostader.se", "dist": "185 km", "tid": "2h 10 min"},
    "Uddevalla": {"bolag": "Uddevallahem", "web": "https://www.uddevallahem.se", "dist": "90 km", "tid": "1h 10 min"},
    "Ulricehamn": {"bolag": "Stubo", "web": "https://www.stubo.se", "dist": "100 km", "tid": "1h 15 min"},
    "Vara": {"bolag": "Varabostäder", "web": "https://www.varabostader.se", "dist": "100 km", "tid": "1h 15 min"},
    "Vårgårda": {"bolag": "Vårgårda Bostäder", "web": "https://www.vargardabostader.se", "dist": "65 km", "tid": "45 min"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "web": "https://www.vanersborgsbostader.se", "dist": "85 km", "tid": "55 min"},
    "Åمål": {"bolag": "Åmåls Kommunfastigheter", "web": "https://www.amalskommunfastigheter.se", "dist": "175 km", "tid": "1h 40 min"},
    "Öckerö": {"bolag": "Öckerö Bostads AB", "web": "https://www.ockerobostad.se", "dist": "25 km", "tid": "50 min"}
}

# Session State for reset
if 'kommun' not in st.session_state:
    st.session_state.kommun = ""

col_input, col_btn = st.columns([4, 1])

with col_input:
    selected = st.selectbox("Välj en kommun i listan:", [""] + sorted(list(kommuner.keys())), key="main_select")

with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("Rensa 🔄"):
        st.session_state.main_select = ""
        st.rerun()

if selected:
    data = kommuner[selected]
    
    # 🏢 Card 1: Bostad
    st.markdown(f'<div class="card"><div class="section-header">🏢 Bostad: {selected}</div>', unsafe_allow_html=True)
    st.write(f"**Kommunalt bolag:** {data['bolag']}")
    st.link_button(f"Gå till {data['bolag']} officiella hemsida ↗️", data['web'])
    
    st.write("---")
    st.write("**Sök lediga lägenheter direkt på portalerna:**")
    c1, c2, c3 = st.columns(3)
    
    # Corrected Search Links
    c1.link_button("HomeQ", f"https://www.homeq.se/search?q={selected}")
    c2.link_button("Boplats", f"https://nya.boplats.se/sok?searchgridquery={selected}")
    
    # Fix for Qasa (Lower case, no special chars)
    q_url = selected.lower().replace('å','a').replace('ä','a').replace('ö','o')
    c3.link_button("Qasa", f"https://qasa.se/p2/sv/find-home/sweden/{q_url}-kommun/lagenhet")
    st.markdown('</div>', unsafe_allow_html=True)

    # 🚆 Card 2: Pendling
    st.markdown(f'<div class="card"><div class="section-header">🚆 Pendling till Göteborg C</div>', unsafe_allow_html=True)
    st.write(f"📍 **Distans:** {data['dist']} | 🕒 **Restid:** {data['tid']}")
    st.link_button("Visa vägbeskrivning på Google Maps 🗺️", f"https://www.google.com/maps/dir/?api=1&origin={selected},+Sweden&destination=Gothenburg+Central+Station")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Välkommen! Välj en kommun för att se hyresvärdar, lediga annonser och pendlingsinfo.")

# Footer
st.markdown("---")
st.caption("© 2026 Västrabo | Enheten för mottagande och integration i Lerums kommun")
