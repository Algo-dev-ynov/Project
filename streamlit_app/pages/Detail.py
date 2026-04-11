import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from datetime import date, timedelta

API_URL = "https://flask-api-tourisme.onrender.com"

st.set_page_config(page_title="Détail", layout="wide", page_icon="🏠")

st.markdown("""
    <style>
        header { visibility: hidden; }
        .badge-row { display:flex; flex-wrap:wrap; gap:6px; margin:8px 0; }
        .badge { background:#f7f7f7; border:1px solid #eee; border-radius:20px; padding:3px 10px; font-size:0.78rem; color:#444; }
        .review-card { background:#f9f9f9; border-radius:10px; padding:12px; margin-bottom:8px; font-size:0.85rem; }
        .contact-card { background:#f9f9f9; border-radius:12px; padding:14px; }
        .contact-item { font-size:0.88rem; margin-bottom:6px; }
        .res-card { border:1px solid #ddd; border-radius:16px; padding:16px; margin-bottom:16px; }
        .res-price { font-size:1.3rem; font-weight:700; color:#222; }
        .sug-card { border:1px solid #eee; border-radius:12px; overflow:hidden; margin-bottom:8px; }
        .sug-card img { width:100%; height:120px; object-fit:cover; }
        .sug-card-body { padding:8px 10px; font-size:0.82rem; }
    </style>
""", unsafe_allow_html=True)

uuid = st.session_state.get('selected_uuid', None)
if not uuid:
    st.error("Aucun lieu sélectionné.")
    st.stop()

place = requests.get(f"{API_URL}/places/{uuid}").json()
ratings_data = requests.get(f"{API_URL}/ratings/{uuid}").json()

if isinstance(ratings_data, list) and len(ratings_data) > 0:
    avg = round(sum(r.get('rating', 0) for r in ratings_data) / len(ratings_data), 1)
else:
    avg = None
    ratings_data = []

if st.button("← Retour"):
    st.switch_page("app.py")

col_left, col_right = st.columns([3, 2])

with col_left:
    index = st.session_state.get('selected_index', 1)
    st.image(f"https://picsum.photos/seed/{index+1}/700/300", use_container_width=True)
    st.markdown(f"### {place.get('label', 'Sans nom')}")

    address = place.get('address', {})
    st.markdown(f"📍 {address.get('addressLocality', '')} {address.get('postalCode', '')}")

    types = place.get('type', [])
    clean_types = [t for t in types if t not in ['PointOfInterest', 'PlaceOfInterest']]
    badges = " ".join([f'<span class="badge">{t}</span>' for t in clean_types])
    st.markdown(f'<div class="badge-row">{badges}</div>', unsafe_allow_html=True)

    if avg:
        st.markdown(f"⭐ **{avg}/5** ({len(ratings_data)} avis) &nbsp;&nbsp; 💰 **{place.get('price', 'N/A')} € / nuit**", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Description**")
    st.write(place.get('description', 'Aucune description disponible.'))

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        contact = place.get('contact', {})
        if any([contact.get('email'), contact.get('telephone'), contact.get('homepage')]):
            st.markdown("**Contact**")
            st.markdown('<div class="contact-card">', unsafe_allow_html=True)
            if contact.get('name'):
                st.markdown(f'<div class="contact-item">👤 {contact.get("name")}</div>', unsafe_allow_html=True)
            if contact.get('email'):
                for email in contact.get('email', []):
                    st.markdown(f'<div class="contact-item">📧 {email}</div>', unsafe_allow_html=True)
            if contact.get('telephone'):
                for tel in contact.get('telephone', []):
                    st.markdown(f'<div class="contact-item">📞 {tel}</div>', unsafe_allow_html=True)
            if contact.get('homepage'):
                for url in contact.get('homepage', []):
                    st.markdown(f'<div class="contact-item">🌐 <a href="{url}" target="_blank">{url}</a></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        if ratings_data:
            st.markdown("**Avis**")
            for r in ratings_data:
                st.markdown(f"""
                    <div class="review-card">⭐ <b>{r.get('rating','')}/5</b> — {r.get('comment','')}</div>
                """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="res-card">', unsafe_allow_html=True)
    st.markdown(f'<span class="res-price">{place.get("price", "N/A")} €</span> / nuit', unsafe_allow_html=True)
    checkin = st.date_input("Arrivée", value=date.today())
    checkout = st.date_input("Départ", value=date.today() + timedelta(days=2))
    nights = (checkout - checkin).days
    if nights > 0:
        total = nights * (place.get('price', 0) or 0)
        st.markdown(f"**{nights} nuit(s) × {place.get('price', 'N/A')} € = {total} €**")
    if st.button("Réserver", use_container_width=True, type="primary"):
        st.session_state['place_name'] = place.get('label', '')
        st.session_state['checkin'] = checkin
        st.session_state['checkout'] = checkout
        st.session_state['price'] = place.get('price', 0)
        st.switch_page("pages/Reservation.py")
    st.markdown('</div>', unsafe_allow_html=True)

    geo = place.get('geo', {})
    lat = geo.get('latitude')
    lon = geo.get('longitude')
    if lat and lon:
        st.markdown("**Localisation**")
        m = folium.Map(location=[lat, lon], zoom_start=13)
        folium.Marker([lat, lon], popup=place.get('label', ''), icon=folium.Icon(color='red', icon='home')).add_to(m)
        st_folium(m, use_container_width=True, height=280)

st.markdown("---")
st.markdown("### Autres hébergements")

suggestions = requests.get(f"{API_URL}/places").json()
suggestions = [p for p in suggestions if p.get('uuid') != uuid][:4]

sug_cols = st.columns(4)
for j, s in enumerate(suggestions):
    with sug_cols[j]:
        st.markdown(f"""
            <div class="sug-card">
                <img src="https://picsum.photos/seed/{j+30}/400/120" />
                <div class="sug-card-body">
                    <b>{s.get('label','')[:35]}</b><br>
                    <span style="color:#717171;">{s.get('address',{}).get('addressLocality','')}</span><br>
                    <span style="color:#FF385C; font-weight:700;">{s.get('price','N/A')} €</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Voir", key=f"sug_{s.get('uuid')}"):
            st.session_state['selected_uuid'] = s.get('uuid')
            st.switch_page("pages/Detail.py")

st.markdown("---")
st.markdown("""
    <div style="text-align:center; color:#717171; font-size:0.8rem; padding:16px 0;">
        © 2024 TourismeAir — Données ouvertes <a href="https://datatourisme.fr" style="color:#FF385C;">datatourisme.fr</a>
    </div>
""", unsafe_allow_html=True)