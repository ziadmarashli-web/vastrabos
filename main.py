import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="Västrabo", page_icon="🏠", layout="centered")

# تصميم الواجهة (CSS)
st.markdown("""
    <style>
    .main-title { font-size: 42px; color: #1E3A8A; font-weight: bold; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 30px; line-height: 1.4; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .section-header { color: #1E3A8A; font-weight: bold; border-bottom: 2px solid #f3f4f6; padding-bottom: 8px; margin-bottom: 12px; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown('<p class="main-title">🏠 Västrabo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Enheten för mottagande och integration i Lerums kommun<br>Hitta din framtida bostad i Västra Götaland</p>', unsafe_allow_html=True)

# قاعدة بيانات البلديات الكاملة (عينة شاملة)
kommuner = {
    "Ale": {"bolag": "Alebyggen", "dist": "25 km", "tid": "20 min"},
    "Alingsås": {"bolag": "Alingsåshem", "dist": "45 km", "tid": "40 min"},
    "Borås": {"bolag": "AB Bostäder i Borås", "dist": "65 km", "tid": "55 min"},
    "Göteborg": {"bolag": "Bostadsbolaget, Poseidon, Familjebostäder", "dist": "0 km", "tid": "0 min"},
    "Härryda": {"bolag": "Förbo", "dist": "20 km", "tid": "20 min"},
    "Kungälv": {"bolag": "Kungälvsbostäder", "dist": "20 km", "tid": "25 min"},
    "Lerum": {"bolag": "Förbo", "dist": "20 km", "tid": "20 min (Tåg)"},
    "Mölndal": {"bolag": "Mölndalsbostäder", "dist": "10 km", "tid": "15 min"},
    "Partille": {"bolag": "Partillebo", "dist": "10 km", "tid": "10 min"},
    "Trollhättan": {"bolag": "Eidar", "dist": "75 km", "tid": "40 min (Tåg)"},
    "Uddevalla": {"bolag": "Uddevallahem", "dist": "90 km", "tid": "1h 10 min"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "dist": "85 km", "tid": "55 min"}
}

# قائمة البحث
option = st.selectbox("Välj en kommun eller sök:", [""] + sorted(list(kommuner.keys())))

if option:
    data = kommuner[option]
    
    # بطاقة معلومات السكن
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🏢 Bostadsinformation: {option}</div>', unsafe_allow_html=True)
    st.write(f"**Kommunalt bostadsbolag:** {data['bolag']}")
    
    st.write("**Sök lediga annonser direkt:**")
    c1, c2, c3 = st.columns(3)
    c1.link_button("HomeQ", f"https://www.homeq.se/search?q={option}")
    c2.link_button("Boplats", f"https://nya.boplats.se/sok?searchgridquery={option}")
    c3.link_button("Qasa", f"https://qasa.se/p2/sv/find-home/sweden/{option.lower().replace('å','a').replace('ä','a').replace('ö','o')}-kommun")
    st.markdown('</div>', unsafe_allow_html=True)

    # بطاقة التنقل
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">🚆 Pendling till Göteborg C</div>', unsafe_allow_html=True)
    st.write(f"📍 **Distans:** {data['dist']} | 🕒 **Restid:** {data['tid']}")
    
    maps_link = f"https://www.google.com/maps/dir/{option},+Sweden/Gothenburg+Central+Station"
    st.link_button("Visa på Google Maps 🗺️", maps_link)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("Välj en kommun i listan ovan för أن تبدأ البحث.")

