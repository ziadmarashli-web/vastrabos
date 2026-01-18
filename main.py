import streamlit as st

# Setup page
st.set_page_config(page_title="Västrabo", page_icon="🏠", layout="centered")

# Design & Font sizes
st.markdown("""
    <style>
    .app-title { font-size: 70px !important; color: #1E3A8A; font-weight: 900; text-align: center; margin-bottom: 0px; }
    .app-subtitle { font-size: 22px !important; color: #4B5563; text-align: center; margin-bottom: 40px; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; }
    .card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .section-header { color: #1E3A8A; font-size: 24px; font-weight: bold; margin-bottom: 15px; display: flex; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown('<p class="app-title">Västrabo</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Enheten för mottagande och integration i Lerums kommun</p>', unsafe_allow_html=True)

# Database
kommuner = {
    "Ale": {"bolag": "Alebyggen", "web": "https://www.alebyggen.se", "dist": "25 km", "tid": "20 min"},
    "Alingsås": {"bolag": "Alingsåshem", "web": "https://www.alingsashem.se", "dist": "45 km", "tid": "40 min"},
    "Borås": {"bolag": "AB Bostäder i Borås", "web": "https://www.bostader.boras.se", "dist": "65 km", "tid": "55 min"},
    "Göteborg": {"bolag": "Bostadsbolaget", "web": "https://bostadsbolaget.se", "dist": "0 km", "tid": "0 min"},
    "Härryda": {"bolag": "Förbo", "web": "https://www.foerbo.se", "dist": "20 km", "tid": "20 min"},
    "Kungälv": {"bolag": "Kungälvsbostäder", "web": "https://www.kungalvsbostader.se", "dist": "20 km", "tid": "25 min"},
    "Lerum": {"bolag": "Förbo", "web": "https://www.foerbo.se", "dist": "20 km", "tid": "20 min"},
    "Mölndal": {"bolag": "Mölndalsbostäder", "web": "https://www.molndalsbostader.se", "dist": "10 km", "tid": "15 min"},
    "Partille": {"bolag": "Partillebo", "web": "https://www.partillebo.se", "dist": "10 km", "tid": "10 min"},
    "Trollhättan": {"bolag": "Eidar", "web": "https://www.eidar.se", "dist": "75 km", "tid": "40 min"},
    "Uddevalla": {"bolag": "Uddevallahem", "web": "https://www.uddevallahem.se", "dist": "90 km", "tid": "1h 10 min"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "web": "https://www.vanersborgsbostader.se", "dist": "85 km", "tid": "55 min"}
} # يمكنك إضافة بقية الـ 49 بلدية هنا لاحقاً بنفس النمط

# Logic for Reset
if 'selected_k' not in st.session_state:
    st.session_state.selected_k = ""

col_search, col_reset = st.columns([4, 1])

with col_search:
    choice = st.selectbox("Välj kommun:", [""] + sorted(list(kommuner.keys())), key="k_selector")

with col_reset:
    st.write(" ")
    st.write(" ")
    if st.button("Rensa 🔄"):
        st.session_state.k_selector = ""
        st.rerun()

if choice:
    d = kommuner[choice]
    
    # Card 1: Official Company
    st.markdown(f'<div class="card"><div class="section-header">🏢 Bostadsbolag i {choice}</div>', unsafe_allow_html=True)
    st.write(f"Det kommunala bolaget är **{d['bolag']}**.")
    st.link_button(f"Besök {d['bolag']} ↗️", d['web'])
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 2: Search Portals (The Links you requested)
    st.markdown(f'<div class="card"><div class="section-header">🔍 Lediga annonser just nu</div>', unsafe_allow_html=True)
    st.write(f"Klicka nedan för att se sökresultat för **{choice}**:")
    
    c1, c2, c3 = st.columns(3)
    
    # HomeQ: Direct Search Link
    c1.link_button("HomeQ", f"https://www.homeq.se/search?q={choice}")
    
    # Boplats: Filtered Search Link
    c2.link_button("Boplats", f"https://nya.boplats.se/sok?searchgridquery={choice}")
    
    # Qasa: NEW CORRECTED LINK (Search based)
    q_clean = choice.lower().replace('å','a').replace('ä','a').replace('ö','o')
    c3.link_button("Qasa", f"https://qasa.se/p2/sv/find-home/sweden/{q_clean}-kommun")
    st.markdown('</div>', unsafe_allow_html=True)

    # Card 3: Google Maps
    st.markdown(f'<div class="card"><div class="section-header">📍 Pendling & Karta</div>', unsafe_allow_html=True)
    st.write(f"**Avstånd:** {d['dist']} | **Restid:** ca {d['tid']} till Göteborg C")
    
    # Google Maps Routing link
    maps_url = f"https://www.google.com/maps/dir/?api=1&destination={choice}+Station&travelmode=transit"
    st.link_button("Visa vägbeskrivning (Karta) 🗺️", maps_url)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Välkommen till Västrabo. Välj en kommun för att komma igång.")

st.markdown("---")
st.caption("© 2026 Västrabo | Lerums Kommun")
