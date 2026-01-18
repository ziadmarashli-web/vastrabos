import streamlit as st

# Inställningar
st.set_page_config(page_title="Västrabo", page_icon="🏠", layout="centered")

# Design (CSS)
st.markdown("""
    <style>
    .main-title { font-size: 42px; color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 30px; line-height: 1.4; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .section-header { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #f3f4f6; padding-bottom: 8px; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

# Rubrik
st.markdown('<p class="main-title">🏠 Västrabo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Enheten för mottagande och integration i Lerums kommun<br>Hitta din framtida bostad i Västra Götaland</p>', unsafe_allow_html=True)

# Komplett databas för alla 49 kommuner i VGR
kommuner = {
    "Ale": {"bolag": "Alebyggen", "dist": "25 km", "tid": "20 min"},
    "Alingsås": {"bolag": "Alingsåshem", "dist": "45 km", "tid": "40 min"},
    "Bengtsfors": {"bolag": "Bengtsforsbostäder", "dist": "175 km", "tid": "2h 30 min"},
    "Bollebygd": {"bolag": "Bollebygds Hyresbostäder", "dist": "40 km", "tid": "35 min"},
    "Borås": {"bolag": "AB Bostäder i Borås", "dist": "65 km", "tid": "55 min"},
    "Dals-Ed": {"bolag": "Edshus", "dist": "165 km", "tid": "2h 15 min"},
    "Essunga": {"bolag": "Essungabostäder", "dist": "85 km", "tid": "1h 10 min"},
    "Falköping": {"bolag": "Falköpings Hyresbostäder", "dist": "115 km", "tid": "1h 10 min"},
    "Färgelanda": {"bolag": "Valbohem", "dist": "110 km", "tid": "1h 30 min"},
    "Grästorp": {"bolag": "Grästorps Bostäder", "dist": "100 km", "tid": "1h 20 min"},
    "Gullspång": {"bolag": "Gullspångsbostäder", "dist": "210 km", "tid": "2h 45 min"},
    "Götene": {"bolag": "GöteneBostäder", "dist": "150 km", "tid": "1h 50 min"},
    "Göteborg": {"bolag": "Bostadsbolaget, Poseidon, Familjebostäder", "dist": "0 km", "tid": "0 min"},
    "Herrljunga": {"bolag": "Herrljungabostäder", "dist": "85 km", "tid": "55 min"},
    "Hjo": {"bolag": "Guldkroksbostäder", "dist": "160 km", "tid": "2h 10 min"},
    "Härryda": {"bolag": "Förbo", "dist": "20 km", "tid": "20 min"},
    "Karlsborg": {"bolag": "Karlsborgsbostäder", "dist": "200 km", "tid": "2h 40 min"},
    "Kungälv": {"bolag": "Kungälvsbostäder", "dist": "20 km", "tid": "25 min"},
    "Lerum": {"bolag": "Förbo", "dist": "20 km", "tid": "20 min (Tåg)"},
    "Lidköping": {"bolag": "AB Bostäder i Lidköping", "dist": "130 km", "tid": "1h 45 min"},
    "Lilla Edet": {"bolag": "Lilla Edet Bostads AB", "dist": "55 km", "tid": "50 min"},
    "Lysekil": {"bolag": "LysekilsBostäder", "dist": "110 km", "tid": "1h 35 min"},
    "Mariestad": {"bolag": "Mariehus", "dist": "175 km", "tid": "2h"},
    "Mark": {"bolag": "Marks Bostads AB", "dist": "60 km", "tid": "55 min"},
    "Mellerud": {"bolag": "Melleruds Bostäder", "dist": "125 km", "tid": "1h 30 min"},
    "Munkedal": {"bolag": "Munkedals Bostäder", "dist": "110 km", "tid": "1h 20 min"},
    "Mölndal": {"bolag": "Mölndalsbostäder", "dist": "10 km", "tid": "15 min"},
    "Orust": {"bolag": "Orustbostäder", "dist": "80 km", "tid": "1h 10 min"},
    "Partille": {"bolag": "Partillebo", "dist": "10 km", "tid": "10 min"},
    "Skara": {"bolag": "Centrumbostäder", "dist": "130 km", "tid": "1h 40 min"},
    "Skövde": {"bolag": "Skövdebostäder", "dist": "150 km", "tid": "1h"},
    "Sotenäs": {"bolag": "Sotenäsbostäder", "dist": "130 km", "tid": "1h 45 min"},
    "Stenungsund": {"bolag": "Stenungsundshem", "dist": "50 km", "tid": "45 min"},
    "Strömstad": {"bolag": "Strömstadsbyggen", "dist": "165 km", "tid": "2h"},
    "Svenljunga": {"bolag": "Svenljunga Bostäder", "dist": "95 km", "tid": "1h 15 min"},
    "Tanum": {"bolag": "Tanums Bostäder", "dist": "140 km", "tid": "1h 40 min"},
    "Tibro": {"bolag": "Tibrobyggen", "dist": "170 km", "tid": "2h 15 min"},
    "Tidaholm": {"bolag": "Tidaholms Bostads AB", "dist": "160 km", "tid": "2h"},
    "Tjörn": {"bolag": "Tjörns Bostads AB", "dist": "65 km", "tid": "1h"},
    "Tranemo": {"bolag": "Tranemobostäder", "dist": "100 km", "tid": "1h 20 min"},
    "Trollhättan": {"bolag": "Eidar", "dist": "75 km", "tid": "40 min"},
    "Töreboda": {"bolag": "Törebodabostäder", "dist": "185 km", "tid": "2h 10 min"},
    "Uddevalla": {"bolag": "Uddevallahem", "dist": "90 km", "tid": "1h 10 min"},
    "Ulricehamn": {"bolag": "Stubo", "dist": "100 km", "tid": "1h 15 min"},
    "Vara": {"bolag": "Varabostäder", "dist": "100 km", "tid": "1h 15 min"},
    "Vårgårda": {"bolag": "Vårgårda Bostäder", "dist": "65 km", "tid": "45 min"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "dist": "85 km", "tid": "55 min"},
    "Åmål": {"bolag": "Åmåls Kommunfastigheter", "dist": "175 km", "tid": "1h 40 min"},
    "Öckerö": {"bolag": "Öckerö Bostads AB", "dist": "25 km", "tid": "50 min"}
}

# Sökfunktion
option = st.selectbox("Välj en kommun för att se detaljer:", [""] + sorted(list(kommuner.keys())))

if option:
    data = kommuner[option]
    
    # Bostadskort
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🏢 Bostadsinformation: {option}</div>', unsafe_allow_html=True)
    st.write(f"**Kommunalt bostadsbolag:** {data['bolag']}")
    st.write("**Sök lediga annonser direkt:**")
    
    c1, c2, c3 = st.columns(3)
    c1.link_button("HomeQ", f"https://www.homeq.se/search?q={option}")
    c2.link_button("Boplats", f"https://nya.boplats.se/sok?searchgridquery={option}")
    # Fix för länkar med å,ä,ö
    q_url = option.lower().replace('å','a').replace('ä','a').replace('ö','o')
    c3.link_button("Qasa", f"https://qasa.se/p2/sv/find-home/sweden/{q_url}-kommun")
    st.markdown('</div>', unsafe_allow_html=True)

    # Pendlingskort
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🚆 Pendling till Göteborg C</div>', unsafe_allow_html=True)
    st.write(f"📍 **Distans:** {data['dist']}")
    st.write(f"🕒 **Ungefärlig restid:** {data['tid']}")
    
    maps_url = f"https://www.google.com/maps/dir/{option},+Sweden/Gothenburg+Central+Station"
    st.link_button("Visa vägbeskrivning på Google Maps 🗺️", maps_url)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Vänligen välj en kommun i listan ovan för att börja söka.")

# Footer
st.markdown("---")
st.caption("© 2026 Västrabo - Ett stödverktyg för nyanlända i Västra Götaland")
