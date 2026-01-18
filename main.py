import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="Västrabo", page_icon="🏠", layout="centered")

st.markdown("""
    <style>
    .app-title { font-size: 75px !important; color: #1E3A8A; font-weight: 900; text-align: center; margin: 0; padding: 0; }
    .app-subtitle { font-size: 20px !important; color: #4B5563; text-align: center; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 15px; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .section-header { color: #1E3A8A; font-size: 22px; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. العنوان الرئيسي
st.markdown('<p class="app-title">Västrabo</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Enheten för mottagande och integration i Lerums kommun</p>', unsafe_allow_html=True)

# 3. قاعدة البيانات (أضفت إحداثيات تقريبية للخريطة)
kommuner = {
    "Ale": {"bolag": "Alebyggen", "web": "https://www.alebyggen.se", "lat": 57.92, "lon": 12.08, "dist": "25 km"},
    "Alingsås": {"bolag": "Alingsåshem", "web": "https://www.alingsashem.se", "lat": 57.93, "lon": 12.53, "dist": "45 km"},
    "Borås": {"bolag": "AB Bostäder i Borås", "web": "https://www.bostader.boras.se", "lat": 57.72, "lon": 12.94, "dist": "65 km"},
    "Göteborg": {"bolag": "Bostadsbolaget", "web": "https://bostadsbolaget.se", "lat": 57.70, "lon": 11.97, "dist": "0 km"},
    "Härryda": {"bolag": "Förbo", "web": "https://www.foerbo.se", "lat": 57.66, "lon": 12.12, "dist": "20 km"},
    "Kungälv": {"bolag": "Kungälvsbostäder", "web": "https://www.kungalvsbostader.se", "lat": 57.87, "lon": 11.98, "dist": "20 km"},
    "Lerum": {"bolag": "Förbo", "web": "https://www.foerbo.se", "lat": 57.77, "lon": 12.27, "dist": "20 km"},
    "Mölndal": {"bolag": "Mölndalsbostäder", "web": "https://www.molndalsbostader.se", "lat": 57.65, "lon": 12.01, "dist": "10 km"},
    "Partille": {"bolag": "Partillebo", "web": "https://www.partillebo.se", "lat": 57.74, "lon": 12.10, "dist": "10 km"},
    "Trollhättan": {"bolag": "Eidar", "web": "https://www.eidar.se", "lat": 58.28, "lon": 12.28, "dist": "75 km"},
    "Uddevalla": {"bolag": "Uddevallahem", "web": "https://www.uddevallahem.se", "lat": 58.35, "lon": 11.93, "dist": "90 km"},
    "Vänersborg": {"bolag": "Vänersborgsbostäder", "web": "https://www.vanersborgsbostader.se", "lat": 58.37, "lon": 12.32, "dist": "85 km"}
}

# 4. منطق اختيار المدينة وزر المسح
if 'reset_trigger' not in st.session_state:
    st.session_state.reset_trigger = False

col_sel, col_btn = st.columns([4, 1])

with col_sel:
    # استخدام index للتحكم في التصفير
    selected_city = st.selectbox(
        "Välj kommun:", 
        [""] + sorted(list(kommuner.keys())), 
        index=0 if st.session_state.reset_trigger else None,
        key="city_box"
    )
    if st.session_state.reset_trigger:
        st.session_state.reset_trigger = False

with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("Rensa 🔄"):
        st.session_state.reset_trigger = True
        st.rerun()

# 5. عرض النتائج
if selected_city and selected_city != "":
    d = kommuner[selected_city]
    
    # بطاقة معلومات السكن
    st.markdown(f'<div class="card"><div class="section-header">🏢 {selected_city} - Bostad</div>', unsafe_allow_html=True)
    st.write(f"Kommunalt bolag: **{d['bolag']}**")
    st.link_button(f"Besök {d['bolag']} ↗️", d['web'])
    
    st.write("---")
    st.write("**Sök lediga lägenheter:**")
    c1, c2, c3 = st.columns(3)
    c1.link_button("HomeQ", f"https://www.homeq.se/search?q={selected_city}")
    c2.link_button("Boplats", f"https://nya.boplats.se/sok?searchgridquery={selected_city}")
    
    # رابط Qasa المصلح (رابط بحث عام)
    q_url = f"https://qasa.se/p2/sv/find-home/sweden/{selected_city}"
    c3.link_button("Qasa", q_url)
    st.markdown('</div>', unsafe_allow_html=True)

    # بطاقة الخريطة والمسافة
    st.markdown(f'<div class="card"><div class="section-header">📍 Karta & Läge</div>', unsafe_allow_html=True)
    st.write(f"Avstånd till Göteborg C: **{d['dist']}**")
    
    # عرض الخريطة التفاعلية
    map_data = pd.DataFrame({'lat': [d['lat']], 'lon': [d['lon']]})
    st.map(map_data, zoom=9)
    
    st.link_button("Öppna i Google Maps 🗺️", f"https://www.google.com/maps/dir/?api=1&destination={selected_city}+Station")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Välj en kommun för att se information.")

st.markdown("---")
st.caption("© 2026 Västrabo | Lerums Kommun")
